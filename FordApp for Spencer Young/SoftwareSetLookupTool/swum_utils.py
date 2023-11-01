# -*- coding: utf-8 -*-
import inspect
import os
import re
import ast
import sys
import time
import json
from tarfile import TarFile
import numpy
import logging
import requests
import subprocess
import traceback
import winshell
from logging import Filter, LogRecord
from ctypes import c_long, py_object, pythonapi
from bs4 import BeautifulSoup
from jira import Issue
from jira.resilientsession import ResilientSession
from lxml import etree
from copy import deepcopy
from omegaconf import OmegaConf
from shutil import rmtree, copyfile
from pymongo import MongoClient, InsertOne, DeleteOne, ReplaceOne, UpdateOne, client_session
from common_lib.http_util import download_with_progress_bar_retry
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from common_lib.ford_nexus import Nexus
from common_lib.http_util import SessionWithDefaultSslContext
from jira_interface.jira_interface import FordJIRA
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from multiprocessing import Process
from threading import Thread
from swum_cloud_manager.conf import (
    NEXUS_REPOSITORY_URL, LOG_STR_FORMAT, URL_FORMS, MONGO_DB_SERVER_EXE,
    PROJECT, ISSUE_TYPE, COMPONENTS, SEVERITY, PRIORITY, LABELS, SUMMARY,
    DESCRIPTION, ASSIGNEE_ID, JIRA_KEY, PLATFORMS, FOUND_IN_BUILD, STATUS,
    SUPPORTED_DOMAIN_INSTANCES, SUPPORTED_ECU_APPS, TEST_ENVIRONMENT, OPEN,
    CLOSED, JiraPriority, JiraSeverity, JiraComponent, JiraLabel, TCU,
    JiraIssueType, JiraProject, OWNER_GUIDE_LINEAGE, THIRTY_MINUTES, THREADS,
    MAX_JIRA_CHARACTERS, JSON, HTML, NEXUS_ARTIFACT, LINKS, get_logs_folder,
    NAME, VERSION, FILE, NEXUS_URL, ECG, VMCU_TYPES, get_workstation, NexusConfig,
    SUPPORTED_ECU_TYPES, DomainInstance, SYSTEM_SETTINGS_FILE, SWUM_USER,
    DOMAIN_INSTANCES, ROOT_DIR, ASSEMBLIES, APPS_LIST, ECU, DEVELOPMENT,
    BUILD, VARIANT, CFG_FILE, ACTIVE, SYNC_VARIANTS_IGNORE_LIST, PRODUCTION,
    URL_PATTERN_BUILD_TYPE, URL_PATTERN_ECU_TYPE, VALID_URL_PATTERN,
    SUPPORTED_ECU_VERSIONS, DEFAULT_SETTINGS, URL_TYPES, SYNC, VadrConfig,
    ARTIFACT_VERSION, SEARCH_VALUE, VMCU, CCPU, FILES, update_workstation,
    PHOENIX, TEST_DATASET_FILE, BUILD_URL, COLUMN_NAME, SEQUENCE_NAME, JOB_ARGS,
    REQUIRED_JOB_ARGS, PENDING_JOBS, REQUESTED_BY, PC_NAME, TIME_REQUESTED, ADDED_BY,
    PAST_JOBS_LIMIT, ECG1, TCU1, TCU2, ECG2, NEXUS_VERSION, FILE_UPLOAD_STATUS,
    DOMAIN_INSTANCE_STATUS, APPLICATION_STATUS, SWS_STATUS, NODE, NETWORK, UPLOAD_SPEED,
    DOWNLOAD_SPEED, IP_ADDRESS, ID, START_TIME, END_TIME, TIME_ELAPSED, FAILURE_REASON,
    UPLOAD_STATUS, BUILD_NUMBER, PROCESSED_BY, ARGS, KWARGS, IP_API, PACKAGES, TIME_OUT, TWO_HOUR, TIMER, PROXY_ENV,
    DOMAIN_AND_SWS, JENKINS_PATTERN, GROUP_ID, AOS_NEXUS, PHX_NEXUS, NEXUS_FETCH_REPOSITORY, NEXUS_ARTIFACT_ID,
    NEXUS_NAME, NEXUS_EXTENSION, FPN, PENDING_UPLOADS, DEV_FILE_PATTERN, SYSTEM_NAME, MASTER_BUILD_PATTERN, USERS,
    BUILD_NUMBER_PATTERN,
)
from zipfile import ZipFile, is_zipfile
from datetime import datetime
from pathlib import Path

console_formatter = logging.Formatter(LOG_STR_FORMAT)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
null_handler = logging.NullHandler()
null_handler.setLevel(logging.DEBUG)
null_handler.setFormatter(logging.Formatter(LOG_STR_FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(null_handler)
LOG_VERSIONS = {}
# Load Hydra Environment Values
cfg = OmegaConf.load(CFG_FILE)


def get_latest_log_version(log_name):
    log_version = 0
    try:
        log_version = LOG_VERSIONS.get(log_name, 0)
        LOG_VERSIONS[log_name] = deepcopy(log_version)
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve latest log version!")
    finally:
        return log_version


def create_log_file(path, log_name, suffix="_debug.log", log_version=None):
    """
    Creates new log file if the current log is too large. (greater than 1GB) or
    if the current date is different from when the current log was created.

    :param path: directory in which to create log file.
    :param log_name: the name of the log which needs to be created.
        creates a new logger if no logger with provider name exist.
    :param suffix: suffix to add at the end of the log name.
    :param log_version: create log file with a specific version number
    :type path: str
    :type log_name: str
    :type suffix: str
    :type log_version: int

    :return: Logger - logging object with the requested name.
    """
    logger.debug(
        f"Creating new log file in path={path} for log_name={log_name}, "
        f"suffix={suffix}, log_version={log_version}"
    )
    time_now = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    log_file = f"{log_name}{suffix}"
    if log_version is None:
        # Get version number for the specified log file
        log_version = get_latest_log_version(log_file)
    else:
        # Update version number for the specified log file
        current_version = LOG_VERSIONS.get(log_file, 0)
        LOG_VERSIONS[log_file] = max(log_version, current_version)
    if log_version < 1:
        new_log_name = f"{time_now} {log_name}{suffix}"
        log_file = os.path.join(path, new_log_name)
    else:
        new_suffix = suffix.replace('.', ' ({0}).').format(log_version)
        new_log_name = f"{time_now} {log_name}{new_suffix}"
        log_file = os.path.join(path, new_log_name)
    try:
        # Ensure log path exists
        if not os.path.exists(path):
            update_workstation()
        # Get log size in MBs
        log_size = os.path.getsize(log_file) >> 20
        # Create new log file if current log size is greater than 1GB
        if log_size >= 1024:
            log_version += 1
            log_file = create_log_file(path, log_name, suffix, log_version)
    except FileNotFoundError:
        # Create new log file is now already exist
        with open(log_file, mode="a"):
            pass
    except Exception as e:
        logger.exception(f"{e} - Cannot create new log file")
    finally:
        return log_file


def update_logs(logger_name="SwumCloudManager", log_file="swum_cloud_manager"):
    """
    Creates new log file if the current log is too large. (greater than 1GB) or
    if the current date is different from when the current log was created.

    :param logger_name: the name of the logger which needs to be updated.
        creates a new logger if no logger with provider name exist.
        (default is 'SwumCloudManager')
    :param log_file: name of logging file.
    :type logger_name: str
    :type log_file: str

    :return: Logger - logging object with the requested name.

    """
    date_format = '%Y-%m-%d %H:%M'
    log_format = f'%(asctime)s {LOG_STR_FORMAT}'
    file_formatter = logging.Formatter(log_format, date_format)
    # Setup handler for debug logs
    debug_log_file = create_log_file(get_logs_folder(), log_file, "_debug.log")
    debug_handler = logging.FileHandler(debug_log_file)
    debug_handler.setFormatter(file_formatter)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.addFilter(FileLogFilter())
    # Setup handler for info logs
    info_log_file = create_log_file(get_logs_folder(), log_file, "_info.log")
    info_handler = logging.FileHandler(info_log_file)
    info_handler.setFormatter(file_formatter)
    info_handler.setLevel(logging.INFO)
    # Setup handler for error logs
    error_log_file = create_log_file(get_logs_folder(), log_file, "_error.log")
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setFormatter(file_formatter)
    error_handler.setLevel(logging.WARNING)
    # Add handlers to logger
    logging.basicConfig(format=log_format,
                        datefmt=date_format,
                        level=logging.DEBUG,
                        handlers=[console_handler, info_handler, error_handler, debug_handler],
                        force=True,
                        )
    new_logger = logging.getLogger(logger_name)

    return new_logger, debug_log_file


def get_credentials(password=""):
    if not password:
        password = os.getenv(SWUM_USER, "")

    return password


def get_user(username=""):
    if not username:
        username = os.getlogin()

    return username


def get_user_name():
    user = ""
    try:
        user_id = get_user().upper()
        user = USERS.get(user_id, "")
        if user:
            user = f" - {user}"
    except Exception as e:
        logger.exception(f"{e} - Cannot get user name.")
    finally:
        return user


def is_numeric(value):
    numeric = True
    try:
        int(value)
    except (ValueError, TypeError):
        numeric = False
    finally:
        return numeric


def is_official_file(part_number):
    official_file = True
    try:
        logger.debug(f"Checking file state for: {part_number}")
        if re.match(DEV_FILE_PATTERN, part_number):
            official_file = False
    except Exception as e:
        logger.exception(f"{e} - Cannot check if file is official.")
    finally:
        return official_file


def is_master_build(url):
    master_build = False
    try:
        if re.findall(MASTER_BUILD_PATTERN, url):
            master_build = True
    except Exception as e:
        logger.exception(f"{e} - Cannot check if master build.")
    finally:
        return master_build


def get_caller_info():
    caller_info = ""
    try:
        caller = inspect.currentframe().f_back.f_back
        caller = inspect.getframeinfo(caller)
        caller_info = f"{Path(caller[0]).name} -> {str(caller[2]).strip()}"
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve caller info!")
    finally:
        return caller_info


def find_caller():
    return get_caller_info()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.bool_):
            return super().encode(bool(obj))
        else:
            super().default(obj)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        object - (self) can be used to delete object after completing task

    error
        tuple (exctype, value, traceback.format_exc())

    result
        object data returned from processing, anything

    progress
        int indicating % progress
    updated
        indicates that the results was updated.
    """
    finished = pyqtSignal(object)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    updated = pyqtSignal()


class WorkerThread(Thread):
    """
    WorkerThread Inherits from Thread to handle worker thread setup
    """

    def __init__(self, fn, *args, **kwargs):
        """
         WorkerThread uses Thread to run any time-consuming tasks.

        :param fn: The function to run with the supplied args and kwargs.
        :type fn: function
        :param args: Arguments to pass to the function
        :type args: tuple
        :param kwargs: Keywords arguments to pass to the function
        :type kwargs: dict
        """
        Thread.__init__(self)
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.daemon = True

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            logger.debug(f"Starting task: {self.fn} on thread: '{self.name}'")
            result = self.fn(*self.args, **self.kwargs)
            logger.debug(f"Task {self.name} Complete! result={result}")
        except:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result when complete
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit(self)  # Done

    def stop(self):
        logger.debug(
            f"Stopping thread: {self.name} with id={self.native_id}"
        )
        retry_count = 0
        while self.is_alive() and retry_count < 3:
            pythonapi.PyThreadState_SetAsyncExc(
                c_long(self.native_id), py_object(SystemExit)
            )
            time.sleep(3)
            retry_count += 1
        self.signals.finished.emit(self)  # Done


class WorkerProcess(Process):
    """
    WorkerProcess - Inherits from Process to handle worker setup
    """

    def __init__(self):
        """
         WorkerThread uses Thread to run any time-consuming tasks.
        """
        super(WorkerProcess, self).__init__()
        self.daemon = True
        self.logger = logging.getLogger('WorkerProcess')
        self.logger.addHandler(null_handler)
        self.fn = None
        self.args = None
        self.kwargs = None
        self.results = {}
        self.tasks = {}

    def save_results(self, results):
        pass

    def add_task(self, name, fn, *args, **kwargs):
        """
         WorkerThread uses Thread to run any time-consuming tasks.

        :param fn: The function to run with the supplied args and kwargs.
        :type fn: function
        :param args: Arguments to pass to the function
        :type args: tuple
        :param kwargs: Keywords arguments to pass to the function
        :type kwargs: dict
        """
        task = WorkerThread(fn, *args, **kwargs)
        self.tasks[name] = task
        task.start()

    def run(self):
        self.logger.warning(f"Starting New Process: '{self.name}'")

    def stop(self):
        self.logger.warning(f"Stopping Process: {self.name} with id={self.pid}")
        # Stop threads
        for name in self.tasks:
            try:
                self.logger.warning(f"Stopping Thread: {name}...")
                thread = self.tasks[name]
                thread.stop()
            except Exception as e:
                self.logger.exception(
                    f"{e} - Cannot stop thread: {name}"
                )
        # Kill main process
        self.kill()


class PriorityQueue:
    """
    Create priority queue that is multiprocessing safe.
    """

    def __init__(self):
        self.queue = {}
        self.level_name = "LEVEL_{0}"
        self.level_idx = "_NEXT_IDX"
        self.level_size = "_SIZE"
        self.size = 0
        self.next = 0
        self.max = 0

    def get(self):
        """
        Get next item in queue or raise IndexError if queue is empty.
        """
        if self.empty():
            raise IndexError("Queue is Empty.")
        value = None
        # Get next item with the low priority index
        while self.next <= self.max:
            item = self.queue.get(self.next)
            if item is None:
                self.next += 1
                continue
            try:
                # Check if multiple items exist with same priority
                idx = item[self.level_idx]
                key = self.level_name.format(idx)
                value = item[key]
                if item[self.level_size] > 1:
                    # Update next priority level item and remove first item
                    self.queue[self.next][self.level_idx] += 1
                    self.queue[self.next][self.level_size] -= 1
                    del self.queue[self.next][key]
                else:
                    # Remove final item with same priority level
                    del self.queue[self.next]
                    self.next += 1
                break
            except:
                # Remove and return next item in queue
                value = item
                del self.queue[self.next]
                self.next += 1
                break
            finally:
                self.size -= 1
        # Reset values after last item is removed from queue
        if self.size < 1:
            self.next = 0
            self.max = 0

        return value

    def put(self, item, priority):
        """
        Add item to priority queue

        :param item: object to add to queue(str, dict, int, float, etc...)
        :param priority: int value representing the priority level
        :type priority: int
        """
        self.next = min(self.next, priority)  # update next priority item
        self.max = max(self.max, priority)  # Update max priority level
        self.size += 1  # increment queue
        # Check if item already exist with same priority
        value = self.queue.get(priority)
        if value is not None:
            try:
                # Check if multiple item exist with same priority
                idx = value[self.level_size]
                key = self.level_name.format(idx)
                idx += 1
                # Add new item with same priority
                self.queue[priority].update({key: item, self.level_size: idx})
            except:
                # Add new item with same priority
                key1 = self.level_name.format(0)
                key2 = self.level_name.format(1)
                self.queue[priority] = {
                    key1: value,
                    key2: item,
                    self.level_size: 2,
                    self.level_idx: 0
                }
        else:
            # Add new item to queue
            self.queue[priority] = item

    def empty(self):
        if self.size < 1:
            return True
        else:
            return False


class FileLogFilter(Filter):
    def __init__(self):
        super(FileLogFilter, self).__init__()

    def filter(self, record: LogRecord) -> bool:
        global last_gui_log
        # Edit logging from requests_oauthlib module
        if record.pathname.find("requests_oauthlib") >= 0:
            if isinstance(record.args, dict) and record.args.get('files'):
                record.msg = "Log Removed! - File Bytes Too Large."

        return True


def create_task(fn, callback, *args, **kwargs):
    """
    Create a task for specified function and calls the callback function with
    the results when complete.
    """
    logger.debug(
        f"Create task for: {fn} with args={args} & kwargs={kwargs}, "
        f"callback={callback}"
    )
    worker = WorkerThread(fn, *args, **kwargs)
    worker.start()
    if callable(callback):
        # Call the callback function with results when complete.
        worker.signals.result.connect(callback)
    else:
        logger.debug(f"No callback function provided for: {fn}")

    return worker


def save_function_calls(name, args, return_value):
    results = {
        name: {
            'args': args, 'return_value': return_value
        }
    }
    logger.warning(f"New Function Call: {results}")


def dns_server_lookup():
    """
    Get the name of the server that handles network requests

    Returns
    -------
    str
        Name of server. i.e: 'name.of.server.com'
    """
    server = ""
    try:
        results = subprocess.getoutput('nslookup google.com').lower()
        for item in results.split('\n'):
            if 'server' in item:
                server = str(item.split(":")[1]).strip()
    except IndexError as e:
        logger.exception(e)
    finally:
        return server


def get_proxy_server():
    proxy = ""
    server = dns_server_lookup()
    if "internal" in server:
        proxy = cfg.env.get("PROXY")

    return proxy


def enable_global_proxy():
    try:
        sys.path.append(ROOT_DIR)
        proxy = get_proxy_server()
        logger.debug(f"Setting Global Proxy: {proxy}")
        for key in PROXY_ENV:
            os.environ[key] = proxy
    except Exception as e:
        logger.exception(f"{e} - Cannot set global proxy.")


def disable_global_proxy():
    try:
        logger.debug(f"Removing Global Proxy...")
        for key in PROXY_ENV:
            os.environ[key] = ""
    except Exception as e:
        logger.exception(f"{e} - Cannot remove global proxy.")


def is_internet_connected(url='http://www.google.com/', timeout=3):
    try:
        proxy = get_proxy_server()
        proxies = {"https": proxy, "http": proxy}
        r = requests.head(url, timeout=timeout, proxies=proxies)
        print(r.text)
        return True
    except Exception as e:
        logger.error(repr(e))
        return False


def get_ip_address(timeout=3):
    ip_address = ""
    try:
        proxy = get_proxy_server()
        proxies = {"https": proxy, "http": proxy}
        resp = requests.get(IP_API, timeout=timeout, proxies=proxies)
        ip_address = resp.content.decode('utf-8')
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve ip address.")
    finally:
        return ip_address


def merge_dictionary(dict_one, dict_two):
    results = {}
    if isinstance(dict_one, dict) and not isinstance(dict_two, dict):
        return dict_one
    if isinstance(dict_two, dict) and not isinstance(dict_one, dict):
        return dict_two
    try:
        new_keys = set(dict_two.keys()).difference(dict_one.keys())
        for key in dict_one:
            value_one = dict_one[key]
            value_two = dict_two.get(key)
            if isinstance(value_one, dict) and isinstance(value_two, dict):
                results[key] = merge_dictionary(value_one, value_two)
            else:
                try:
                    results[key] = deepcopy(value_one)
                except TypeError:
                    results[key] = value_one
                # Replace existing value with value from second dictionary
                if value_two is not None:
                    try:
                        results[key] = deepcopy(value_two)
                    except TypeError:
                        results[key] = value_two
        for key in new_keys:
            try:
                results[key] = deepcopy(dict_two[key])
            except TypeError:
                results[key] = dict_two[key]
    except Exception as e:
        logger.exception(f"{e} - Cannot merge dictionaries: {dict_one} & {dict_two}")
    return results


"""
args as key/value pair:
'inspect.currentframe().f_locals' or 'vars()'

(Pdb) inspect.currentframe().f_locals
{'url': 'https://mail.google.com/', 'timeout': 3, 'proxy': 'http://internet.ford.com:83', 'proxies': {'https': 'http://internet.ford.com:83', 'http': 'http://internet.ford.com:83'}, 'r': <Response [301]>, '__return__': True}
connected = is_internet_connected("https://mail.google.com/")
print(f"connected: {connected}")
"""


def get_keyword_args(string_value, kwargs):
    pattern = "{([a-zA-Z0-9]+)}"
    args = re.findall(pattern, string_value)

    keywords = {x: kwargs.get(x) for x in args}
    print(f"string_value={string_value}, & keywords={keywords}")

    return keywords


def update_url_build_number(build_number, url):
    # Update url build number
    for form in URL_FORMS:
        url = str(url).replace(form, build_number)
    return url


def get_system_settings(file_name=None):
    system_setting = DEFAULT_SETTINGS
    try:
        logger.debug(f"Loading system settings for: {file_name}")
        if not file_name:
            file_name = SYSTEM_SETTINGS_FILE
        system_setting = read_json(file_name)
    except Exception as e:
        logger.exception(f"{e} - Cannot import system setting.")
    finally:
        return system_setting


def update_system_setting(file_name, system_settings):
    # Save system settings to file
    logger.debug(f"Saving System Settings: {system_settings}")
    try:
        system_settings = json.dumps(
            system_settings, indent=4, cls=CustomJSONEncoder
        )
        write_to_file(file_name, system_settings)
    except Exception as e:
        logger.exception(f"{e} - Cannot save system setting.")


def get_supported_domain_instances():
    """
        Import domain instances grouping them by ECU e.g.
        {
            "ECG1": {...},
            "ECG2": {
                ECG2_PROD_U725_MY23_GAS_CP_ONLY: {...},
                ECG2_PROD_P702_MY23_BEV_CP_ONLY: {...}, ...
            },
        }
        """
    supported_domain_instances = {}
    try:
        system_setting = read_json(SYSTEM_SETTINGS_FILE)
        supported_domains = system_setting[SUPPORTED_DOMAIN_INSTANCES]
        for name in supported_domains:
            value = supported_domains[name]
            ecu = value[ECU]
            try:
                supported_domain_instances[ecu][name] = deepcopy(value)
            except KeyError:
                logger.debug(f"Adding new ecu={ecu}.")
                supported_domain_instances[ecu] = deepcopy({name: value})
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve supported domain instances")
    finally:
        return supported_domain_instances


def activate_supported_domain_instances():
    try:
        system_settings = get_system_settings()
        for name in system_settings[SUPPORTED_DOMAIN_INSTANCES]:
            domain = system_settings[SUPPORTED_DOMAIN_INSTANCES][name]
            """
            files = domain.get(FILES, [])
            if set(files) == {VMCU, CCPU}:
                logger.debug(f"AP & CP ONLY domain instances not yet supported. skipping...")
                continue
            """
            domain[STATUS] = ACTIVE
        update_system_setting(SYSTEM_SETTINGS_FILE, system_settings)
    except Exception as e:
        logger.exception(f"{e} - Cannot activate domain instances!")


def get_variant_high_low(variant):
    if re.findall(r"(8GB)", variant):
        style = "LOW_COST"
    else:
        style = "MID_HIGH"

    return style


def get_sync_variant_types(variants):
    def key(text):
        idx = str(text).find("-")
        text = text[idx + 1:]
        return text

    variant_types = {}
    try:
        groups = set()
        # Sort variants
        variants = sorted(variants, key=key)
        # Extract acronym from variants
        for variant in variants:
            start = str(variant).find("-")
            _type = variant[:start]
            description = variant[start + 1:]
            words = re.findall(r"([-]+|[A-Z]+[a-z]+)", description)
            size = len(description)
            remaining = deepcopy(size)
            description = [_type]
            count = len(words)
            hyphen = False
            group = []
            for word in words:
                if '-' in word:
                    hyphen = True
                    remaining -= 1
                    size = deepcopy(remaining)
                    if group:
                        description.append("".join(group))
                        group = []
                    continue
                if count < 2 or size < 8:
                    description.append(str(word).upper())
                else:
                    if hyphen:
                        if group:
                            name = "".join(group)
                            description.append(name)
                            group = []
                        if remaining >= 8:
                            name = str(word)[:3]
                        else:
                            name = word
                        description.append(str(name).upper())
                    else:
                        if len(group) < 1 and remaining < 8:
                            description.append(str(word).upper())
                            size = deepcopy(remaining)
                            remaining -= len(word)
                            hyphen = True
                            continue
                        group.append(str(word)[0])
                        name = "".join(group)
                        if name in groups:
                            description.append(name)
                            group = []
                remaining -= len(word)
            name = "".join(group)
            if name:
                description.append(name)
                groups.add(name)
            variant_types[variant] = "_".join(description)
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve variant types!")
    finally:
        return variant_types


def import_domain_instances():
    """
    Import domain instances grouping them by ECU -> BUILD -> VARIANT. e.g.
    {
        "ECG2": {
            "production": {
                "P702": {
                    ECG2_PROD_U725_MY23_GAS_CP_ONLY: {...},
                    ECG2_PROD_P702_MY23_BEV_CP_ONLY: {...}, ...
                }
        },
        "ECG1": {...}
    }
    """
    domain_instances = {}
    supported_ecu = []
    try:
        logger.debug("Importing domain instances from system settings...")
        system_setting = read_json(SYSTEM_SETTINGS_FILE)
        supported_domains = system_setting.get(SUPPORTED_DOMAIN_INSTANCES)
        for name in supported_domains:
            domain = supported_domains[name]
            ecu = domain[ECU]
            variant = domain[VARIANT]
            build = domain[BUILD]
            if ecu not in supported_ecu:
                domain_instances[ecu] = {build: {variant: {}}}
                supported_ecu.append(ecu)
            if build not in domain_instances[ecu]:
                domain_instances[ecu][build] = {variant: {}}
            try:
                domain_instances[ecu][build][variant].update({name: domain})
            except KeyError:
                domain_instances[ecu][build][variant] = {name: domain}
    except Exception as e:
        logger.exception(f"{e} - Cannot Import Domain Instances!")
    finally:
        return domain_instances


def import_ecu_apps():
    supported_ecu_apps = {}
    try:
        logger.debug(f"Importing apps from: {SYSTEM_SETTINGS_FILE}...")
        system_setting = read_json(SYSTEM_SETTINGS_FILE)
        supported_ecu_apps = system_setting.get(SUPPORTED_ECU_APPS, {})
    except Exception as e:
        logger.exception(f"{e} - Cannot import ecu apps!")
    finally:
        return supported_ecu_apps


def get_nexus_name(url, full_name=True):
    nexus_name = ""
    try:
        if str(url).find("www.nexus.ford.com") >= 0:
            logger.debug(f"Retrieving nexus name from nexus url={url}")
            info = extract_nexus_url_info(url)
            # Retrieve nexus name
            if full_name:
                nexus_name = info[NEXUS_NAME]
            else:
                nexus_name = str(info[NEXUS_NAME]).split('-')[-1]
        else:
            logger.debug(f"Retrieving nexus name from jenkins url={url}")
            start = str(url).rfind("job/") + len("job/")
            search_text = str(url)[start:]
            group = search_text.split('/')
            nexus_name = group[0]
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve nexus name from url={url}")
    finally:
        return nexus_name


def get_available_ecus(ecu_type):
    available_ecu_types = [ecu_type]
    for ecu in SUPPORTED_ECU_VERSIONS:
        if len(re.findall(ecu, ecu_type)) > 0:
            available_ecu_types = SUPPORTED_ECU_VERSIONS[ecu]
            break
    return available_ecu_types


def get_time_remaining(start_time):
    time_remaining = 0
    try:
        time_remaining = (start_time - time.time())
        if time_remaining > 0:
            time_remaining = int(time_remaining / 60)
    except Exception as e:
        logger.exception(f"{e} - Cannot get time remaining.")
    finally:
        return time_remaining


def get_domain_objects(domain_names):
    logger.debug(f"Retrieving domain objects for: {domain_names}")
    available_domain = get_supported_domain_instances()
    domain_instances = {}
    domain_objects = []
    try:
        for ecu in available_domain:
            domain_instances.update(available_domain[ecu])
        for name in domain_names:
            try:
                domain_settings = domain_instances[name]
                domain_instance = DomainInstance(domain_settings)
                domain_objects.append(domain_instance)
            except KeyError:
                logger.error(f"Cannot retrieve domain object for: {name}")
    except Exception as e:
        logger.exception(
            f"{e} - Cannot retrieve domain objects. {domain_instances}"
        )
    finally:
        return domain_objects


def get_ecu_from_ecu_type(ecu_type):
    ecu = ""
    try:
        if str(ecu_type).find(ECG) >= 0:
            ecu = ECG
        elif str(ecu_type).find(TCU) >= 0:
            ecu = TCU
        elif str(ecu_type).find(SYNC) >= 0:
            ecu = SYNC
        elif str(ecu_type).find(PHOENIX) >= 0:
            ecu = PHOENIX
        else:
            logger.error(f"Cannot Retrieve ECG with type={ecu_type}")
    except Exception as e:
        logger.exception(f"{e} - Cannot Extract ECU From ECU Type!")
    finally:
        return ecu


def verify_build_type(ecu, build_type, url):
    match = False
    try:
        # Verify build type matches url
        build_type_pattern = URL_PATTERN_BUILD_TYPE[ecu][build_type]
        if re.findall(build_type_pattern, url):
            match = True
    except Exception as e:
        logger.exception(f"{e} - Cannot verify build type!")
    finally:
        return match


def verify_ecu_type(ecu, url):
    match = False
    try:
        # Verify ecu type matches url
        ecu_pattern = URL_PATTERN_ECU_TYPE[ecu]
        if re.findall(ecu_pattern, url):
            match = True
    except Exception as e:
        logger.exception(f"{e} - Cannot verify ecu type!")
    finally:
        return match


def get_ecu_type_from_url(url):
    ecu = ""
    try:
        for ecu_type in URL_PATTERN_ECU_TYPE:
            pattern = URL_PATTERN_ECU_TYPE[ecu_type]
            match = re.search(pattern, url)
            if match:
                ecu = ecu_type
                break
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve ecu type from url.")
    finally:
        return ecu


def verify_url_exist(url, username, password):
    try:
        nexus = SwumNexus(username, password)
        with nexus.get_session() as nexus_session:
            response = nexus_session.head(url)
            if response.status_code in [200, 201]:
                exist = True
            else:
                logger.warning(f"status: {response.status_code}, resp: {response.text}")
                exist = False
    except Exception as e:
        logger.exception(f"{e} - Cannot verify if url exist.")
    finally:
        return exist, response


def is_valid_url(url, ecu=None, build_type=None, username=None, password=None):
    """
    Function to validate URL using regular expression.
    """
    # Check if string is empty
    valid = False
    reasons = []
    # Verify url is actually a string value
    if not isinstance(url, str):
        msg = f"Invalid URL! Expected : <class 'str'>. Received: {type(url)}\n"
        reasons.append(msg)
        logger.error(msg)
        return valid, "\n".join(reasons)
    # Bypass check for PR build urls
    if url.find("build.ford.com") > 0 and url.find("PR") > 0:
        msg = "Found PR Build URL!"
        reasons.append(msg)
        valid = True
        print(msg)
        return valid, ", ".join(reasons)
    # Validate build type matches url
    if ecu and build_type and not verify_build_type(ecu, build_type, url):
        msg = f"Build='{build_type}' Do Not Match URL"
        reasons.append(msg)
    # Validate ecu type matches url
    if ecu and not verify_ecu_type(ecu, url):
        msg = f"ECU='{ecu}' Do Not Match URL"
        reasons.append(msg)
    # Regex to check valid URL
    match = re.search(VALID_URL_PATTERN, url)
    if match:
        valid = True
    else:
        msg = "Invalid URL Format"
        reasons.append(msg)
        valid = False
    # Verify path to url exist
    if username and password:
        if ecu == SYNC:
            # Format url for latest master
            status, build = get_latest_build_number(url, username, password)
            if status:
                url = update_url_build_number(build, url)
        valid, response = verify_url_exist(url, username, password)
        if not valid:
            reasons.append(response)

    return valid, ", ".join(reasons)


def authenticate_user(username, password):
    logger.debug(f"Authenticating User... {username}")
    reason = f"NetworkError - Cannot Authenticate User!"
    verified = False
    try:
        nexus = SwumNexus(username, password)
        session = nexus.get_session()
        response = session.head(NEXUS_REPOSITORY_URL, timeout=5)
        if response.status_code in [200, 201]:
            verified = True
            reason = f"{username} Logged in Successfully!"
            logger.info(reason)
        else:
            logger.warning(response.text)
            if response.status_code == 403:
                reason = "Forbidden - Invalid Credentials!"
            elif response.status_code == 404:
                reason = "Not Found - Please update nexus url!"
            else:
                reason = "Bad Request - Invalid Credentials!"
    except Exception as e:
        reason = f"{e.args[0]} - Cannot Authenticate User!"
        logger.exception(reason)
    finally:
        return verified, reason


def get_html_page(url, username, password):
    html = ""
    try:
        logger.debug(f"Retrieving html page for url={url}")
        nexus = SwumNexus(username, password)
        nexus_session = nexus.get_session()
        retry = 3
        while retry > 0:
            with nexus_session as session:
                response = session.get(url)
                if response.status_code == 200:
                    html = response.text
                    break
                else:
                    print(f"Error retrieving html page! Retry in 3 sec...{url}")
                    time.sleep(3)
                retry -= 1
    except Exception as e:
        logger.exception(f"{e} - Cannot get html page!")
    finally:
        return html


def html_to_json(url, username, password):
    """
    :param url:
    :param username:
    :param password:
    :return:

    """
    results = dict()
    try:
        tables = []
        build_url = deepcopy(url)
        html = get_html_page(build_url, username, password)
        body = etree.HTML(html).find("body")
        title = "N/A"
        for element in body:
            if element.tag == 'h1':
                title = element.text
                continue
            elif element.tag == 'table':
                table = element
            else:
                # ignore all the other tags
                continue
            section = (title, table)
            tables.append(section)
        base_url = str(url).split('/')[:-1]
        for title, table in tables:
            links = {}
            record = []
            title = str(title).replace(PACKAGES, "").strip() or PACKAGES
            section = {title: list()}
            table_data = table.iter("td")
            headers = [th.text.lower().strip() for th in table.iter('th')]
            for row in table_data:
                text = row.text
                for link in row.iter('a'):
                    href = link.get('href', "")
                    name = link.text
                    full_url = deepcopy(base_url)
                    valid, reason = is_valid_url(href)
                    if not valid:
                        full_url.append(href)
                        href = "/".join(full_url)
                    links[name] = deepcopy(href)
                    if not text:
                        text = name
                parts = [row.iter('br')]
                if parts:
                    pattern = r"\(([0-9.]*)\)"
                    version_text = etree.tostring(row).decode()
                    version = re.findall(pattern, version_text)
                    if version:
                        text = version[0]
                record.append(text)
                if len(record) == len(headers):
                    data = dict(zip(headers, record))
                    data.update({LINKS: links})
                    section[title].append(data)
                    record = []
                    links = {}
            results.update(section)
            if len(record) > 0:
                print(f"Error - Extra Data Found: {record}")
    except Exception as e:
        print(f"{repr(e)} - Cannot parse json from html.")
    finally:
        return results


def get_url_type(url):
    url_type = ""
    try:
        for _type in list(URL_TYPES):
            pattern = URL_TYPES.get(_type)
            pattern = f"(?s)({'|'.join(pattern)})"
            if re.findall(pattern, str(url).lower(), flags=re.IGNORECASE):
                url_type = _type
                break
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve url type.")

    return url_type


def is_jenkins_url(url):
    is_jenkins = False
    try:
        pattern = f"({'|'.join(JENKINS_PATTERN)})"
        if len(re.findall(pattern, str(url).lower())) > 0:
            is_jenkins = True
    except Exception as e:
        logger.exception(f"{e} - Cannot check if jenkins URL.")
    finally:
        return is_jenkins


def get_manifest_type(manifest):
    manifest_type = ""
    try:
        if manifest.get(FILES) or manifest.get(ASSEMBLIES):
            manifest_type = JSON
        else:
            manifest_type = HTML
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve url type.")

    return manifest_type


def select_phoenix_assembly(manifest, artifact_name=None):
    """
    Retrieve the phoenix assembly for the specified artifact.

    :param manifest: Phoenix manifest json
    :param artifact_name: artifact name from nexus. e.g. 'supplement_VBF_XBF_artifact'
    :type manifest: dict
    :type artifact_name: str

    :return: assembly with list of artifacts for the specified artifact name.

    """
    logger.debug(f"Selecting phoenix artifact for: {artifact_name}")
    assembly = []
    try:
        if ASSEMBLIES in manifest.keys():
            logger.debug(f"Extracting Phoenix JSON assembly...")
            if artifact_name:
                for package in manifest[ASSEMBLIES]:
                    assembly = package.get(artifact_name, [])
                    if assembly:
                        break
            else:
                assembly = manifest[ASSEMBLIES]
        else:
            logger.debug(f"Extracting Phoenix HTML assembly...")
            assembly = manifest.get(artifact_name, [])
    except Exception as e:
        logger.exception(f"{e}- Cannot retrieve artifact for: {artifact_name}")
        logger.debug(f"phoenix manifest: {manifest}")
    finally:
        return assembly


def extract_phoenix_artifact(manifest, artifact, artifact_id):
    """
    Extract assembly with selected file artifact id.

    :param manifest: Jenkins manifest with Nexus artifacts.
    :param artifact: name of package from which to extract artifact files.
    :param artifact_id: regex pattern to match artifact id.
    :type manifest: dict
    :type artifact: str
    :type artifact_id: str

    :return: dictionary with assembly that matches artifact id.
    """
    logger.debug(f"Extracting phoenix assembly for: {artifact} & artifact_id={artifact_id}")
    results = {}
    assemblies = []
    try:
        assemblies = select_phoenix_assembly(manifest, artifact)
        for assembly in assemblies:
            if re.match(artifact_id, assembly[NEXUS_ARTIFACT_ID]):
                results = assembly
                break
    except Exception as e:
        logger.exception(f"{e} - Cannot extract phoenix assembly.")
        logger.debug(f"assemblies={assemblies}")
    finally:
        return results


def extract_phoenix_artifact_html(manifest, artifact, artifact_id):
    """
    Extract assembly with selected file artifact id.

    :param manifest: Jenkins manifest with Nexus artifacts.
    :param artifact: name of package from which to extract artifact files.
    :param artifact_id: regex pattern to match artifact id.
    :type manifest: dict
    :type artifact: str
    :type artifact_id: str

    :return: dictionary with assembly that matches artifact id.
    """
    logger.debug(f"Extracting phoenix html assembly for :{artifact} & artifact_id:{artifact_id}")
    new_artifact = {}
    try:
        for assembly in manifest[artifact]:
            file = assembly[FILE]
            nexus_url = assembly[LINKS][file]
            assembly = extract_nexus_url_info(nexus_url)
            assembly.update({NEXUS_URL: nexus_url})
            if re.match(artifact_id, assembly[NEXUS_ARTIFACT_ID]):
                new_artifact = assembly
                break
            else:
                logger.debug(f"Skipping artifact_id: {assembly[NEXUS_ARTIFACT_ID]}...")
    except Exception as e:
        logger.exception(f"{e} - Cannot extract html phoenix assembly.")
        logger.debug(f"Phoenix manifest: {manifest}")
    finally:
        return new_artifact


def get_phoenix_artifact(manifest, artifact_name, artifact_id):
    artifact = {}
    try:
        manifest_type, url_type = get_phoenix_manifest_type(manifest)
        if url_type == JSON:
            artifact = extract_phoenix_artifact(manifest, artifact_name, artifact_id)
        elif url_type == HTML:
            artifact = extract_phoenix_artifact_html(manifest, artifact_name, artifact_id)
        else:
            msg = f"url_type={url_type} Not Supported!"
            raise NotImplementedError(msg)
    except Exception as e:
        logger.exception(f"{e} - Cannot select phoenix assembly.")
    finally:
        return artifact


def get_sync_package(manifest, package_name):
    """
    :param manifest: sync manifest json
    :param package_name: package name from jenkins '32GB-NorthAmerica',
        '32GB-RestOfWorld', etc...

    :return: dictionary with package information.

    """
    logger.debug(
        f"Retrieving sync package for: {package_name}"
    )
    results = {}
    try:
        for package in manifest['assemblies']:
            description = package['description']
            if package_name == description:
                logger.info(
                    f"Extracting sync artifact for: {package_name}"
                )
                results = package
                break
    except Exception as e:
        logger.exception(f"{e}- Cannot retrieve package")
    finally:
        return results


def get_sync_artifact(manifest, package_name, artifact):
    """

    :param manifest: sync manifest json
    :param package_name: package name from jenkins '32GB-NorthAmerica',
        '32GB-RestOfWorld', etc...
    :param artifact: name of artifact to retrieve.

    :return: dictionary with package artifact information.

    """
    logger.debug(
        f"Retrieving artifact: {artifact} for: {package_name}"
    )
    try:
        return get_sync_package(manifest, package_name)[artifact]
    except Exception as e:
        logger.exception(f"{e}- Cannot retrieve artifact: {artifact}")


def extract_sync_assembly_html(assemblies, file_description):
    """
    Extract assembly with selected file description and file extension.
    :param assemblies: dictionary or list of assemblies from jenkins manifest.
    :param file_description: description of file to search for.
    :return: if success - dictionary with assembly that matches file description and file extension.
             if failure - {}
    """
    logger.debug("Extracting html sync assembly...")
    new_assembly = {}
    if not file_description:
        logger.critical(f"Invalid file_description={file_description}")
        return new_assembly
    if not assemblies:
        logger.critical(f"Invalid assemblies={assemblies}")
        return new_assembly
    try:
        for assembly in assemblies:
            description = str(assembly.get(DESCRIPTION))
            if description.find(file_description) >= 0:
                logger.debug(f"Found assembly for: {description}")
                version = str(assembly.get(VERSION, ""))
                links = assembly.get(LINKS, {})
                file = assembly.get(NAME, "")
                nexus_url = links.get(file)
                nexus_extension = str(file).split('.')[-1]
                if version and version.find('(') > 0:
                    part_number, version = str(version).split('(')
                    version = str(version).replace(")", "")
                else:
                    version = None
                    parts = str(file).split('-')[:4]
                    part_number = "-".join(parts[:3])
                    suffix = str(parts[-1])
                    if part_number.find(suffix) < 1 and is_numeric(suffix):
                        add_suffix = True
                    else:
                        add_suffix = False
                    if add_suffix or 'local' in parts:
                        part_number += suffix
                new_assembly[FILE] = file
                new_assembly[NEXUS_NAME] = description
                new_assembly[NEXUS_VERSION] = version
                new_assembly[NEXUS_EXTENSION] = nexus_extension
                new_assembly[NEXUS_URL] = nexus_url
                new_assembly[FPN] = part_number
                break
        if not new_assembly:
            logger.error(f"Cannot retrieve sync assembly for file={file_description} from assemblies={assemblies}")
    except Exception as e:
        logger.exception(f"{e} - Cannot extreact sync html assembly!")
    finally:
        return new_assembly


def get_sync_manifest_variants(manifest):
    variants = set()
    try:
        if not manifest:
            msg = "Invalid SYNC Manifest"
            raise ValueError(msg)
        try:
            assemblies = manifest[ASSEMBLIES]
            logger.debug(f"Using SYNC JSON manifest...")
            for assembly in assemblies:
                variant = assembly[DESCRIPTION]
                variants.add(variant)
        except KeyError:
            assemblies = manifest[ASSEMBLIES.capitalize()]
            logger.debug(f"Using SYNC HTML manifest...")
            for assembly in assemblies:
                variant = assembly[DESCRIPTION]
                variants.add(variant)
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve manifest variants!")
    finally:
        return list(variants)


def get_phoenix_manifest_variants(manifest):
    variants = set()
    try:
        if not manifest:
            msg = "Invalid SYNC Manifest"
            raise ValueError(msg)
        try:
            assemblies = manifest[ASSEMBLIES]
            logger.debug(f"Using PHOENIX JSON manifest...")
            for assembly in assemblies:
                variant = assembly[NEXUS_ARTIFACT_ID]
                variants.add(variant)
        except KeyError:
            logger.debug(f"Using PHOENIX HTML manifest...")
            for variant in manifest:
                variants.add(variant)
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve manifest variants!")
    finally:
        return list(variants)


def get_nexus_url(ecu, manifest, variant=None, artifact_id=None):
    """
    summary: Retrieves the nexus url from the provided manifest object.

    Parameters
    ----------
    ecu: can be any of the following: [ECG, TCU, SYNC, PHOENIX]
    manifest: dictionary object with build information
    variant: str
        Can be any of the following: ['8GB-LowCost', '32GB-NorthAmerica',
        '16GB-RestOfWorld', '32GB-Europe', 'PHOENIX/phx-fsb VIP', 'PHOENIX/phx-fsb VBF/XBF', ...]
    artifact_id: str
        nexus artifact id of the desired artifact. e.g. 'AAA_Readme'

    Returns
    -------
    str
        the nexus url from the jenkins manifest for the current selected build.
    """
    nexus_url = ""
    try:
        file_settings = VadrConfig.FILE_SETTINGS
        logger.debug(f"Retrieving nexus url for variant={variant} & artifact_id={artifact_id}")
        if not manifest:
            logger.critical(
                f"Cannot retrieve nexus url! Invalid manifest={manifest}"
            )
            return nexus_url
        if ecu in [ECG, ECG1, ECG2, TCU, TCU1, TCU2]:
            assembly = deepcopy(manifest['files'][0])
            nexus_url = assembly.get(NEXUS_URL, "")
        elif ecu == SYNC:
            if variant is None:
                variant = get_sync_manifest_variants(manifest)[0]
                logger.debug(f"Using default sync variant: {variant}...")
            try:
                assembly = manifest[ASSEMBLIES]
                logger.debug(f"Extracting sync url from JSON Manifest...")
                assembly = get_sync_package(manifest, variant)
                nexus_url = assembly.get(NEXUS_URL, "")
            except KeyError:
                assemblies = manifest[ASSEMBLIES.capitalize()]
                logger.debug(f"Extracting sync url from HTML Manifest...")
                assembly = extract_sync_assembly_html(
                    assemblies, variant
                )
                nexus_url = assembly.get(NEXUS_URL, "")
        elif ecu == PHOENIX:
            if variant is None or artifact_id is None:
                manifest_type, url_type = get_phoenix_manifest_type(manifest)
                info = file_settings[PHOENIX][NEXUS_URL][url_type][manifest_type]
                artifact_id = info[NEXUS_ARTIFACT_ID]
                variant = info[VARIANT]
                logger.warning(f"Using default variant={variant} & artifact_id={artifact_id}...")
            if manifest.get(ASSEMBLIES):
                logger.debug(f"Extracting phoenix url from JSON Manifest...")
                artifact = extract_phoenix_artifact(manifest, variant, artifact_id)
                nexus_url = artifact.get(NEXUS_URL, "")
                if not nexus_url:
                    logger.critical(f"Cannot retrieve nexus url from artifact: {artifact}")
            else:
                logger.debug(f"Extracting phoenix url from HTML Manifest...")
                artifact = extract_phoenix_artifact_html(manifest, variant, artifact_id)
                nexus_url = artifact.get(NEXUS_URL, "")
                if not nexus_url:
                    logger.critical(f"Cannot retrieve nexus url from artifact: {artifact}")
        else:
            logger.critical(
                f"Cannot retrieve nexus url! {ecu} Not Supported!"
            )
        logger.debug(f"Found nexus url: {nexus_url}")
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve nexus url for: {ecu}!")
        logger.debug(f"manifest={manifest}\n\n")
    finally:
        return nexus_url


def clean_workstation(all_files=False):
    logger.info("Cleaning Up Workstation...")
    exclude_files = [PENDING_UPLOADS, "logs", ".xlsx"]
    for file in Path(get_workstation()).iterdir():
        try:
            if all_files:
                if file.is_dir():
                    # Do Not Delete Special DIR
                    if file.name in exclude_files:
                        continue
                    logger.info(f'Deleting.. "{file}"')
                    rmtree(file)
                else:
                    # Do Not Delete Excel Files
                    if file.suffix in exclude_files:
                        continue
                    logger.info(f"Deleting... '{file.name}'")
                    os.remove(file)
            else:
                if file.is_dir() and file.name not in exclude_files:
                    rmtree(file)
                    logger.info(f'Deleting.. "{file}"')
        except (PermissionError, OSError) as e:
            logger.debug(f"{repr(e)} while deleting: {file.name}")


def read_zip_file(file):
    """
    Extract zip files to the specified destination.
    :param file: full path to zip file.

    :return: destination path to extracted files.
    """
    results = {}
    try:
        if is_zipfile(file):
            with ZipFile(file, 'r') as zip_file:
                logger.info(f"Reading zip file: {file} ...")
                try:
                    file_list = zip_file.filelist
                    results["FILE_LIST"] = deepcopy(file_list)
                except PermissionError:
                    logger.exception("Permission Error!")
        else:
            logger.error(f"{file} is Not a ZipFile")
    except Exception as e:
        logger.exception(f"{e} - Cannot read zip file!")
    finally:
        return results


def extract_zip_file(file_name, destination="", clean_station=True):
    """
    Extract zip files to the specified destination.
    :param file_name: name of file to extract
    :param destination: destination path to extract files.
    :param clean_station: True or False - Delete files in destination folder before extraction new files.
    :return: destination path to extracted files.
    """
    try:
        if clean_station:
            clean_workstation()
        if os.path.exists(file_name):
            if not destination:
                destination = str(Path(file_name).parent)
            path, name = os.path.split(file_name)
            if is_zipfile(file_name):
                with ZipFile(file_name) as file:
                    logger.info(f"Extracting {name} ...")
                    try:
                        file.extractall(destination)
                    except PermissionError:
                        logger.exception("Permission Error!")
            else:
                logger.error(f"{name} is Not a ZipFile")
        else:
            logger.error(f"Zipfile: {file_name} Not Found!")
    except Exception as e:
        logger.exception(f"{e} - Cannot extract zip file!")
    finally:
        return destination


def extract_tar_file(file_name, destination="", clean_station=True):
    """
    Extract tar.gz files to the specified destination.
    :param file_name: name of file to extract
    :param destination: destination path to extract files.
    :param clean_station: True or False - Delete files in destination folder before extraction new files.
    :return: destination path to extracted files.
    """
    files = []
    try:
        logger.debug(f"Extracting tar file: {file_name}")
        if clean_station:
            clean_workstation()
        if os.path.exists(file_name):
            path, name = os.path.split(file_name)
            if not destination:
                destination = str(Path(file_name).parent)
            if str(file_name).endswith("tar.gz"):
                logger.info(f"Extracting {name}...")
                with TarFile.open(file_name, "r:gz") as tar:
                    try:
                        tar.extractall(destination)
                        files = [os.path.join(destination, x.name) for x in tar.getmembers()]
                    except PermissionError:
                        logger.critical(
                            f"Permission Error: {traceback.format_exc()}"
                        )
            else:
                logger.info(f"Extracting {name}...")
                with TarFile.open(file_name, "r") as tar:
                    try:
                        tar.extractall(destination)
                        files = [os.path.join(destination, x.name) for x in tar.getmembers()]
                    except PermissionError:
                        logger.critical(
                            f"Permission Error: {traceback.format_exc()}")
        else:
            logger.error(f"Tarfile: {str(file_name)} Not Found!")
    except Exception as e:
        logger.exception(f"{e} Cannot extract tar file!")
    finally:
        return files


def extract_nexus_artifact(nexus_url, username, password):
    path = ""
    try:
        nexus = SwumNexus(username, password)
        jenkins_file_name = nexus_url.split('/')[-1]
        ecu_bundle = os.path.join(get_workstation(), jenkins_file_name)
        if not os.path.exists(ecu_bundle):
            logger.info(f"Downloading... {jenkins_file_name}")
            ecu_bundle = nexus.attempt_nexus_download(
                nexus_url, get_workstation(), jenkins_file_name
            )
        # Extract files
        if is_zipfile(ecu_bundle):
            path = extract_zip_file(ecu_bundle)
        elif ".tar" in ecu_bundle or ".gz" in ecu_bundle:
            path = extract_tar_file(ecu_bundle)
    except Exception as e:
        logger.exception(f"{e} - Cannot download sync files")
    finally:
        return path


def extract_nexus_url_info(nexus_url):
    """
    Extract nexus artifact info from url. can be used to generate new url.

    :param nexus_url: Nexus url from which to extract info.
    :return: dictionary with Nexus artifact info.
    """
    nexus_info = dict()
    try:
        base, parts = str(nexus_url).split(f"{NexusConfig.NEXUS_URL}/")
        parts = str(parts).split('/')
        file = parts.pop(len(parts) - 1)
        nexus_version = parts.pop(len(parts) - 1)
        nexus_artifactid = parts.pop(len(parts) - 1)
        nexus_fetch_repository = parts.pop(0)
        groupid = ".".join(parts)
        if str(parts[0]).find('sync4') >= 0:
            parts.pop(0)
        if str(groupid).find(nexus_artifactid) > 0:
            nexus_name = ".".join(parts[3:])
        else:
            if str(nexus_version).find('-') > 0:
                parts = str(nexus_version).split('-')
                if len(parts) > 10:
                    nexus_name = "-".join(parts[3:-3])
                elif len(parts) > 5:
                    nexus_name = "-".join(parts[1:-3])
                else:
                    nexus_name = "-".join(parts[1:])
            else:
                nexus_name = "-".join(parts[3:])
                if nexus_name.find('-') < 1:
                    nexus_name = nexus_artifactid
        nexus_info.update({
            FILE: file,
            GROUP_ID: groupid,
            NEXUS_FETCH_REPOSITORY: nexus_fetch_repository,
            NEXUS_ARTIFACT_ID: nexus_artifactid,
            NEXUS_VERSION: nexus_version,
            NEXUS_NAME: nexus_name
        })
    except Exception as e:
        logger.exception(f"{e} - Cannot extract nexus info!")
    finally:
        return nexus_info


def build_nexus_url(build, artifact):
    """
    Builds nexus url from artifact info

    :param build: Can be any of the following: [production, development]
    :type build: str
    :param artifact: dictionary with sync artifact info
    :type artifact: dict

    :return: nexus url
    """
    logger.debug(f"building nexus url for build={build} from \nartifact={artifact}")
    nexus_url = ""
    try:
        key = 'nexus_fetch_repository'
        base_url = NexusConfig.NEXUS_URL
        nexus_fetch_repository = NexusConfig.NEXUS_REPOSITORIES[build]
        nexus_fetch_repository = artifact.get(key, nexus_fetch_repository)
        file = artifact[FILE]
        if 'tar' in file:
            start = str(file).find('.')
            nexus_extension = file[start:]
        else:
            nexus_extension = f".{file.split('.')[-1]}"
        artifact_id = artifact[NEXUS_ARTIFACT_ID]
        nexus_version = artifact[NEXUS_VERSION]
        nexus_group = artifact[GROUP_ID]
        build_artifact = f"{artifact_id}-{nexus_version}{nexus_extension}"
        nexus_info = [base_url, nexus_fetch_repository]
        nexus_info.extend(nexus_group.split('.'))
        nexus_info.append(artifact_id)
        nexus_info.append(nexus_version)
        nexus_info.append(build_artifact)
        nexus_url = "/".join(nexus_info)
    except Exception as e:
        logger.exception(f"{e} - Cannot build nexus url.")
    finally:
        return nexus_url


def get_phoenix_manifest_type(manifest):
    manifest_type = ""
    url_type = ""
    try:
        group_id = manifest.get(GROUP_ID)
        if group_id:
            url_type = JSON
            if str(group_id).lower().find('aosp') > 0:
                manifest_type = AOS_NEXUS
            else:
                manifest_type = PHX_NEXUS
        else:
            url_type = HTML
            variants = get_phoenix_manifest_variants(manifest)
            if 'PHX-AOSP/manifest Artifacts' in variants:
                manifest_type = AOS_NEXUS
            else:
                manifest_type = PHX_NEXUS
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve url type.")
    finally:
        return manifest_type, url_type


def get_build_type_from_manifest(ecu, manifest):
    build_type = ""
    try:
        if ecu == SYNC:
            try:
                assembly = manifest[ASSEMBLIES][0]
                artifact_version = assembly[ARTIFACT_VERSION]
            except KeyError:
                assembly = manifest[ASSEMBLIES.capitalize()][0]
                artifact_version = assembly[VERSION]
            if str(artifact_version).find("PRODUCT") > 0:
                build_type = PRODUCTION
            else:
                build_type = DEVELOPMENT
        else:
            logger.warning(f"Get build type for ecu={ecu} not supported!")
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve build type from manifest")
    finally:
        return build_type


def json_url_to_html(url):
    html = "AAA_Readme.html"
    json = "sync_manifest.json"
    new_url = str(url).replace(json, html)

    return new_url


def get_vbf_file_version(url, username, password):
    nexus = SwumNexus(username, password)
    nexus_session = nexus.get_session()
    with nexus_session as session:
        response = session.get(url)
        text = response.text

    return text


# TO DO - Update or Delete (duplicate)
def get_file_logger(logger_name, log_version=None, log_level=logging.DEBUG):
    time_now = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    if log_version is not None:
        log_name = f"{time_now} {logger_name} ({log_version}).log"
    else:
        log_name = f"{time_now} {logger_name}.log"
    log_file = os.path.join(get_logs_folder(), log_name)
    log_format = f'%(asctime)s {LOG_STR_FORMAT}'
    date_format = '%Y-%m-%d %H:%M'
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    # Create new logger
    new_logger = logging.getLogger(logger_name)
    new_logger.addHandler(file_handler)
    try:
        os.path.getsize(log_file) >> 20
    except FileNotFoundError:
        # Create new logging file if not already exist
        with open(log_file, mode="a"):
            os.path.getsize(log_file) >> 20

    return new_logger


def read_file(file_name):
    results = ""
    try:
        with open(file_name, "r") as file:
            results = file.read()
    except Exception as e:
        logger.exception(f"{e} - Cannot read file={file_name}")

    return results


def read_json(file_name):
    data = {}
    try:
        data = json.loads(read_file(file_name))
    except Exception as e:
        logger.exception(f"{e} - Cannot read json file={file_name}")
    finally:
        return data


def read_file_data(file_name):
    results = ""
    try:
        with open(file_name, "r") as file:
            data = file.read()
            results = ast.literal_eval(data)
    except ValueError:
        results = data
    except Exception as e:
        logger.exception(f"{e} - Cannot read file={file_name}")

    return results


def extract_test_name(*args, **kwargs):
    name = ",".join([str(x) for x in args])
    name = f"{name}{''.join([str(x) for x in kwargs.values()])}"
    return name


def update_testing_data(key, value):
    """
    Add the specified key and value pair to test_dataset.json
    """
    dataset = read_json(TEST_DATASET_FILE)
    dataset = merge_dictionary(dataset, {key: value})
    dataset = json.dumps(dataset, indent=4, cls=CustomJSONEncoder)
    write_to_file(TEST_DATASET_FILE, dataset)


def write_to_file(file_name, data):
    results = False
    try:
        with open(file_name, "w+") as file:
            file.write(data)
            results = True
    except Exception as e:
        logger.exception(
            f"{e} - Cannot write data to file={file_name}, data={data}"
        )

    return results


def get_latest_owner_guide(owner_guides):
    """
    Get the correct owner guide from the list of available guides.

    Parameters
    ----------
    owner_guides: set
        set of available owners guides

    Returns
    -------
    str:
        if SUCCESS - the latest owner guide.
        if FAILURE - empty string

    """
    best_idx = 0
    selected = ""
    for guide in owner_guides:
        if guide not in OWNER_GUIDE_LINEAGE:
            continue
        idx = OWNER_GUIDE_LINEAGE.index(guide)
        if idx >= best_idx:
            best_idx = idx
            selected = OWNER_GUIDE_LINEAGE[best_idx]

    return selected


def remove_file(file_list, file_name):
    try:
        file_list.remove(file_name)
    except (ValueError, AttributeError):
        pass
    finally:
        return file_list


def install_mongo_db_server():
    try:
        db_server_installed = cfg.env.get('MONGO_DB_INSTALLED')
        if db_server_installed:
            logger.debug("MongoDB Server Already Installed.")
            return True
        # Check installed application list
        file_name = str(MONGO_DB_SERVER_EXE).split('/')[-1]
        full_name = os.path.join(get_workstation(), file_name)
        server_version = file_name.split('-')
        server_version = f"MongoDB {server_version[-2]}"
        logger.info("Checking for MongoDB Server...")
        installed_apps = str(subprocess.check_output(['wmic', 'product', 'get', 'name']))
        if re.findall(server_version, installed_apps):
            logger.info(f"{server_version} Already Installed.")
            cfg.env.MONGO_DB_INSTALLED = True
            OmegaConf.save(cfg, CFG_FILE)
            return True
        # Prevent malicious files from being installed.
        if not file_name.startswith('mongodb'):
            logger.critical(f"Unrecognized MongoDB Installation File={file_name}")
            return False
        # Download the latest mongoDB server
        proxy = get_proxy_server()
        proxies = {"https": proxy, "http": proxy}
        session = requests.Session()
        session.proxies = proxies
        if not os.path.exists(full_name):
            logger.info(f"Downloading {server_version} Server...")
            download_with_progress_bar_retry(session, MONGO_DB_SERVER_EXE, full_name)
        logger.info(f"Installing MongoDB Server... {file_name}")
        # Install mongoDB server
        os.system(full_name)
        cfg.env.MONGO_DB_INSTALLED = True
        OmegaConf.save(cfg, CFG_FILE)
        return True
    except Exception as e:
        logger.exception(f"{e} - Cannot install mongoDB server.")


class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger('DatabaseManager')
        self.logger.addHandler(null_handler)
        self.connection = cfg.db.local.get("driver")
        self.client = self.start_new_connection()
        self.db = self.client.get_database()
        self.logger.debug(f'Database Status: {self.db.stats}')

    def start_new_connection(self):
        self.logger.warning(f"Starting New DB Connection...")
        client = None
        try:
            kwargs = {
                "connectTimeoutMS": 200, "serverSelectionTimeoutMS": 5000,
                "retryWrites": True
            }
            client = MongoClient(self.connection, **kwargs)
        except ServerSelectionTimeoutError:
            self.logger.warning(
                "Cannot Connect to Database! Please ensure DB server is running"
            )
        except Exception as e:
            self.logger.exception(
                f"{e} - Cannot Connect to Database!"
            )
            self.logger.critical("Please ensure service is running... MongoDB Server (MongoDB)")
        finally:
            return client

    def save_document(self, table_name, data, query=None):
        results = []
        try:
            try:
                if isinstance(data, dict):
                    del data['_id']
            except KeyError:
                pass

            if query is None:
                self.logger.debug(f"Adding New Record...\n{data}")
                results = self.db[table_name].insert_one(data)
            else:
                self.logger.debug(f"Updating Record with Query: {query}...\n{data}")
                results = self.db[table_name].replace_one(query, data, upsert=True)
        except Exception as e:
            self.logger.exception(f"{e} - Cannot save document.")
        finally:
            return results

    def get_document(self, table_name, query):
        records = []
        try:
            if query is not None:
                self.logger.debug(f"Loading Query: {query}")
                records = self.db[table_name].find(query)
                records = [x for x in records]
            else:
                self.logger.debug(f"Loading Records for: {table_name}")
                records = self.db[table_name].find({})
                records = [x for x in records]
        except Exception as e:
            records = []
            self.logger.exception(f"{e} - Cannot get document.")
        finally:
            return records

    def get_table_list(self, name, sort=None):
        """
        Retrieves data for the specified collection.

        Parameters
        ----------
        name: str
            name of the database collection.
        sort: list
            [Optional] - [(value, direction)] whereas value is the field in documents to sort by;
            direction is an int value specifying the sort order: ascending=1, descending=-1

        Returns
        -------
        list:
            records in the specified database collection as key value pairs.

        """
        self.logger.debug(f"Attempting to retrieve collection from database...")
        database = []
        try:
            if sort:
                database = [x for x in self.db[name].find({}).sort(sort)]
            else:
                database = [x for x in self.db[name].find({})]
        except Exception as e:
            self.logger.exception(f"{e} - Cannot get database table")
        finally:
            return database

    def get_table_dict(self, name, sort=None):
        """
        Retrieves data for the specified collection.

        Parameters
        ----------
        name: str
            name of the database collection.
        sort: list
            [Optional] - [(value, direction)] whereas value is the field in documents to sort by;
            direction is an int value specifying the sort order: ascending=1, descending=-1

        Returns
        -------
        dict:
            records in the specified database collection as key value pairs.

        """
        self.logger.debug(f"Attempting to retrieve collection from database...")
        database = {}
        try:
            if sort:
                records = self.db[name].find({}).sort(sort)
            else:
                records = self.db[name].find({})
            for record in records:
                try:
                    del record['_id']
                except KeyError:
                    self.logger.debug("No '_id' found in record.")
                database.update(record)
        except Exception as e:
            self.logger.exception(f"{e} - Cannot get database table")
        finally:
            return database

    def delete_document(self, table_name, query):
        results = {}
        try:
            if '_id' in query.keys():
                query = {'_id': query.get('_id')}
            self.logger.debug(f"Deleting Database Record: {query}")
            results = self.db[table_name].delete_one(query)
        except Exception as e:
            self.logger.exception(f"{e} - Cannot delete document.")
        finally:
            return results

    def bulk_update(self, table_name, data):
        """
        Update several records in the database.

        Args:
            table_name (str): name of the collection to update.
            data (list): list of Tuple (query, record) where as.
                query - dictionary object to query database.
                record - new record to insert in the database.

        Returns:
            int: number of records that were inserted or updated in the database.

        """
        self.logger.debug(f"Attempting to update table:{table_name} with data: {data}")
        count = 0
        try:
            # Create list of data to bulk update
            bulk_data = []
            if data:
                for query, record in data:
                    bulk_data.append(ReplaceOne(query, record, upsert=True))
                # Update Database
                self.logger.debug(f"Bulk Updating '{table_name}': {bulk_data}")
                results = self.db[table_name].bulk_write(bulk_data)
                count = results.matched_count
            else:
                self.logger.warning(f"No data provided for: {table_name}! data={data}")
        except Exception as e:
            self.logger.exception(f"{e} - Cannot bulk update database.")
        finally:
            return count

    def bulk_delete(self, table_name, records):
        """
        Delete several records in the database.

        Args:
            table_name (str): name of the collection to update.
            records (list): list of DB records to delete.

        Returns:
            int: number of records that were deleted from database.

        """
        self.logger.debug(f"Attempting to delete records={records} from table:{table_name}")
        count = 0
        try:
            # Create list of data to bulk delete
            bulk_data = []
            if records:
                for record in records:
                    bulk_data.append(DeleteOne(record))
                # Delete DB Records
                self.logger.debug(f"Bulk deleting records... {bulk_data}")
                results = self.db[table_name].bulk_write(bulk_data)
                count = results.matched_count
            else:
                self.logger.warning(f"No data provided for: {table_name}! records={records}")
        except Exception as e:
            self.logger.exception(f"{e} - Cannot bulk delete database.")
        finally:
            return count


def read_zip_file(file):
    """
    Extract zip files to the specified destination.
    :param file: full path to zip file.

    :return: list of files in the provided zip file
    """
    file_list = []
    try:
        if is_zipfile(file):
            try:
                logger.info(f"Reading zip file: '{file}'...")
                with ZipFile(file, 'r') as zip_file:
                    file_list = zip_file.namelist()
            except PermissionError:
                logger.exception(
                    f"Permission Error! - '{file}' already in use.")
        else:
            logger.error(f"{file} is Not a ZipFile")
    except Exception as e:
        logger.exception(f"{e} - Cannot read zip file!")
    finally:
        return file_list


def read_zip_directories(file, root_dir, include_sub_dir=True):
    zip_paths = []
    file_list = read_zip_file(file)
    if not str(root_dir).endswith('/'):
        root_dir = f"{root_dir}/"
    for name in file_list:
        if name.startswith(root_dir) and name.endswith('/'):
            parts = name.split(root_dir)
            if len(parts[1]) < 1:
                continue
            name = parts[1].strip('/')
            if include_sub_dir:
                zip_paths.append(name)
            else:
                if name.find('/') > 0:
                    continue
                zip_paths.append(name)

    return zip_paths


def extract_selected_zip_files(file,
                               destination=None,
                               file_list=[],
                               ignore_dir_list=[],
                               ignore_file_list=[]):
    """
    Extract zip files to the specified destination.
    :param file: full path to zip file.
    :param destination: full path of location to extract the zip file.
    :param file_list: list of file names or directories to extract from the zip file.
    :param ignore_dir_list: list of directory names to ignore in the zip file.
    :param ignore_file_list: list of file extensions to ignore in the zip file.

    :return set: (destination, file_list) - whereas:
        destination - file path with extracted files.
        file_list - list of files extracted from the specified zip file.
    """
    extracted_files = []
    try:
        if is_zipfile(file):
            try:
                with ZipFile(file) as zip_file:
                    logger.debug(f"File Search List={file_list}")
                    if destination is None:
                        full_name = Path(file)
                        suffix = full_name.suffix
                        folder_name = full_name.name.replace(suffix, "")
                        destination = os.path.join(get_workstation(), folder_name)
                    if not os.path.exists(destination):
                        logger.info(
                            f"Extracting selected zip files: '{file}'...")
                        os.mkdir(destination)
                    for file_name in zip_file.namelist():
                        skip = False
                        for ext in ignore_file_list:
                            if file_name.endswith(ext):
                                logger.debug(
                                    f"Skipping file: '{file_name}'...")
                                skip = True
                                break
                        for name in ignore_dir_list:
                            if file_name.find(name) >= 0:
                                logger.debug(f"Skipping dir: '{file_name}'...")
                                skip = True
                                break
                        if skip:
                            continue
                        for name in file_list:
                            skip = True
                            if file_name.find(name) >= 0:
                                skip = False
                                break
                        if skip:
                            logger.debug(
                                f"'{file_name}' Not Found in Selected Files! Skipping...")
                            continue
                        zip_file.extract(file_name, destination)
                        extracted_files.append(file_name)
            except PermissionError:
                logger.exception(
                    f"Permission Error! - '{file}' already in use.")
        else:
            logger.error(f"{file} is Not a ZipFile")
    except Exception as e:
        logger.exception(f"{e} - Cannot read zip file!")
    finally:
        return destination, extracted_files


class SwumNexus(Nexus):
    """Extends the functionality of the Nexus class to allow
    users to download build artifacts by simply providing the nexus URL.
    """

    def __init__(self,
                 username,
                 password,
                 repository_url='https://www.nexus.ford.com'):
        """
        Creates a new Nexus object authenticated with the provided credentials

        Parameters
        ----------
        username : str
            The Ford User ID of the user running the script.
        password : str
            The Ford User Password of the user running the script.
        repository_url : str, optional
            the website used to authenticate the provided login credentials
        """
        self.proxies = {}
        self.user = username
        self.password = password
        self.logger = logging.getLogger('SwumNexus')
        self.logger.addHandler(null_handler)
        self.session = SessionWithDefaultSslContext()
        self.session.auth = (self.user, self.password)
        super(SwumNexus, self).__init__(username, password, repository_url)

    def get_session(self):
        """
        Gets the current Nexus session

        Returns
        -------
        SessionWithDefaultSslContext
            The current nexus session.
        """
        return self.session

    def attempt_nexus_download(self, nexus_url, destination, file_name=None):
        """
        Downloads the build artifact from the provided Nexus URL
        to the specified location

        Parameters
        ----------
        nexus_url : str
            The Nexus url where the file is located.
        destination : str
            The location to store the downloaded file
        file_name : str, optional
            The file name to save the artifact as

        Returns
        -------
        str
            The full path to the downloaded artifact if successful,
        None
            if the download fails.
        """

        try:
            self.logger.debug(
                f'Attempting to download nexus artifact from url: {nexus_url}'
            )
            with self.get_session() as session:
                if file_name is None:
                    file_name = nexus_url.split('/')[-1]
                destination = os.path.join(destination, file_name)
                # Check to make sure file is not already downloading
                partial_file = f"{destination}.part"
                if os.path.exists(partial_file):
                    file_size = os.path.getsize(partial_file)
                    file = Path(partial_file)
                    time.sleep(2)
                    if os.path.getsize(partial_file) == file_size:
                        self.logger.warning(f"Deleting incomplete file download... {file}")
                        os.remove(file)
                        download_with_progress_bar_retry(
                            session, nexus_url, destination, max_attempts=3)
                    else:
                        self.logger.warning(f"\nFile already downloading... {file_name}")
                        while os.path.exists(partial_file):
                            time.sleep(3)
                            if os.path.getsize(partial_file) == file_size:
                                self.logger.warning(f"\nFile Download Stopped for: {file_name}")
                                break
                            file_size = os.path.getsize(partial_file)
                else:
                    download_with_progress_bar_retry(
                        session, nexus_url, destination, max_attempts=3)
        except OSError:
            self.logger.debug(f"Pending file download completed for: {destination}")
        except Exception as e:
            self.logger.exception(f"{e} Cannot attempt nexus download.")
        finally:
            return destination

    def get_nexus_files(self, nexus_url, destination):
        self.logger.info(f"Retrieving files for: {nexus_url}")
        results = {}
        try:
            nexus_file = self.attempt_nexus_download(nexus_url, destination)
            results = read_zip_file(nexus_file)
        except Exception as e:
            logger.exception(f"{e} - Cannot get nexus files.")

        return results


class JiraIssueManager:
    """
    Extends the functionality of FordJIRA to validate user inputs when
    raising Jira items.
    """

    def __init__(self, env, username, password):
        """
        :param env: Jira environment. can be any of the following: [Prod, QA]
        :param username: username used to authenticate Jira server.
        :param password: password used to authenticate Jira server.
        """
        self.key = None
        self._new_issue = {}
        try:
            # self._ford_jira = FordJIRA(username, password, server=env)
            self._ford_jira = FordJIRA(server=env)
        except Exception as e:
            logger.exception(f"{e} - Invalid Login Credentials!")

    def _search_jira_issue(self, query, summary, description):
        if not summary:
            raise ValueError(f"Invalid Value: summary={summary}")
        logger.debug(
            f"Searching for issue: '{summary}' with query={query}"
        )
        jira_issue = {}
        try:
            issues = self._ford_jira.search_issues(query)
            for issue in issues.values():
                fields = issue.fields
                status = fields.get(STATUS)
                jira_summary = fields.get(SUMMARY)
                jira_description = fields.get(DESCRIPTION)
                if str(jira_summary).find(summary) >= 0:
                    size = len(jira_description) + len(description)
                    if size > MAX_JIRA_CHARACTERS:
                        continue
                    jira_issue = deepcopy(fields)
                    break
        except Exception as e:
            logger.exception(f"Error Finding Jira - {e}")
        finally:
            return jira_issue

    def close_duplicate_issues(self, project, summary, label=None):
        """
        Closes all duplicate JIRA issues matching the specified project and summary

        :param project: project from which to close duplicates. e.g. 'TAT'
        :param summary: summary of the JIRA issue.
        :param label: [OPTIONAL]. Only close issue that has the specified label.

        :return: number of duplicates issues closed.
        """
        count = 0
        try:
            if not project or not summary:
                msg = "JIRA Project & Summary Must be Provided!"
                raise ValueError(msg)
            query = f"project = {project} AND status IN (open, analysis)"
            if label:
                query = f"{query} AND labels IN ({label})"
            issues = self._ford_jira.search_issues(query)
            duplicates = []
            for issue in issues.values():
                fields = issue.fields
                if summary not in fields.get(SUMMARY, ""):
                    continue
                duplicates.append(fields.get(JIRA_KEY))
            jira_key = duplicates.pop()
            count = len(duplicates)
            logger.debug(f"Main JIRA Issue={jira_key} for '{summary}'. ({count}) Duplicates Found!")
            for jira_key in duplicates:
                logger.debug(f"closing duplicate issue... {jira_key}")
                self._ford_jira.transition_issue(jira_key, "Close", "Duplicate")
        except IndexError:
            logger.debug(f"No duplicate issues found for: '{summary}' in project={project}")
        except Exception as e:
            logger.exception(f"{e} - Cannot close duplicate issues.")
        finally:
            return count

    def _save_ticket(self, **kwargs):
        """
        Save current jira issue.
        """
        created = False
        try:
            # Search for existing tickets
            labels = self._new_issue.get(LABELS)
            query = f"status != {CLOSED}"
            if labels:
                query = f"{query} AND labels IN ({labels})"
            summary = self._new_issue.get(SUMMARY)
            description = self._new_issue.get(DESCRIPTION)
            jira_issue = self._search_jira_issue(query, summary, description)
            self.key = jira_issue.get(JIRA_KEY)
            # Create new ticket if not exist or update ticket.
            if self.key:
                # Update Existing JIRA
                jira_description = jira_issue.get(DESCRIPTION)
                search_value = kwargs.get(SEARCH_VALUE, description)
                logger.debug(
                    "Attempting to update the following jira: key="
                    f"{self.key}, description={jira_description}"
                )
                if str(jira_description).find(search_value) < 0:
                    try:
                        del self._new_issue[SUMMARY]
                    except KeyError:
                        logger.debug(f"summary not found in jira issue.")
                    logger.warning(f"Updating jira ticket: {self.key}")
                    self._new_issue[DESCRIPTION] = f"\r\n{description}"
                    self._ford_jira.update_issue(self.key, issue_dict=self._new_issue)
                    logger.info(
                        f"Jira Updated Successfully! {self.key}"
                    )
                else:
                    logger.info(f"Jira already logged. {self.key}")
                    logger.debug(f"text={search_value}, description={jira_description}")
            else:
                logger.warning(f"Creating jira ticket for: {summary}")
                self.key = self._ford_jira.create_issue(issue_dict=self._new_issue)
                logger.info(
                    f"Jira Created Successfully! {self.key}"
                )
                created = True
        except Exception as e:
            logger.exception(f"{e} - Cannot Save Jira Ticket")
        finally:
            return created, self.key

    def create_jira_ticket(self, issue_dict):
        """
        Create or Update Existing JIRA Ticket.

        :param issue_dict: keywords arguments as key value pairs.
        :type issue_dict: dict

        :return: (created, issue) - whereas:
            create - is a boolean specifying in a new ticket was created.
            issue - dict containing jira ticket info as key/value pairs.
        """
        jira_issue = {}
        created = False
        try:
            # Initialize default values
            self._new_issue = {
                PROJECT: JiraProject.TAT,
                ISSUE_TYPE: JiraIssueType.DEFECT,
                SEVERITY: JiraSeverity.MINOR,
                PRIORITY: JiraPriority.HIGH,
                COMPONENTS: [JiraComponent.SWUM, JiraComponent.MMOTA_TRIAGE],
                LABELS: JiraLabel.CLOUD_MANAGER,
            }
            fields = self._ford_jira.get_field_names()
            for name in fields:
                value = issue_dict.get(name)
                if not value:
                    continue
                self._new_issue[name] = deepcopy(value)
            created, jira_key = self._save_ticket(**issue_dict)
            jira_issue = self._ford_jira.get_issue(jira_key).fields
        except Exception as e:
            logger.exception(f"{e} - Cannot Create Jira Ticket.")
        finally:
            return created, jira_issue

    def get_issue(self, jira_key):
        """
        Add a watcher to a jira issue.

        :param jira_key: Jira key for which to retrieve issue.

        :return: Issue matching the specified jira key.
        """
        issue = Issue({}, ResilientSession())
        try:
            logger.debug(f"Retrieve issue for jira={jira_key}...")
            issue = self._ford_jira.get_issue(jira_key)
        except Exception as e:
            logger.exception(f"{e} - Cannot retrieve jira issue.")
        finally:
            return issue

    def add_watcher(self, jira_key, username):
        """
        Add a watcher to a jira issue.

        :param jira_key: Jira key of which to add watcher
        :param username: watcher to add (CDSID as string)
        """
        try:
            logger.debug(f"Adding watcher={username} to jira={jira_key}...")
            self._ford_jira.add_watcher(jira_key, username)
        except Exception as e:
            logger.exception(f"{e} - Cannot add watcher to jira.")

    def add_comment(self, jira_key, comment):
        """
        Add a comment to a jira issue.

        :param jira_key: Jira key of which to add comment
        :param comment: comment to add to the issue
        """
        try:
            logger.debug(f"Adding comment={comment} to jira={jira_key}...")
            self._ford_jira.add_comment(jira_key, comment)
        except Exception as e:
            logger.exception(f"{e} - Cannot add comment to jira.")

    def add_attachment(self, jira_key, file_path):
        """
        Add an attachment to a jira issue.

        :param jira_key: Jira key of which to add attachment
        :param file_path: path to the file you want to add (as a string)
        """
        try:
            logger.debug(f"Adding attachment={file_path} to jira={jira_key}...")
            attachments = self._ford_jira.get_attachment_list(jira_key)
            file_name = Path(file_path).name
            if file_name not in attachments:
                logger.debug(f"Adding {file_name} to jira...")
                self._ford_jira.add_attachment(jira_key, file_path)
            else:
                logger.debug(f"{file_name} already added to {jira_key} attachments.")
        except Exception as e:
            logger.exception(f"{e} - Cannot add attachment to jira.")


def retrieve_nexus_data(url, username, password, retry=3):
    """
    Retrieve data from provided url using a Nexus Session.
    :return: response from server.
    """
    results = {}
    success = False
    logger.debug(f"Retrieving data from url: {url}")
    valid, reason = is_valid_url(url)
    if not valid or not str(url).endswith('.json'):
        logger.critical(f"Invalid URL Detected! {url}")
        return success, results
    nexus = SwumNexus(username, password)
    nexus_session = nexus.get_session()
    while retry > 0:
        msg = "Please check network connection and build url."
        try:
            response = nexus_session.get(url)
            success = response.ok
            logger.debug(
                "Server response code: " + str(response.status_code)
            )
            logger.debug(
                "Server response text: " + str(response.text)
            )
            if response.status_code == 200:
                json_response = response.json()
                results = json_response
                break
            elif response.status_code == 400:
                logger.error(
                    "Error Retrieving Data! 400 - Bad Request"
                )
                results = {"message": deepcopy(response.text)}
                break
            elif response.status_code == 401:
                logger.error(
                    "Error Retrieving Data! 401 - Unauthorized(Invalid Login Credentials)"
                )
                results = {
                    "message": deepcopy(response.text),
                    "status_code": response.status_code
                }
                break
            elif response.status_code == 403:
                logger.error(
                    "Error Retrieving Data! 403 - Directory Not Found"
                )
                results = {
                    "message": deepcopy(response.text),
                    "status_code": response.status_code
                }
                break
            elif response.status_code == 404:
                logger.error(
                    f"Error Retrieving Data! 404 - Page Not Found! \n{url}"
                )
                results = {
                    "message": deepcopy(response.text),
                    "status_code": response.status_code
                }
                break
            else:
                logger.error(f"{response} retry in 60 Seconds...")
                time.sleep(60)
        except (ConnectionError, OSError) as e:
            logger.error(f"{e}! {msg} Retry in 30 Seconds...")
            time.sleep(30)
            retry -= 1
        except Exception as e:
            logger.critical(f"{repr(e)} {msg} {url}")
            logger.exception(f"New Exception: {e}")
            success = False
            break

    return success, results


def extract_html_app_info(manifest, sync_variant):
    logger.debug(f"Extracting html apps for: {sync_variant}")
    results = {}
    try:
        artifact_info = manifest.get(sync_variant, [])
        additional_apps = manifest.get(PACKAGES, [])
        if len(artifact_info) < 1:
            logger.error(f"Cannot find '{sync_variant}' in html manifest!")
            return results
        if len(additional_apps) < 1:
            logger.critical(f"Cannot find '{PACKAGES}' in html manifest!")
        else:
            artifact_info.extend(additional_apps)
        for app in artifact_info:
            try:
                name = app[NAME]
                description = app[DESCRIPTION]
                version = app[VERSION]
                links = app[LINKS]
                nexus_url = links[name]
                results[description] = deepcopy({
                    FILE: name,
                    VERSION: version,
                    NEXUS_URL: nexus_url
                })
            except KeyError:
                logger.error(f"Cannot retrieve html app info for app: {app}")
    except Exception as e:
        logger.exception(f"{e} - Cannot extract html sync apps!\n{manifest}")
    finally:
        return results


def get_latest_build_number(build_url, username, password):
    build_number = "0"
    status = False
    try:
        ecu = get_ecu_type_from_url(build_url)
        url_type = get_url_type(build_url)
        logger.debug(
            f"Retrieving latest build number with ecu={ecu} & url_type={url_type}"
            f"\nbuild_url={build_url}"
        )
        if build_url.find("Sync4-master") > 0 and build_url.find("nexus.ford.com") < 1:
            artifact_url = str(build_url).split('/artifact/')
            if build_url.find("lastSuccessfulBuild") > 0:
                url = f"{artifact_url[0]}/artifact/"
                html = get_html_page(url, username, password)
                head = etree.HTML(html).find('head')
                for element in head:
                    if element.tag == "title":
                        title, build = str(element.text).split('#')
                        build_number = []
                        for num in build:
                            if is_numeric(num):
                                build_number.append(num)
                            else:
                                break
                        build_number = "".join(build_number)
                        break
                if build_number:
                    status = True
                    return status, build_number
            else:
                variant = str(artifact_url[1]).split('/')[0]
                build_number = str(variant.split('-')[-1])
                status = True
                return status, build_number
        if url_type == JSON:
            # Retrieve build number from manifest
            status, manifest = retrieve_nexus_data(
                build_url, username, password
            )
            if ecu in [ECG1, ECG2, TCU1, TCU2]:
                build_number = manifest['jenkins_buildID']
                status = True
            elif ecu in [SYNC, PHOENIX]:
                version = manifest[ASSEMBLIES][0][NEXUS_VERSION]
                build_number = str(version).split('-')[-2]
                status = True
            else:
                msg = f"ECU Type={ecu} Not Supported!"
                raise NotImplementedError(msg)
        elif url_type == HTML:
            manifest = html_to_json(build_url, username, password)
            try:
                version = manifest[ASSEMBLIES.capitalize()][0][VERSION]
                build_number = str(version).split('.')[-1]
                status = True
            except KeyError:
                for assembly in manifest:
                    version = manifest[assembly][0][VERSION]
                    build_number = re.findall(BUILD_NUMBER_PATTERN, version)[0]
                    status = True
                    break
        elif url_type == NEXUS_ARTIFACT:
            url_parts = str(build_url).split('/')
            if ecu in [SYNC, PHOENIX]:
                build_number = url_parts[-1].split('-')[-2]
                status = True
            else:
                build_number = url_parts[-1].split('.')[-2]
                status = True
        else:
            msg = f"URL Type='{url_type}' Not Supported!"
            raise NotImplementedError(msg)
    except Exception as e:
        logger.exception(f"{e} - Cannot retrieve latest build number.")
    finally:
        return status, build_number


def get_support_sync_variants_html(manifest):
    results = []
    try:
        key = ASSEMBLIES.capitalize()
        supported_pkgs = manifest[key]
        for package in supported_pkgs:
            variant = package[DESCRIPTION]
            results.append(variant)
    except Exception as e:
        logger.exception(
            f"{e} - Cannot retrieve supported sync variants from html."
        )
        logger.debug(f"manifest={manifest}")
    finally:
        return results


def get_sync_variant_apps(url, username, password):
    """
    Download SYNC Apps and retrieve version information

    :param url: url path to sync manifest.json
    :param username:
    :param password:
    :return: dictionary object with sync apps info for the specified
        package_name. {app_name :(part_number, app_version), ...} where as:
        app_name - is the name of the sync application,
        part_number - is the part number of the application.
        app_version - is the version number of the application

    """
    logger.debug(f"Retrieving Apps & Maps from url={url}")
    success = False
    results = {}
    try:
        manifest_type = get_url_type(url)
        if manifest_type == JSON:
            success, manifest = retrieve_nexus_data(url, username, password)
            artifact = 'package_artifacts'
            logger.debug(
                f"Extracting sync variant apps from: url={url}"
            )
            if not success:
                logger.critical("Cannot retrieve sync manifest.")
                return success, results
            for package in manifest['assemblies']:
                package_name = package['description']
                if package_name in SYNC_VARIANTS_IGNORE_LIST:
                    logger.warning(
                        f"Skipping Unsupported Variant: '{package_name}'..."
                    )
                    continue
                results[package_name] = []
                logger.debug(
                    f"Extracting sync artifact for: {package_name}"
                )
                pkg_artifact = get_sync_artifact(
                    manifest, package_name, artifact
                )
                for app in pkg_artifact:
                    app_name = app[DESCRIPTION]
                    results[package_name].append(app_name)
        elif manifest_type == HTML:
            manifest = html_to_json(url, username, password)
            logger.debug(
                f"Extracting sync variant apps from html: url={url}"
            )
            supported_variants = get_support_sync_variants_html(manifest)
            for package_name in supported_variants:
                logger.debug(
                    f"Extracting html sync apps for: {package_name}"
                )
                pkg_artifact = extract_html_app_info(
                    manifest, package_name
                )
                results[package_name] = list(pkg_artifact.keys())
        else:
            msg = f"Manifest Type Not Supported! {manifest_type}"
            raise NotImplementedError(msg)
    except Exception as e:
        logger.exception(
            f"{e} - Cannot retrieve applications for: {url}"
        )
    finally:
        return success, results


def create_app_shortcuts():
    # Create app shortcuts
    logger.debug(f"Creating application shortcuts... {ROOT_DIR}")
    desktop = winshell.desktop()
    app_path = os.path.join(desktop, f"{SYSTEM_NAME}.lnk")
    dir_path = os.path.join(desktop, "SWUM Working Directory.lnk")
    app_target = os.path.join(ROOT_DIR, f'{SYSTEM_NAME}.exe')
    dir_target = os.path.join(ROOT_DIR, 'swum_cloud_manager')
    logger.debug(f"app shortcut link={app_path}")
    logger.debug(f"app_target={app_target}")
    # Create shortcut to app.exe
    with winshell.shortcut(app_path) as shortcut:
        shortcut.path = app_target
        shortcut.description = SYSTEM_NAME
        shortcut.working_directory = ROOT_DIR
    # Create shortcut to working dir
    with winshell.shortcut(dir_path) as shortcut:
        shortcut.path = dir_target
        shortcut.working_directory = ROOT_DIR

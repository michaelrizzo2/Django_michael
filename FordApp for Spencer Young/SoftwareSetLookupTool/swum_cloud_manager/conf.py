import os
import time
import json
from pathlib import Path
from calendar import timegm
WORKING_DIR = os.getcwd()
CURRENT_USER = os.getlogin()
PC_DOMAIN = "na2.ford.com"
PARENT_DIR = os.path.dirname(__file__)
ROOT_DIR = str(Path(PARENT_DIR).parent)
AUTOMATION_PC = ['WGC110F4N1H03', 'WGC1106PND793']
PC_NAME = os.environ['COMPUTERNAME']
PART_II_SPECS = os.path.join(WORKING_DIR, "MDX Files")
WORKSTATION = os.path.join(WORKING_DIR, f"{PC_NAME}_{timegm(time.gmtime())}")
LOGS_FOLDER = os.path.join(WORKSTATION, 'logs')
TESTS_FOLDER = os.path.join(ROOT_DIR, 'tests')
TEST_DATASET_FILE = os.path.join(TESTS_FOLDER, "test_dataset.json")
LOG_STR_FORMAT = '%(name)s.%(threadName)s %(levelname)s: %(message)s'
CFG_FILE = os.path.join(PARENT_DIR, "config.yaml")
PROXY_ENV = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']
# Requests
GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"
STATUS = "status"
PROJECT = "project"
ISSUE_TYPE = "issue_type"
COMPONENTS = "components"
ATTACHMENT = "attachment"
SEVERITY = "severity"
PRIORITY = "priority"
LABELS = "labels"
SUMMARY = "summary"
CREATED = "created"
JIRA_KEY = "key"
CREATED_BY = 'createdBy'
ASSIGNEE = "assignee"
ASSIGNEE_ID = "assignee_cdsid"
DESCRIPTION = "description"
RESOLUTION = "resolution"
PLATFORMS = "applicable_platforms"
NEW_ISSUES = "NEW_ISSUES"
PENDING_ISSUES = "PENDING_ISSUES"
PENDING_UPLOADS = "PENDING_UPLOADS"
COMPLETED_ISSUES = "COMPLETED_ISSUES"
FOUND_IN_BUILD = "integrated_in_branch"
TEST_ENVIRONMENT = "test_environment"
VEHICLE_PROGRAM = "vehicle_program"
REPLACEMENTS = "replacements"
SEARCH_VALUE = "search_value"
REPLACES = "replaces"
JIRA_ISSUE = "jira_issue"
CLOSED = "Closed"
OPEN = "Open"
PATH = "path"
FILE = "file"
FILES = "files"
MAPS = "maps"
APPS = "apps"
SWS_INFO = "sws_info"
APP_NAME = "app_name"
APP_VERSION = "app_version"
APP_NAMES = "app_names"
FILE_SIZE = "file_size"
LOW = "SYNC - Low Cost"
MID_HIGH = "SYNC - Mid/High"
STORAGE_URL = "storageUrl"
CHINA_STORAGE_URL = "chinaStorageUrl"
DELIVERY_URL = "cdnDeliveryUrl"
VBF_URLS = [STORAGE_URL, CHINA_STORAGE_URL, DELIVERY_URL]
# BUILD TYPE
PROTOTYPE = "PROTOTYPE"
PR_BUILD = "PR_BUILD"
GROUP_ID = "groupid"
ARTIFACT = "artifact"
HTML_ARTIFACT = "html_artifact"
NEXUS_NAME = "nexus_name"
NEXUS_GROUP = "nexus_group"
NEXUS_VERSION = "nexus_version"
NEXUS_EXTENSION = "nexus_extension"
NEXUS_META_DATA = "sync4-buildroot-metadata"
NEXUS_FETCH_REPOSITORY = "nexus_fetch_repository"
ARTIFACT_VERSION = "artifact_version"
MANIFEST_VERSION = "versionFromManifest"
NEXUS_ARTIFACT_ID = "nexus_artifactid"
BUILD_ARTIFACT = "build_artifact"
ARTIFACT_ID = "artifact_id"
NEXUS_URL = "nexus_url"
NEXT_BUILD_URL = "next_build_url"
NEXT_SOURCE_URL = "next_source_url"
FILE_FILTER = "file_filter"
PAYLOAD = "payload"
TIME_OUT = "timeout"
ECU = 'ecu'
FPN = "FPN"
NAME = "name"
LINKS = "links"
LOCATION = "location"
PACKAGES = "Packages"
ASSEMBLIES = "assemblies"
SUPPLEMENTS = "Supplements"
PACKAGE_ARTIFACT = "package_artifacts"
PENDING_UPDATES = "pending_updates"
MAX_JIRA_CHARACTERS = 25000
SYSTEM_NAME = "MMOTA Cloud Data Setup Tool"
SYSTEM_VERSION = "v3.0.6"
OFFICIAL_BUILD = "official_build"
FILE_UPLOAD_LIST = "file_upload_list"
CALIBRATION_FILES = "calibration_files"
VIM_ARTIFACTS = "vim_artifacts"
USERS = {
    "AALAM11": "Alam, Amur (A.P.)",
    "JJOSEP76": "Joseph, Julian (J.)",
    "MRIZZO12": "Rizzo, Michael (M.)",
    "MBROW640": "Brown, Micombero (M.)",
    "DCORRE10": "Correal, Diana (D.)",
    "JPERE447": "Perez, Jose (J.A.)",
    "JANAYA15": "Anaya, Jorge (J.)",
    "JMERCA35": "Mercado, Juvenal (J.)",
    "OORTIZ16": "ORTIZ, OSCAR (O.)",
    "AAMBRIZ": "AMBRIZ, AMAURY (A.)",
    "URODRIG3": "RODRIGUEZ, URIEL (U.)",
    "JGILCH10": "Gilchrist, Jeff (J.)",
    "FREYNOS4": "Reynoso, Fernanda (F.)",
    "JPRAJA15": "Prajapati, Jaydeep (J.)",
    "AARELL18": "ARELLANO, ANGEL (A.)",
    "PVILLAG5": "Villagomez, Patricia (P.)",
    "SCHOI20": "Choi, Sid (S.)"
}
INCLUDED = "included"
EXCLUDED = "excluded"
F16B = "f16b"
F10A_FILES = "F10A_FILES"
F16C_FILES = "F16C_FILES"
F16B_FILES = "F16B_FILES"
ENVIRONMENT = "environment"
ECG_CONFIG_APPS = "VIM Artifacts"
CALIBRATION_APPS = "Calibration Apps"
URL_VARIANT_PATTERN = "([0-9]+G)+(_[0-9]+G)*"
MDX_PATTERN = r"^[0-9a-zA-Z]+-[0-9a-zA-Z]+-[a-zA-Z]+[0-9]+$"
DEV_FILE_PATTERN = r"(?i)[0-9a-zA-Z]+-[0-9a-zA-Z]+-[a-zA-Z]+([0-9]|local)"
SYSTEM_SETTINGS = "settings.json"
SWUM_USER = "SWUM_USER"
CAN_DELETE = "canDelete"
UNAUTHORIZED_UPLOADS = os.path.join(ROOT_DIR, "unauthorized_uploads.json")
DOWN_STREAM_STATUS = "downstreamStatus"
APPLICATION_GROUPS = "applicationGroups"
DOMAIN_INSTANCE_REL = "domainInstances"
SYSTEM_SETTINGS_FILE = os.path.join(PARENT_DIR, SYSTEM_SETTINGS)
MASTER_BUILD_PATTERN = r"(?i)(ECG_Bundle_Release|ECG2_WRLinux_|TCU_Bundle_Release|/modem6_Bundle_Release|IntegrationsMaster)"
# Phoenix
USER = "user"
GAS_USER = "gas_user"
# Software Lineage & Differential Files
SYNC_SIGN_COMMAND = "SYNC4_7D0_AP_OTA"
ECG_SIGN_COMMAND = "ECG_716_AP_OTA"
TCU_SIGN_COMMAND = "TCU_754_AP_OTA"
SIGNING_TYPE = "COMPLEX"
COMPRESSION = "LZMA"
COMPRESSION_LEVEL = 5
# ECG
F16B_PART_NUMBERS = ["14H525"]
F10A_PART_NUMBERS = ["14J009", "U540-F10A", "C519-F10A", "C519-F10A", "P552-F10A", "U55X-F10A", "U625-F10A", "14H485"]
F16C_PART_NUMBERS = ["14J007", "U540-F16C", "C519-F16C", "C519-F16C", "P552-F16C", "U55X-F16C", "U625-F16C", "14H484"]
# "14G680", "14J003", "local", *F10A_PART_NUMBERS, *F16C_PART_NUMBERS
ALLOWED_OFFICIAL_FILES = []
SWS_WIKI_PAGE = "https://www.eesewiki.ford.com/display/fnv/Software+Sets+-+Daily+Uploads"
NEXUS_REPOSITORY_URL = "https://www.nexus.ford.com/repository/fnv2-private-maven-group/com/ford/sync/sync4_0/launch-SYNC-v1/8/0/sync4-buildroot-metadata/Sync4-launch-signing-16G_32G-775-a124fe9f23/sync4-buildroot-metadata-Sync4-launch-signing-16G_32G-775-a124fe9f23.json"
SYNC_VARIANTS = {
    "pr_": ["8G", "16G", "32G", "64G"],
    "sync4-master": ["8G", "16G", "32G", "64G"],
    "launch": ["8G", "16G_32G", "32G", "64G"],
    "milestone": ["8G", "16G_32G", "32G", "64G"],
    "other": ["8G", "16G_32G", "16G", "32G", "64G"],
}
APPLICATIONS = [
    'APPLICATION', 'ECU_CONFIGURATION', 'CALIBRATION', 'SYNC_MAP_DATA',
    'SYNC_VOICE_DATA', 'CBZ_MAP_DATA'
]
CORE_FILES = [
    'BOOT_IMAGE', 'STRATEGY', 'PRIMARY_BOOTLOADER', 'SECONDARY_BOOTLOADER',
    'IMAGE'
]
OWNER_GUIDE_LINEAGE = [
    "alm-pkg-OwnersGuidesMY21-EU",
    "alm-pkg-OwnersGuidesMY21-NA",
    "alm-pkg-OwnersGuidesMY21-ROW",
    "alm-pkg-OwnersGuidesMY22-EU",
    "alm-pkg-OwnersGuidesMY22-NA",
    "alm-pkg-OwnersGuidesMY22-ROW",
    "alm-pkg-OwnersGuidesMY23-EU",
    "alm-pkg-OwnersGuidesMY23-NA",
    "alm-pkg-OwnersGuidesMY23-ROW",
]
SUPPORTED_APPLICATION_TYPES = [
    VIM_ARTIFACTS, CALIBRATION_FILES, APPS, MAPS
]
SINGLE_FILE_APPS = [ECG_CONFIG_APPS, CALIBRATION_APPS]
ID = "id"
URL = "url"
ECG = "ECG"
TCU = "TCU"
TCU1 = "TCU1"
TCU2 = "TCU2"
ECG1 = "ECG1"
ECG2 = "ECG2"
SYNC = "SYNC"
PHOENIX = "PHOENIX"
JSON = "json"
HTML = "html"
QUERY = "query"
# STATE = "state"
MESSAGE = "message"
VERSION = "version"
CATEGORY = "category"
LOG_FILE = "log_file"
SWS_NAME = "sws_name"
OWNER_GUIDES = "owners_guides"
SEQUENCE_ID = "sequence_id"
SEQUENCE_NAME = "sequence_name"
PART_NUMBER = "partNumber"
SW_PART_NUMBER = "sw_part_number"
LATEST_BUILD = "latest_build"
SYNC_VARIANT = "sync_variant"
AVAILABLE_VARIANTS = "available_variant"
BUNDLE_STATUS = "bundle_status"
NEXUS_ARTIFACT = "nexus"
PRODUCTION_STATE = "productionState"
DOMAIN_INSTANCE_ID = "domainInstanceId"
REMAINING_SOFTWARE = "remaining_software"
APPLICATION_LIST = "application_list"
PENDING_DOMAINS = "pending_domains"
PREVIOUS_DOMAIN = "previous_domain"
PREVIOUS_VERSION = "previous_version"
DOMAIN_LIST = "domain_list"
NOT_FOUND = "not_found"
MISSING_APPS = "missing_apps"
PENDING_APPS = "pending_apps"
MAX_UPLOAD_SEQUENCE = 100
GROUP_APPS = "group_apps"
INDEX = "index"
# Timer & Restrictions
TIME_PATTERN = r"^[0-9]{2}:[0-9]{2}:[0-9]{2}[.0-9]*"
FIVE_SECONDS = 5
ONE_MINUTE = 60
THREE_MINUTE = 180
FIVE_MINUTES = 300
TEN_MINUTES = 600
THIRTY_MINUTES = 1800
ONE_HOUR = 3600
TWO_HOUR = 7200
THREE_HOUR = 10800
EIGHT_HOUR = 28800
TWELVE_HOUR = 43200
TWENTY_HOUR = 72000
TWENTY_FOUR_HOUR = 86400
SWS_SLEEP_TIME = THREE_MINUTE
FILE_UPLOAD_TIMEOUT = THIRTY_MINUTES
RELEASE_DOMAIN_APPS_TIMEOUT = ONE_HOUR
UPLOAD_SIZE_LIMIT = 2048  # 2GB
MAX_FILE_UPLOAD = 4
# ENVIRONMENTS
QA = "QA"
STG = "STG"
PRD = "PRD"
# BUILD TYPES
INTEGRATION = "integration"
DEVELOPMENT = "development"
PRODUCTION = "production"
RELEASE = "release"
DEBUG = "debug"
RELEASED = "RELEASED"
EXCLUDE = "exclude"
CONTENT = "content"
DOMAIN_IDS = "domain_ids"
ECU_SOFTWARE = "ecuSoftware"
SOFTWARE_ID = "software_id"
SOFTWARE_IDS = "software_ids"
PART_TWO_SPECS = "part_two_specs"
ECU_SOFTWARE_ID = "ecuSoftwareId"
DOMAIN_INSTANCE = "domainInstance"
CLASSIFICATION = "classification"
DEPENDENT_ON = "DEPENDENT_ON"
COORDINATED_WITH = "COORDINATED_WITH"
RELATIONSHIP_TYPE = "relationshipType"
DOMAIN_RELATIONSHIP = "domainInstanceRelationships"
SOFTWARE_RELATIONSHIP = "ecuSoftwareRelationships"
INSTALLATION_SEQUENCE = "installationSequence"
SOFTWARE_PART_NUMBERS = "softwarePartNumbers"
SOFTWARE_LINEAGES_ADDED = "software lineages added"
DIFFERENTIAL_FILES_CREATED = "differential files created"
SYNC_VARIANTS_IGNORE_LIST = ["Developer-SDK"]
ALREADY_RELEASED = ["RELEASED", "RELEASED_PENDING_UPLOAD"]
SOFTWARE_TYPE = ["DEVELOPMENT", "PROTOTYPE", "PRODUCTION"]
ECU_PART_NUMBER = "ecuAssemblyPartNumber"
BASE_PART_NUMBER = "base_part_number"
SOURCE_PART_NUMBER = "source_part_number"
TARGET_PART_NUMBER = "target_part_number"
SUPPORTED_ECU_TYPES = [ECG1, ECG2, TCU1, TCU2, SYNC, PHOENIX]
SUPPORTED_AUTO_DOMAIN = [ECG1, ECG2, SYNC]
VALID_ECU_BUILD_TYPES = {
    ECG: [RELEASE, DEBUG, PRODUCTION],
    TCU: [RELEASE, DEBUG, PRODUCTION],
    SYNC: [DEVELOPMENT, PRODUCTION],
    PHOENIX: [INTEGRATION]
}
VALID_DEV_PROD_BUILD_TYPES = {
    DEVELOPMENT: {
        ECG: [RELEASE, DEBUG], TCU: [RELEASE, DEBUG], SYNC: [DEVELOPMENT], PHOENIX: [INTEGRATION]
    },
    PRODUCTION: {
        ECG: [PRODUCTION], TCU: [PRODUCTION], SYNC: [PRODUCTION], PHOENIX: [PRODUCTION]
    }
}
SUPPORTED_ECU_VERSIONS = {
    ECG: [ECG1, ECG2],
    TCU: [TCU1, TCU2],
    SYNC: [SYNC],
    PHOENIX: [PHOENIX]
}
SUPPORTED_ECUS = [ECG, TCU, SYNC, PHOENIX]
VMCU_BASE_KEYS = ['VMCU', 'VMCU SINGLE']
THREADS = "threads"
ACTIVE = "active"
PENDING = "pending"
STARTED = "started"
COMPLETE = "complete"
FAILED = "failed"
PARTIAL = "partial"
CONF_FILE = "conf.py"
PART_II_PART_NUMBER = "partIiPartNumber"
ECG2_FILE_LIST = [
    "out/target/product/vmcu/", "out/target/product/bootloader/",
    "out/target/product/aarch64le-debug/",
    "out/target/product/ECG2_LINCD_WRLinux/ggmt/",
    "out/target/product/ECG2_LINCD_WRLinux/perm/", ".vbf"
]
ECG1_FILE_LIST = [
    "ECG_VMCU", "out/target/product/bootloader/",
    "out/target/product/aarch64le-debug/", ".vbf"
]
DESTINATION = "destination"
NEW_DOMAIN_INSTANCES = "new_domain_instances"
SUPPORTED_DOMAIN_INSTANCES = "supported_domain_instances"
SUPPORTED_ECU_APPS = "supported_ecu_apps"
DOMAIN_INSTANCES = "domain_instances"
CCPU_BOOTLOADER_SECURE = "ccpu_bootloader_secure"
CCPU_BOOTLOADER = "ccpu_bootloader"
VMCU_BOOTLOADER = "vmcu_bootloader"
ANDROID_GUEST = "android_guest"
MODEM = "modem"
CCPU = "ccpu"
VMCU = "vmcu"
FUSA = "fusa"
CHIME = "chime"
VIP_SBL = "vip_sbl"
VIP_APP = "vip_app"
DI_GAUGES = "di_gauges"
ILLUMINATION = "illumination"
VMCU_INFO = "vmcu_info"
VIM_FOLDER = "vim_folder"
VMCU_FOLDER = "vmcu_folder"
CONTAIN_APPS = "contain_apps"
SOURCE_BUILD = "source_build"
BUILD_NUMBER = "build_number"
COLUMN_NAME = "column_name"
VARIANT_TYPE = "variant_type"
VARIANT_INFO = "variant_info"
BUILD_TYPE = "build_type"
BUILD_INFO = "build info"
BUILD_FILES = "build files"
MANUAL = "manual"
HIGH_LOW = "high_low"
DOMAIN = "domain"
FENIX = "Fenix"
BUILD = "build"
BRANCH = "branch"
PHX_NEXUS = "phx_nexus"
AOS_NEXUS = "aos_nexus"
PHX_BUILD_NUMBER = "phx_build_number"
AOS_BUILD_NUMBER = "aos_build_number"
UPLOADED = "UPLOADED"
BUILD_URL = "build_url"
PHX_BUILD_URL = "phx_build_url"
AOS_BUILD_URL = "aos_build_url"
SOURCE_URL = "source_url"
DESTINATION_URL = "destination_url"
DEVELOPER_EMAIL = 'DEVELOPER_EMAIL'
FILE_SETTINGS = "file_settings"
RELEASE_FILES = "release_files"
ADD_LINEAGE = "add_lineage"
SELECTED_GROUPS = "selected_groups"
USE_REAL_APP_NAMES = "use_real_app_names"
CREATE_DIFFERENTIAL_FILES = "create_differential_files"
UPLOAD_FILES_ONLY = "upload_files_only"
OVERWRITE_DB = "overwrite_database"
APPS_LIST = "apps_list"
MANIFEST = "manifest"
AOS_MANIFEST = "aos_manifest"
PHOENIX_APPS = [DI_GAUGES, ILLUMINATION, FUSA, CHIME]
SUPPORTED_CORE_FILES = [
    CCPU, CCPU_BOOTLOADER, CCPU_BOOTLOADER_SECURE, VMCU, VMCU_BOOTLOADER, MODEM, ANDROID_GUEST, VIP_APP, VIP_SBL
]
# Excel Keys
DOMAIN_VERSION = "Domain Instance"
ECG_VIM_ARTIFACTS = "ECG VIM Artifacts"
SYNC_CALIBRATION = "Sync Calibration"
SWS_DETAILS = "SWS Details"
DOMAIN_SWS = "Domain & SWS"
SYNC_APPS = "Sync Apps"
SWS_DETAILS_ARGS = [
    'SWS', 'Details', 'ECU', 'Build #', 'Build', 'Branch',
    DOMAIN_VERSION, 'Core Files', 'Apps', 'URL'
]
RECORD_ARGS_MAPPING = [
    FENIX, DESCRIPTION, ECU, BUILD_NUMBER, BUILD, BRANCH, DOMAIN
]
RECORD_KWARGS_MAPPING = [
    (SWS_INFO, 'Core Files'),
    (SWS_INFO, 'Apps'),
    f"{BUILD_FILES}.{BUILD_URL}"
]
# Databases
MONGO_DB_SERVER_EXE = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.1-signed.msi"
DOMAIN_AND_SWS = "domain_and_sws"
JENKINS_BUILD_URLS = "jenkins_build_urls"
ACTIVE_JIRA_ISSUES = "active_jira_issues"
PENDING_JIRA_ISSUES = "pending_jira_issues"
FAILED_BUILD_SEQUENCE = "failed_build_sequence"
NEXUS_BASE_URL = "nexus.ford.com"
SWS_RETRY = 3
URL_TYPES = {
    JSON: [".json"],
    HTML: [".html"],
    NEXUS_ARTIFACT: [".zip", "tar.gz", "(?i).VBF"],
}
JENKINS_PATTERN = ["fnvbuild.ford.com", "jenkins.ford.com"]
DEFAULT_ECG_APPS = {
    ECG_CONFIG_APPS: ["VIM Artifact Bin File", "VIM Service Definition Config"]
}
DEFAULT_SYNC_APPS = {
    CALIBRATION_APPS: ["Illumination Calibration", "Audio Calibration"],
}
DEFAULT_APPS = {
    ECG1: DEFAULT_ECG_APPS,
    ECG2: DEFAULT_ECG_APPS,
    TCU1: {},
    TCU2: {},
    PHOENIX: {},
    SYNC: DEFAULT_SYNC_APPS,

}
DEFAULT_SETTINGS = {
    FILE_UPLOAD_LIST: {},
    SUPPORTED_DOMAIN_INSTANCES: {},
    SUPPORTED_ECU_APPS: {
        x: DEFAULT_APPS[x] for x in DEFAULT_APPS
    }
}
CALIBRATION_INFO = {
    "Illumination Calibration": {
        BASE_PART_NUMBER: "14J003"
    },
    "Audio Calibration": {
        BASE_PART_NUMBER: "14G680"
    }
}
# GUI ONLY
INVALID_URL_MSG = "Invalid Build URL!"
FOCUS_OUT_EVENT_NAME = "{0}: FocusOut"  # objectName: FocusOut
VALID_Q_LABEL = '''
    QLabel {
        color: black
    }
'''
INVALID_Q_LABEL = '''
    QLabel {
        color: red
    }
'''
Q_START_BUTTON_STYLE = '''
    QPushButton {
        border-style: outset;
        background-color: green;
        border-radius: 15;
        border : 2px solid blue;
        border-color: blue;
        font-weight: bold;
        color: white;
    }
'''
Q_STOP_BUTTON_STYLE = '''
    QPushButton {
        border-style: outset;
        background-color: red;
        border-radius: 15;
        border : 2px solid blue;
        border-color: blue;
        font-weight: bold;
        color: white;
    }
'''
INVALID_BUILD_URL = "invalid_build_url"
INVALID_SOURCE_URL = "invalid_source_url"
INVALID_DESTINATION_URL = "invalid_destination_url"
ALL_BUILD_TYPES = ["Release", "Development", "Production", "Debug"]
ADDITIONAL_PROGRAMS = "additional_programs"
PROGRAM = "program"
VARIANT = "variant"
MODEL_TYPE = "model_type"
MODEL_YEAR = "model_year"
ECG1_VMCU = "ECG_VMCU_"
ECG2_VMCU = "ECG2_VMCU_"
VMCU_TYPES = {
    ECG1: ECG1_VMCU,
    ECG2: ECG2_VMCU
}
# https://sync-build.ford.com/job/SYNC4/job/PullRequests/job/Sync4-PR-FNV_cpm/144/artifact/buildroot/output/images/publish/AAA_Readme.html
#
VALID_URL_PATTERN = r"((http|https)://)(www.)?([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
URL_FORMS = ["lastSuccessfulBuild", "lastStableBuild", "lastBuild", "lastCompletedBuild"]
URL_PATTERN_BUILD_TYPE = {
    ECG1: {
        RELEASE: r"(?i)release",
        PRODUCTION: r"(?i)production",
        DEBUG: r"(?i)debug"
    },
    ECG2: {
        RELEASE: r"(?i)release",
        PRODUCTION: r"(?i)production",
        DEBUG: r"(?i)debug"
    },
    TCU1: {
        RELEASE: r"(?i)release",
        PRODUCTION: r"(?i)production",
        DEBUG: r"(?i)debug"
    },
    TCU2: {
        RELEASE: r"(?i)release",
        PRODUCTION: r"(?i)production",
        DEBUG: r"(?i)debug"
    },
    SYNC: {
        DEVELOPMENT: r"Sync4-master|Sync4-launch-SYNC",
        PRODUCTION: r"(?i)production|signing"
    },
    PHOENIX: {
        DEVELOPMENT: r"(?i)Integrations"
    }
}
URL_PATTERN_ECU_TYPE = {
    ECG2: "(?i)ECG2",
    ECG1: "(?i)(?=(ECG[1/_-]+))(?=(.(?<!ECG2))*?$)",
    TCU2: "(?i)TCU2|modem6",
    TCU1: "(?i)TCU[1/_-]+",
    SYNC: "(?i)SYNC4",
    PHOENIX: "(?i)phoenix|phx_aosp"
}
MODEL_YEAR_PATTERN = "MY[_0-9]*"
"""
SAMPLE VALUES to auto add support for ECG program:
program = CD764
variant = MY22_GASD
model_year = MY22
model_type = GASD
"""
BUILD_NUMBER_PATTERN = r".*-([0-9]+)"
ECG_VMCU_TEMPLATE = [
    "ECG[0-9]*_VMCU_{program}_{variant} ", "(ECG[0-9]*_VMCU_{program}_{model_year})(_{model_type}[.-_A-Z0-9]*)? ",
    r"(?=[_A-Z0-9]*{additional_programs}[_A-Z0-9]* )([_A-Z0-9]+{program}[.-_A-Z0-9]*{model_type}[.-_A-Z0-9]* )",
    "ECG[0-9]*_VMCU_{program} ",
]
ADDITIONAL_FILTERS = {
    PROGRAM: r"([_A-Z0-9]{4,10}(?=X{1}))"
}
ADDITIONAL_VMCU_TEMPLATES = {
    ECG: {
        "P702": ["ECG[0-9]*_VMCU_{model_type} "],
        "CD764": [r"(?i)(?=[_A-Z0-9]*{additional_programs}[_A-Z0-9]* )([_A-Z0-9]*{program}[_A-Z0-9]*) "],
    },
}
VMCU_TEMPLATE = {
    ECG: ECG_VMCU_TEMPLATE,
}
START = "Start"
STOP = "Stop"
IGNORE_FILE_EXT_LIST = [
    ".img", ".signed", ".ext4", ".sig", ".squashfs-lzo", ".verity"]
# Use to auto add new domain instances
AP_ONLY_DOMAIN_NAME = "{ecu}-{build_type}_AP_ONLY"
CP_ONLY_DOMAIN_NAME = "{ecu}-{build_type}_{vmcu_info}_CP_ONLY"
AP_CP_ONLY_DOMAIN_NAME = "{ecu}-{build_type}_{vmcu_info}_AP_CP_ONLY"
ALL_FILES_DOMAIN_NAME = "{ecu}-{build_type}_{vmcu_info}_ALL_FILES"
SYNC_AP_ONLY_DOMAIN_NAME = "{ecu}-{high_low}_AP_ONLY"
SYNC_CP_ONLY_DOMAIN_NAME = "{ecu}-{build_type}_{high_low}_CP_ONLY"
SYNC_AP_CP_DOMAIN_NAME = "{ecu}-{build_type}_{high_low}_AP_CP"
SYNC_ALL_FILES_DOMAIN_NAME = "{ecu}-{build_type}_{high_low}_ALL_FILES"
ECG_AP_ONLY_OBJECT_NAME = "{ecu}_{build_type}_AP_ONLY"
ECG_CP_ONLY_OBJECT_NAME = "{ecu}_{build_type}_{vmcu_info}_CP_ONLY"
ECG_AP_CP_OBJECT_NAME = "{ecu}_{build_type}_{vmcu_info}_AP_CP"
ECG_AP_CP_VIM_OBJECT_NAME = "{ecu}_{build_type}_{program}_{variant}_AP_CP_VIM"
ECG_ALL_FILES_OBJECT_NAME = "{ecu}_{build_type}_{program}_{variant}_ALL_FILES"
ECG_ALL_FILES_F16B_OBJECT_NAME = "{ecu}_{build_type}_{program}_{variant}_F16B_ALL_FILES"
SYNC_ALL_FILES_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_ALL_FILES"
SYNC_CORE_FILES_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_CORE_FILES"
SYNC_ALL_FILES_APPS_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_APPS"
SYNC_CORE_FILES_MAPS_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_MAPS"
SYNC_AP_ONLY_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_AP_ONLY"
SYNC_CP_ONLY_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_CP_ONLY"
SYNC_CP_CALIBRATION_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_CP_CALIBRATION"
SYNC_AP_CP_OBJECT_NAME = "{ecu}_{build_type}_{variant_type}_AP_CP"
DOMAIN_INSTANCE_GROUPS = ["AP_ONLY", "CP_ONLY", "AP_CP", "ALL_FILES"]
ECG_DOMAIN_INSTANCE_GROUPS = ["AP_CP_VIM"]
SYNC_DOMAIN_INSTANCE_GROUPS = ["CORE_FILES", "APPS", "MAPS", "CALIBRATION"]
ECG1_AP_ONLY_TEMPLATE = {
    ECU: ECG1,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: AP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG1 - {build_type} AP ONLY",
    FILES: [CCPU],
    STATUS: "pending"
}
ECG1_CP_ONLY_TEMPLATE = {
    ECU: ECG1,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG1 - {build_type} {vmcu_info} CP ONLY",
    FILES: [VMCU],
    STATUS: "pending"
}
ECG1_AP_CP_ONLY_TEMPLATE = {
    ECU: ECG1,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: AP_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG1 - {build_type} {vmcu_info} AP & CP ONLY",
    FILES: [VMCU, CCPU],
    STATUS: "pending"
}
ECG1_AP_CP_VIM_TEMPLATE = {
    ECU: ECG1,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [VIM_ARTIFACTS],
    BUILD: "{build}",
    NAME: AP_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG1 - {build_type} {program} {model_year} {model_type} AP & CP + VIM",
    FILES: [VMCU, CCPU],
    STATUS: "pending"
}
ECG1_ALL_FILES_TEMPLATE = {
    ECU: ECG1,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [VIM_ARTIFACTS],
    BUILD: "{build}",
    NAME: ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "ECG1 - {build_type} {program} {model_year} {model_type} All Files + VIM",
    FILES: [CCPU_BOOTLOADER, VMCU, VMCU_BOOTLOADER, CCPU],
    STATUS: "pending"
}
ECG2_AP_ONLY_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: AP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} AP ONLY",
    FILES: [CCPU],
    STATUS: "pending"
}
ECG2_CP_ONLY_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} {vmcu_info} CP ONLY",
    FILES: [VMCU],
    STATUS: "pending"
}
ECG2_AP_CP_ONLY_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [],
    BUILD: "{build}",
    NAME: AP_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} {vmcu_info} AP & CP ONLY",
    FILES: [VMCU, CCPU],
    STATUS: "pending"
}
ECG2_AP_CP_VIM_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [VIM_ARTIFACTS],
    BUILD: "{build}",
    NAME: AP_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} {program} {model_year} {model_type} AP & CP + VIM",
    FILES: [VMCU, CCPU],
    STATUS: "pending"
}
ECG2_ALL_FILES_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [VIM_ARTIFACTS],
    BUILD: "{build}",
    NAME: ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} {program} {model_year} {model_type} All Files + VIM",
    FILES: [CCPU_BOOTLOADER, VMCU, CCPU],
    STATUS: "pending"
}
ECG2_ALL_FILES_F16B_TEMPLATE = {
    ECU: ECG2,
    VIM_FOLDER: [],
    VMCU_FOLDER: "",
    VARIANT: "{program}",
    CONTAIN_APPS: [VIM_ARTIFACTS, F16B],
    BUILD: "{build}",
    NAME: ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "ECG2 - {build_type} {program} {model_year} {model_type} All Files + VIM & F16B",
    FILES: [CCPU_BOOTLOADER, VMCU, CCPU],
    STATUS: "active"
}
SYNC_AP_ONLY_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [],
    VARIANT: "{variant}",
    NAME: SYNC_AP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} AP Only",
    FILES: [CCPU],
    STATUS: "pending"
}
SYNC_CP_ONLY_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [],
    VARIANT: "{variant}",
    NAME: SYNC_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} CP Only",
    FILES: [VMCU],
    STATUS: "pending"
}
SYNC_CP_CALIBRATION_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [CALIBRATION_FILES],
    VARIANT: "{variant}",
    NAME: SYNC_CP_ONLY_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} CP + Calibration",
    FILES: [VMCU],
    STATUS: "pending"
}
SYNC_AP_CP_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [],
    VARIANT: "{variant}",
    NAME: SYNC_AP_CP_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} AP & CP",
    FILES: [VMCU, CCPU],
    STATUS: "pending"
}
SYNC_CORE_FILES_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [],
    VARIANT: "{variant}",
    NAME: SYNC_ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} Core Files",
    FILES: [CCPU_BOOTLOADER, VMCU, VMCU_BOOTLOADER, CCPU],
    STATUS: "pending"
}
SYNC_ALL_FILES_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [CALIBRATION_FILES],
    VARIANT: "{variant}",
    NAME: SYNC_ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {vmcu_info} All Files",
    FILES: [CCPU_BOOTLOADER, VMCU, VMCU_BOOTLOADER, CCPU],
    STATUS: "pending"
}
SYNC_ALL_FILES_APPS_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [CALIBRATION_FILES, APPS],
    VARIANT: "{variant}",
    NAME: SYNC_ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {variant_info} All Files + Apps",
    FILES: [CCPU_BOOTLOADER, VMCU, VMCU_BOOTLOADER, CCPU],
    STATUS: "pending"
}
SYNC_CORE_FILES_MAPS_TEMPLATE = {
    ECU: "SYNC",
    BUILD: "{build}",
    CONTAIN_APPS: [MAPS],
    VARIANT: "{variant}",
    NAME: SYNC_ALL_FILES_DOMAIN_NAME,
    DESCRIPTION: "SYNC - {build_type} {variant_info} Core Files + Maps",
    FILES: [CCPU_BOOTLOADER, VMCU, VMCU_BOOTLOADER, CCPU],
    STATUS: "pending"
}
DOMAIN_INSTANCE_TEMPLATES = {
    ECG1: {
        ECG_AP_ONLY_OBJECT_NAME: [ECG1_AP_ONLY_TEMPLATE],
        ECG_CP_ONLY_OBJECT_NAME: [ECG1_CP_ONLY_TEMPLATE],
        ECG_AP_CP_OBJECT_NAME: [ECG1_AP_CP_ONLY_TEMPLATE],
        ECG_AP_CP_VIM_OBJECT_NAME: [ECG1_AP_CP_VIM_TEMPLATE],
        ECG_ALL_FILES_OBJECT_NAME: [ECG1_ALL_FILES_TEMPLATE]
    },
    ECG2: {
        ECG_AP_ONLY_OBJECT_NAME: [ECG2_AP_ONLY_TEMPLATE],
        ECG_CP_ONLY_OBJECT_NAME: [ECG2_CP_ONLY_TEMPLATE],
        ECG_AP_CP_OBJECT_NAME: [ECG2_AP_CP_ONLY_TEMPLATE],
        ECG_AP_CP_VIM_OBJECT_NAME: [ECG2_AP_CP_VIM_TEMPLATE],
        ECG_ALL_FILES_OBJECT_NAME: [ECG2_ALL_FILES_TEMPLATE],
        ECG_ALL_FILES_F16B_OBJECT_NAME: [ECG2_ALL_FILES_F16B_TEMPLATE]
    },
    SYNC: {
        SYNC_CORE_FILES_OBJECT_NAME: [SYNC_CORE_FILES_TEMPLATE],
        SYNC_ALL_FILES_OBJECT_NAME: [SYNC_ALL_FILES_TEMPLATE],
        SYNC_ALL_FILES_APPS_OBJECT_NAME: [SYNC_ALL_FILES_APPS_TEMPLATE],
        SYNC_CORE_FILES_MAPS_OBJECT_NAME: [SYNC_CORE_FILES_MAPS_TEMPLATE],
        SYNC_AP_ONLY_OBJECT_NAME: [SYNC_AP_ONLY_TEMPLATE],
        SYNC_CP_ONLY_OBJECT_NAME: [SYNC_CP_ONLY_TEMPLATE],
        SYNC_CP_CALIBRATION_OBJECT_NAME: [SYNC_CP_CALIBRATION_TEMPLATE],
        SYNC_AP_CP_OBJECT_NAME: [SYNC_AP_CP_TEMPLATE],
    }
}
SYNC_NO_MAPS = [
    "8GB[-_A-Z]*MAPS", "16GB[-_A-Z]*MAPS", "32GB_EUROPE_MAPS",
    "NO[_N]*NAV_MAPS"
]
INVALID_VARIANCE = ["[-_a-zA-Z0-9]*Developer[-_a-zA-Z0-9]*"]
# Manually Replace Software Part Numbers
REPLACEMENT_FILES = {
    "ZU5T-14H085-ABC00460 1.7.5.460": "ZU5T-14H085-ABC00470.vbf",
    "MU5T-14H090-BAZ 1.8.2.4": "MU5T-14H090-BAZ.vbf",
    "ZU5T-14H241-AAT00082 1.10.0.82": "ZU5T-14H241-AAT00083.vbf",
    STORAGE_URL: {
        "ZU5T-14H085-ABC00470.vbf": "https://vadrprod5n4uo3wfyfkyu.blob.core.windows.net/software/15bd4212-9e3d-4547-85ab-5a51f718c478_ZU5T-14H085-ABC00470.vbf",
        "MU5T-14H090-BAZ.vbf": "https://vadrprod5n4uo3wfyfkyu.blob.core.windows.net/software/df5430fe-8776-4b99-9018-7655c7bc8a73_MU5T-14H090-BAZ.vbf",
        "ZU5T-14H241-AAT00083.vbf": "https://vadrprod5n4uo3wfyfkyu.blob.core.windows.net/software/2c0d8677-cdef-4e28-b8a5-293062e6c409_ZU5T-14H241-AAT00083.vbf",
    }
}
# ProjectManager
PAST_JOBS_LIMIT = 20
PENDING_TASKS = "PENDING_TASKS"
REQUESTED_BY = "REQUESTED_BY"
TIME_REQUESTED = "TIME_REQUESTED"
PROCESSED_BY = "PROCESSED_BY"
TIME_STARTED = "TIME_STARTED"
TIME_COMPLETED = "TIME_COMPLETED"
TOTAL_TIME = "TOTAL_TIME"
ADDED_BY = "ADDED_BY"
# Status Objects
TIMER = "timer"
FILE_UPLOAD_STATUS = "file_upload_status"
DOMAIN_INSTANCE_STATUS = "domain_instance_status"
APPLICATION_STATUS = "application_status"
SWS_STATUS = "sws_status"
UPLOAD_SPEED = "upload_speed"
DOWNLOAD_SPEED = "download_speed"
IP_ADDRESS = "ip_address"
NETWORK = "network"
KWARGS = "kwargs"
ARGS = "args"
NODE = "node"
START_TIME = "start_time"
END_TIME = "end_time"
TIME_ELAPSED = "time_elapsed"
FAILURE_REASON = "failure_reason"
IP_API = "https://api.ipify.org"
JOB_ARGS = [
    SEQUENCE_NAME, NEXT_BUILD_URL, SOURCE_URL, NEXT_SOURCE_URL, DESTINATION_URL,
    BUILD_NUMBER, SOURCE_BUILD, UPLOAD_FILES_ONLY, RELEASE_FILES, ADD_LINEAGE,
    CREATE_DIFFERENTIAL_FILES, USE_REAL_APP_NAMES, OVERWRITE_DB, APPS_LIST, ADDED_BY
]
REQUIRED_JOB_ARGS = [
    ECU, BUILD, BUILD_URL, DOMAIN_INSTANCES, COLUMN_NAME
]
# DB Tables
PENDING_JOBS = "PENDING_JOBS"
UPLOAD_STATUS = "UPLOAD_STATUS"


def update_workstation():
    global WORKSTATION
    global LOGS_FOLDER
    WORKSTATION = os.path.join(WORKING_DIR, f"{PC_NAME}_{timegm(time.gmtime())}")
    LOGS_FOLDER = os.path.join(WORKSTATION, 'logs')
    # Create directory to store downloaded files if none exist.
    if not os.path.exists(WORKSTATION):
        os.mkdir(WORKSTATION)
    # Create directory to store system logs if none exist.
    if not os.path.exists(LOGS_FOLDER):
        os.mkdir(LOGS_FOLDER)
    # Create directory to store pending part ii specs upload.
    if not os.path.exists(PART_II_SPECS):
        os.mkdir(PART_II_SPECS)
    # Create directory to store testing logs if none exist.
    if not os.path.exists(TESTS_FOLDER):
        os.mkdir(TESTS_FOLDER)


def get_workstation():
    return WORKSTATION


def get_logs_folder():
    return LOGS_FOLDER


class JiraProject:
    """
    Class to hold available Jira projects and related constants
    """
    ECG = 'ECG'
    TCU = 'TCU'
    SYNC = 'SYNC'
    FNV = 'FNV'
    TAT = 'TAT'
    AOS = 'AOS'


class JiraPriority:
    """
    Class to hold available Jira priority and related constants
    """
    IMMEDIATE_GATING = "Immediate Gating"
    GATING = "Gating"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    BLOCKER = "Blocker"
    NOT_SET = "Not Set"
    NONE = "None"


class JiraSeverity:
    """
    Class to hold available Jira severity and related constants
    """
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"
    LOW = "Low"
    NONE = "None"


class JiraComponent:
    """
    Class to hold available Jira component and related constants
    """
    SWUM = "SWUM"
    MMOTA_TRIAGE = "MMOTA Triage"
    CLOUD_MMOTA = "Cloud MMOTA"


class JiraLabel:
    """
    Class to hold available Jira label and related constants
    """
    CLOUD_MANAGER = "SWUM-Cloud-Manager"
    SWUM_SSIT_BUILD = "SWUM_SSIT_Build"


class JiraIssueType:
    """
    Class to hold available Jira issue types and related constants
    """
    DEFECT = "Defect"
    STORY = "Story"
    EPIC = "Epic"
    TASK = "Task"
    REQUIREMENT = "Requirement"
    HIGH_LEVEL_DESIGN = "High Level Design"


class JiraTestEnv:
    """
    Class to hold available Jira test environment and related constants
    """
    NONE = "None"
    OFF_TARGET = "Off-Target (VM)"
    ON_TARGET = "On-Target (ECU Standalone)"
    BENCHES = "Sub-System (Benches)"
    BREAD_BOARD = "System: HiL, Breadboard, Vehicle"
    TEST_STATION = "Mfg Test Station"
    PRE_POST_TEST_STATION = "Pre and Post reliability test station"
    MONITORING_STATION = "Monitoring test station"


class JiraPlatform:
    """
    Class to hold applicable Jira platform and related constants
    """
    ECG1 = "ECG1.0 (5/8+1 port)"
    NAV_VOICE_64GB = "Nav and Voice - 64GB Variant"
    NAV_VOICE_32GB = "Nav and Voice - 32GB Variant"
    NO_NAV_VOICE_16GB = "No Nav/Voice- 16GB Variant"
    NO_NAV_NO_VOICE_8GB = "No Nav/No Voice 8GB Variant"
    OTHER = "Other"


class DomainInstance:
    """
    ecu: Type of ECU Module
    program: name of root folder with ECG VIM artifact files
    vim_folder: name of sub folder with ECG VIM artifact files
    vmcu_folder: name of folder with VMCU files
    contain_apps: type of application associated with domain instance.
    build: type of domain instance
    name: name of domain instance
    description: description of files in the domain instance
    files: list of file types in the domain instance
    """

    def __init__(self, domain_instance=None):
        self.domain_instance = {}
        if isinstance(domain_instance, dict):
            self.domain_instance = domain_instance

    def __str__(self):
        text = json.dumps(self.domain_instance, indent=4)
        return text

    @property
    def name(self):
        return self.domain_instance.get(NAME)

    @name.setter
    def name(self, domain_instance_name):
        self.domain_instance[NAME] = domain_instance_name

    @property
    def ecu(self):
        return self.domain_instance.get(ECU)

    @ecu.setter
    def ecu(self, ecu):
        self.domain_instance[ECU] = ecu

    @property
    def variant(self):
        return self.domain_instance.get(VARIANT)

    @variant.setter
    def variant(self, variant):
        self.domain_instance[VARIANT] = variant

    @property
    def vim_folder(self):
        return self.domain_instance.get(VIM_FOLDER)

    @vim_folder.setter
    def vim_folder(self, vim_folder):
        if isinstance(vim_folder, list):
            self.domain_instance[VIM_FOLDER] = vim_folder
        else:
            msg = f"Expected {type(list)} for vim. Received {type(vim_folder)}"
            raise ValueError(msg)

    @property
    def vmcu_folder(self):
        return self.domain_instance.get(VMCU_FOLDER)

    @vmcu_folder.setter
    def vmcu_folder(self, vmcu_folder):
        self.domain_instance[VMCU_FOLDER] = vmcu_folder

    @property
    def contain_apps(self):
        return self.domain_instance[CONTAIN_APPS]

    @contain_apps.setter
    def contain_apps(self, apps_list):
        if isinstance(apps_list, list):
            self.domain_instance[CONTAIN_APPS] = apps_list
        else:
            msg = f"Expected {type(list)} for apps. Received {type(apps_list)}"
            raise ValueError(msg)

    @property
    def build(self):
        return self.domain_instance.get(BUILD)

    @build.setter
    def build(self, build):
        self.domain_instance[BUILD] = build

    @property
    def android_guest(self):
        return self.domain_instance.get(ANDROID_GUEST)

    @android_guest.setter
    def android_guest(self, android_guest):
        self.domain_instance[ANDROID_GUEST] = android_guest

    @property
    def description(self):
        return self.domain_instance.get(DESCRIPTION)

    @description.setter
    def description(self, description):
        self.domain_instance[DESCRIPTION] = description

    @property
    def files(self):
        return self.domain_instance.get(FILES)

    @files.setter
    def files(self, files):
        if isinstance(files, list):
            self.domain_instance[FILES] = files
        else:
            msg = f"Expected {type(list)} for files. Received: {type(files)}"
            raise ValueError(msg)

    @property
    def status(self):
        return self.domain_instance.get(STATUS)

    @status.setter
    def status(self, status):
        self.domain_instance[STATUS] = status

    @property
    def keys(self):
        return self.domain_instance.keys()


class NexusConfig:
    NEXUS_URL = "https://www.nexus.ford.com/repository"
    NEXUS_FETCH_REPOSITORY = "fnv2-private-maven-group"
    NEXUS_FETCH_REPOSITORY_PRODUCTION = "fnv2_private_release_repository"
    SYNC_CCPU_BL_BASE_URL = "https://www.nexus.ford.com/repository/fnv2-private-maven-group/com/ford/sync/bootloader"
    SYNC_MID_HIGH_CCPU_BL_DESCRIPTION = "u-boot-40-h"
    SYNC_LC_CCPU_BL_DESCRIPTION = "u-boot-40-l"
    NEXUS_REPOSITORIES = {
        DEVELOPMENT: NEXUS_FETCH_REPOSITORY,
        PRODUCTION: NEXUS_FETCH_REPOSITORY_PRODUCTION
    }


class VadrConfig:
    SYNC_MANIFEST_SUFFIX = "/output/images/publish/sync_manifest.json"
    EXCLUDED_SYNC_APPS = [
        "alm-pkg-DigitalOwnersManual",
        "alm-pkg-Telenav-Test-App",
        "alm-pkg-Garmin-Test-App",
    ]
    SOFTWARE_MANIFEST_KEYS = {
        'ECG1': {
            'VMCU_BOOTLOADER': ["VMCU_BOOTLOADER_FPN"],
            'CCPU_BOOTLOADER': ['BOOTLOADER_FPN', 'BOOTLOADER_DEV_SECURE_FPN',
                                'BOOTLOADER_INSECURE_FPN'],
            'CCPU': ["AP_FPN"],
            'VMCU': {
                "ECG_VMCU_HEV": ["HEV_BASE_FPN", "VMCU_HEV_FPN"],
                "ECG_VMCU_GASD": ["GASD_BASE_FPN", "VMCU_GASD_FPN"],
                "ECG_VMCU_CX727": ["CX727_BASE_FPN", "VMCU_CX727"],
                "ECG_VMCU_U725": ["U725_BASE_FPN"],
                "ECG_VMCU_CD539": ["CD539_BASE_FPN"],
                "ECG_VMCU_MULE_P552": ["MULE_P552_BASE_FPN"],
                "ECG_VMCU_MULE_U55X": ["MULE_U55X_BASE_FPN"],
                "ECG_VMCU_MULE_U540": ["MULE_U540_BASE_FPN"],
                "ECG_VMCU_MULE_C519": ["MULE_C519_BASE_FPN"],
                "ECG_VMCU_MULE_U625": ["MULE_U625_BASE_FPN"],
                "ECG_VMCU_P702_MY22_BEV": ["P702_MY22_BEV_BASE_FPN"],
                "ECG_VMCU_CX482AV_MY23_Z2": ["CX482AV_MY23_Z2_BASE_FPN"],
                "ECG_VMCU_U55X_MY22_GAS": ["U55X_MY22_GAS_BASE_FPN"],
                "ECG_VMCU_P703_U704_MY21_GASD": [
                    "P703_U704_MY21_GASD_BASE_FPN"],
                "ECG_VMCU_P558_MY22_ICA": ["P558_MY22_ICA_BASE_FPN"],
                "ECG_VMCU_V710_MY23_5_BASE": ["V710_MY23_5_BASE_BASE_FPN"],
                "ECG_VMCU_C519_MY22_5_MCA": ["C519_MY22_5_MCA_BASE_FPN"],
                "ECG_VMCU_V363_MY22_BEV": ["V363_MY22_BEV_BASE_FPN"],
                "ECG_VMCU_P708_MY23_BASE": ["P708_MY23_BASE_BASE_FPN"],
                "ECG_VMCU_CX482_MY23_MCA": ["CX482_MY23_MCA_BASE_FPN"],
                "ECG_VMCU_V710_MY23_DIESEL": ["V710_MY23_DIESEL_BASE_FPN"],
                "ECG_VMCU_S650_MY23_BASE": ["S650_MY23_BASE_BASE_FPN"],
                "ECG_VMCU_CD542_GASD": ["CD542_GASD_BASE_FPN"],
            }
        },
        'ECG2': {
            'VMCU_BOOTLOADER': [],
            'CCPU_BOOTLOADER': [],
            'CCPU': [],
            'VMCU': {
                "ECG2_VMCU_HEV": ["ECG2_VMCU_HEV_BASE_FPN"],
                "ECG2_VMCU_GASD": ["ECG2_VMCU_GASD_BASE_FPN"],
                "ECG2_VMCU_P708_MY23_BASE": ["P708_MY23_BASE_FPN"],
                "ECG2_VMCU_CX727": ["CX727_BASE_FPN", "VMCU_CX727"],
                "ECG2_VMCU_CX482_MY23_MCA": ["CX482_MY23_MCA_BASE_FPN"],
                "ECG2_VMCU_CX482AV_MY23_Z2": ["CX482AV_MY23_Z2_BASE_FPN"],
                "ECG2_VMCU_CDX706_MY23_GASHEV": [
                    "CDX706_MY23_GASHEV_BASE_FPN"],
                "ECG2_VMCU_CDX707_MY23_BASE": ["CDX707_MY23_BASE_FPN"],
                "ECG2_VMCU_S650_MY23_BASE": ["S650_MY23_BASE_FPN"],
                "ECG2_VMCU_V710_MY23": ["V710_MY23_BASE_FPN"],
            }
        }
    }
    # category = [APPLICATION, PRIMARY_BOOTLOADER, STRATEGY, SCRIPTING_APPLICATION, CALIBRATION, IMAGE,
    # ECU_CONFIGURATION, SECONDARY_BOOTLOADER, BOOT_IMAGE]
    # programmingMethods = []
    # responseOnFailedActivation = "NONE", or "REDUCED_FUNCTIONALITY"
    # TO DO - Remove VADR_DOMAIN_SETTINGS (Not Used)
    VADR_DOMAIN_SETTINGS = {
        "ECG": {
            "domainName": "Enhanced Central Gateway",
            "core_hardware": {
                'PROTOTYPE': {
                    'MU5T-14H026-AA': 10, 'AAAA-Information': 22, 'NRC': 23,
                    'NRC_716': 29, 'MU5T-14H026-AD': 68, 'MU5T-14H026-AB': 69,
                    'MU5T-14G650-ABE': 72, 'MU5T-14H026-AF': 81,
                    'MU5T-14G650-ABC': 89,
                    'MU5T-14H026-AE': 94, 'MU5T-14G650-AAA': 113,
                    'MU5T-14H026-AF1': 134,
                    'MU5T-14H026-AC': 173,
                    'MU5T-14H026-AG1': 176, 'MU5T-14H026-AG': 262,
                    'MU5T-14H026-AH': 296,
                    'NU5T-14H026-AC': 303,
                    'MU5T-14H026-DA': 304, 'NUGT-14H026-AB': 310,
                    'NU5T-14H026-AC1': 334,
                    'NU5T-14H026-AB1': 389,
                    'NU5T-14H026-EA': 399, 'MU5T-14H026-AH1': 400,
                    'MU5T-14H026-DA1': 420,
                    'ZU5T-14H027-EAA09853': 426},
                'PRODUCTION': {'MU5T-14H026-AA': 10, 'MU5T-14H026-AD': 68,
                               'MU5T-14H026-AB': 69, 'MU5T-14G650-ABE': 72,
                               'MU5T-14H026-AF': 81, 'MU5T-14G650-ABC': 89,
                               'MU5T-14H026-AE': 94,
                               'MU5T-14G650-AAA': 113,
                               'MU5T-14H026-AC': 173, 'MU5T-14H026-AG': 262,
                               'MU5T-14H026-AH': 296,
                               'NU5T-14H026-AC': 303,
                               'MU5T-14H026-DA': 304, 'NUGT-14H026-AB': 310,
                               'NU5T-14H026-EA': 399}
            }
        },
        "TCU": {
            "domainName": "Embedded Modem B5+",
            "core_hardware": {
                'PROTOTYPE': {'HJ5T-14G145-MB': 9, 'MU5T-14H089-AA': 24,
                              'NRC_754': 27, 'ZU5T-14H109-AAC031': 31,
                              'MU5T-14H074-AAA': 45, 'MU5T-14H089-AB': 59,
                              'MU5T-14H089-NA': 71, 'MU5T-14H074-AAF': 76,
                              'MU5T-14H074-AAC': 78, 'MU5T-14H089-AAF': 82,
                              'MU5T-14H089-0E': 83, 'MU5T-14H089-CA': 84,
                              'MU5T-14H089-ND': 96, 'MU5T-14H089-KD': 102,
                              'K4B9-14G145-AC': 104, 'K4B9-14G145-AB': 105,
                              'K4B9-14G145-AD': 106, 'MU5T-14H089-AE': 111,
                              'MU5T-14H089-NB': 112,
                              'MU5T-14H089-NC': 124,
                              'MU5T-14H089-CAF': 125, 'MU5T-14H089-AC': 126,
                              'K4B9-14G145-AE': 133,
                              'MU5T-14H089-AAG': 136,
                              'MU5T-14H089-BE': 141, 'L2E9-14G145-BA': 148,
                              'L2E9-14G087-BA': 149,
                              'MU5T-14H089-AAJ': 152,
                              'MU5T-14H089-BAJ': 154, 'MU5T-14H089-CAJ': 155,
                              'MU5T-14H089-HAJ': 156,
                              'MU5T-14H089-KAJ': 157,
                              'MU5T-14H089-NAJ': 158, 'MU5T-14H089-MAJ': 159,
                              'MU5T-14H089-NAF': 175,
                              'MU5T-14H089-NAE': 199,
                              'NU5T-14H089-NAE': 200, 'NU5T-14H089-BAE': 201,
                              'NU5T-14H089-MAE': 202,
                              'MU5T-14H089-BAF': 212,
                              'MU5T-14H089-0C': 216, 'MU5T-14H089-CB': 228,
                              'MU5T-14H089-BAE': 257,
                              'MU5T-14H089-MAE': 258,
                              'MU5T-14H089-NAG': 267, 'MU5T-14H089-NAH': 268,
                              'MU5T-14H089-AAH': 269,
                              'MU5T-14H089-AAK': 289,
                              'NU5T-14H074-NAH': 290, 'NU5T-14H089-BAF': 291,
                              'NU5T-14H089-MAF': 292,
                              'MU5T-14H089-CAK': 293,
                              'MU5T-14H089-NAK': 308, 'NU5T-14H089-NAF': 309,
                              'MU5T-14H089-CD': 320,
                              'NU5T-14H089-AAF': 324,
                              'NU5T-14H089-HAF': 325, 'NU5T-14H089-KAF': 328,
                              'NU5T-14H089-AAE1': 341,
                              'MU5T-14H089-MAG': 345,
                              'NU5T-14H089-VAF': 353, 'MU5T-14H089-JA': 356,
                              'MU5T-14H089-EAF': 361,
                              'MU5T-14H089-JE': 363,
                              'MU5T-14H089-AAJ1': 376, 'MU5T-14H089-BA': 383,
                              'NU5T-14H089-HAE1': 385,
                              'MU5T-14H089-EA': 391,
                              'MU5T-14H089-EBJ1': 401, 'MU5T-14H089-JBJ1': 416,
                              'MU5T-14H026-DA1': 421,
                              'NU5T-14H089-VAE1': 422, 'MU5T-14H089-NAK1': 427,
                              'NU5T-14H089-CAE1': 439,
                              'MU5T-14H089-613': 441},
                'PRODUCTION': {'HJ5T-14G145-MB': 9, 'MU5T-14H089-AA': 24,
                               'MU5T-14H074-AAA': 45, 'MU5T-14H089-AB': 59,
                               'MU5T-14H089-NA': 71, 'MU5T-14H074-AAF': 76,
                               'MU5T-14H074-AAC': 78,
                               'MU5T-14H089-AAF': 82,
                               'MU5T-14H089-0E': 83, 'MU5T-14H089-CA': 84,
                               'MU5T-14H089-ND': 96, 'MU5T-14H089-KD': 102,
                               'K4B9-14G145-AC': 104, 'K4B9-14G145-AB': 105,
                               'K4B9-14G145-AD': 106,
                               'MU5T-14H089-AE': 111,
                               'MU5T-14H089-NB': 112, 'MU5T-14H089-NC': 124,
                               'MU5T-14H089-CAF': 125,
                               'MU5T-14H089-AC': 126,
                               'K4B9-14G145-AE': 133, 'MU5T-14H089-AAG': 136,
                               'MU5T-14H089-BE': 141,
                               'L2E9-14G145-BA': 148,
                               'L2E9-14G087-BA': 149, 'MU5T-14H089-AAJ': 152,
                               'MU5T-14H089-BAJ': 154,
                               'MU5T-14H089-CAJ': 155,
                               'MU5T-14H089-HAJ': 156, 'MU5T-14H089-KAJ': 157,
                               'MU5T-14H089-NAJ': 158,
                               'MU5T-14H089-MAJ': 159,
                               'MU5T-14H089-NAF': 175, 'MU5T-14H089-NAE': 199,
                               'NU5T-14H089-NAE': 200,
                               'NU5T-14H089-BAE': 201,
                               'NU5T-14H089-MAE': 202, 'MU5T-14H089-BAF': 212,
                               'MU5T-14H089-0C': 216,
                               'MU5T-14H089-CB': 228,
                               'MU5T-14H089-BAE': 257, 'MU5T-14H089-MAE': 258,
                               'MU5T-14H089-NAG': 267,
                               'MU5T-14H089-NAH': 268,
                               'MU5T-14H089-AAH': 269, 'MU5T-14H089-AAK': 289,
                               'NU5T-14H074-NAH': 290,
                               'NU5T-14H089-BAF': 291,
                               'NU5T-14H089-MAF': 292, 'MU5T-14H089-CAK': 293,
                               'MU5T-14H089-NAK': 308,
                               'NU5T-14H089-NAF': 309,
                               'MU5T-14H089-CD': 320, 'NU5T-14H089-AAF': 324,
                               'NU5T-14H089-HAF': 325,
                               'NU5T-14H089-KAF': 328,
                               'MU5T-14H089-MAG': 345, 'NU5T-14H089-VAF': 353,
                               'MU5T-14H089-JA': 356,
                               'MU5T-14H089-EAF': 361,
                               'MU5T-14H089-JE': 363, 'MU5T-14H089-BA': 383,
                               'MU5T-14H089-EA': 391}
            }
        },
        "SYNC": {
            "domainName": "SYNC System",
            "core_hardware": {
                'PROTOTYPE': {'ZU5T-14G670-DAA001': 11, 'NRC_7d0': 28,
                              'MU5T-14G682-AE': 32, 'MU5T-14G682-AE0031': 37,
                              'MU5T-14G681-KB': 38, '6U5T-14G681-HAD': 39,
                              '7D0': 44, 'NRC0xd7': 46, 'test': 60,
                              '6U5T-14G681-HA': 61, '6U5T-14G681-CA': 70,
                              'MU5T-14G681-BB': 73, 'MU5T-14G681-CC': 74,
                              '6U5T-14G681-DA': 79, 'MU5T-14G681-DC': 80,
                              '6U5T-14G681-GA': 85, 'MU5T-14G681-KA': 86,
                              'MU5T-14G681-AC': 87, 'MU5T-14G681-AA': 88,
                              'MU5T-14G681-CE': 90, 'MU5T-14G681-BA': 95,
                              'MU5T-14G681-LC': 97, 'MU5T-14681-AD': 98,
                              'MU5T-14G681-AE': 99, 'MU5T-14G681-BC': 100,
                              '6U5T-14G670-CAA': 114, 'MU5T-14G681-DB': 115,
                              'MU5T-14G681-KE': 118,
                              'EJ5T-14F130-AA': 123,
                              'MU5T-14G681-DA': 131, 'MU5T-14G681-CB': 132,
                              'MU5T-14G681-LB': 135,
                              'MU5T-14G681-KF': 137,
                              'MU5T-14G681-KC': 139, 'MU5T-14G681-CA': 140,
                              '6U5T-14G681-FA': 147,
                              'MU5T-14G681-KF1': 166,
                              'ZU5T-14H236-CF': 167, 'MU5T-14G681-LF1': 169,
                              'MU5T-14G681-LA': 170,
                              'MU5T-14G681-CF': 180,
                              'MU5T-14G681-AG': 181, 'MU5T-14G681-BF': 182,
                              'MU5T-14G681-GA': 203,
                              'MU5T-14G681-AD': 204,
                              'MU5T-14G681-FA': 205, 'MU5T-14G682-CE': 210,
                              'MU5T-14H234-BC': 211,
                              'MU5T-14G681-BE': 215,
                              '6U5T-14G670-FAA': 226, '6U5T-14G681-LA': 265,
                              'MU5T-14G682-CH00920': 271,
                              'MU5T-14G680-AA0018': 272, 'MU5T-14G681-AF': 274,
                              '6U5T-14G681-DA6': 288,
                              'MU5T-14H212-FG': 298, 'MU5T-14G681-LF': 306,
                              'NU5T-14G681-KB1': 311,
                              'NU5T-14G681-KB': 333, 'MU5T-14G681-JA': 343,
                              'MU5T-14G681-JF': 357,
                              'MZ8T-14H370-MA': 358, 'MU5T-14G681-CF1': 378,
                              'MZ8T-14H370-LA': 379,
                              'NU5T-14G680-JB': 392, 'NU5T-14G681-JB': 393,
                              'NU5T-14G681-AB': 394,
                              'MU5T-14G681-BG': 402, 'MU5T-14G681-CG': 403,
                              'MU5T-14G681-JG': 404,
                              'MU5T-14G681-KG': 405, 'MU5T-14G681-LG': 406,
                              'NU5T-14G681-JC': 407,
                              'NU5T-14G681-KC': 408, 'MU5T-14G681-AH': 409,
                              'NU5T-14G681-AC': 410,
                              'MU5T-14H089-JE': 411, 'MU5T-14H089-EAF': 412,
                              'MU5T-14H089-EBJ1': 413,
                              'MZ8T-18D668-LA004': 415,
                              'MZ8T-14H370-MA006': 417,
                              'MZ8T-14H370-LA006': 418,
                              'NU5T-14G681-LB1': 440},
                'PRODUCTION': {'MU5T-14G682-AE': 32, 'MU5T-14G681-KB': 38,
                               '6U5T-14G681-HAD': 39, '6U5T-14G681-HA': 61,
                               '6U5T-14G681-CA': 70, 'MU5T-14G681-BB': 73,
                               'MU5T-14G681-CC': 74, '6U5T-14G681-DA': 79,
                               'MU5T-14G681-DC': 80, '6U5T-14G681-GA': 85,
                               'MU5T-14G681-KA': 86, 'MU5T-14G681-AC': 87,
                               'MU5T-14G681-AA': 88, 'MU5T-14G681-CE': 90,
                               'MU5T-14G681-BA': 95, 'MU5T-14G681-LC': 97,
                               'MU5T-14681-AD': 98, 'MU5T-14G681-AE': 99,
                               'MU5T-14G681-BC': 100, '6U5T-14G670-CAA': 114,
                               'MU5T-14G681-DB': 115, 'MU5T-14G681-KE': 118,
                               'EJ5T-14F130-AA': 123,
                               'MU5T-14G681-DA': 131,
                               'MU5T-14G681-CB': 132, 'MU5T-14G681-LB': 135,
                               'MU5T-14G681-KF': 137,
                               'MU5T-14G681-KC': 139,
                               'MU5T-14G681-CA': 140, '6U5T-14G681-FA': 147,
                               'ZU5T-14H236-CF': 167,
                               'MU5T-14G681-LA': 170,
                               'MU5T-14G681-CF': 180, 'MU5T-14G681-AG': 181,
                               'MU5T-14G681-BF': 182,
                               'MU5T-14G681-GA': 203,
                               'MU5T-14G681-AD': 204, 'MU5T-14G681-FA': 205,
                               'MU5T-14G682-CE': 210,
                               'MU5T-14H234-BC': 211,
                               'MU5T-14G681-BE': 215, '6U5T-14G670-FAA': 226,
                               '6U5T-14G681-LA': 265,
                               'MU5T-14G681-AF': 274,
                               'MU5T-14H212-FG': 298, 'MU5T-14G681-LF': 306,
                               'NU5T-14G681-KB': 333,
                               'MU5T-14G681-JA': 343, 'MU5T-14G681-JF': 357,
                               'MZ8T-14H370-MA': 358}
            }
        }
    }
    FILE_SETTINGS = {
        ECG: {
            # Supported Base Parts Number
            F16C_FILES: F16C_PART_NUMBERS,
            F10A_FILES: F10A_PART_NUMBERS,
            F16B_FILES: F16B_PART_NUMBERS,
            ECG1: {
                CCPU_BOOTLOADER: {
                    "did_address": "8068",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H152-[0-9a-zA-Z]+",
                    LOCATION: {
                        "release": [
                            "out/target/product/aarch64le-release/bootloader",
                            "out/target/product/aarch64le-debug/bootloader"],
                        PRODUCTION: [
                            "out/target/product/aarch64le-debug/bootloader",
                            "out/target/product/aarch64le-release/bootloader"],
                    },
                },
                VMCU_BOOTLOADER: {
                    "did_address": "D027",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H151-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/vmcu_bootloader"]
                },
                CCPU: {
                    "did_address": "8033",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H027-[0-9a-zA-Z]+",
                    "regex": r"out/target/product/aarch64le\-debug|release",
                    LOCATION: [
                        "out/target/product/aarch64le-release",
                        "out/target/product/aarch64le-debug"]
                },
                VMCU: {
                    "did_address": "F188",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H021-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product"],
                },
                VIM_ARTIFACTS: [
                    "out/target/product/aarch64le-debug",
                    "out/target/product/aarch64le-release"
                ]
            },
            ECG2: {
                CCPU_BOOTLOADER: {
                    "did_address": "8068",
                    "base_number": "14H481",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H481-[0-9a-zA-Z]+",
                    LOCATION: {
                        "release": ["out/target/product/bootloader/insecure"],
                        PRODUCTION: ["out/target/product/bootloader/secure"]
                    }
                },
                VMCU_BOOTLOADER: {
                    "did_address": "D027",
                    "base_number": "",
                    FILE_FILTER: "",
                    LOCATION: []
                },
                CCPU: {
                    "did_address": "8033",
                    "base_number": "14H486",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H486-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/ECG2_LINCD_WRLinux"]
                },
                VMCU: {
                    "did_address": "F188",
                    "base_number": "14H483",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H483-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/vmcu"],
                },
                VIM_ARTIFACTS: [
                    "out/target/product/ECG2_LINCD_WRLinux/perm",
                    "out/target/product/ECG2_LINCD_WRLinux/ggmt",
                ],
            },
            # VADR File Settings
            "F10A": {
                'didAddress': "F10A",
                "category": "ECU_CONFIGURATION",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                'swdlReflashTime': 100,
                'canfdSwdlReflashTime': 50
            },
            "F16B": {
                'didAddress': "F16B",
                "category": "ECU_CONFIGURATION",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                'swdlReflashTime': 100,
                'canfdSwdlReflashTime': 50,
            },
            "F16C": {
                'didAddress': "F16C",
                "category": "ECU_CONFIGURATION",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                'swdlReflashTime': 100,
                'canfdSwdlReflashTime': 50,
            },
            "8068": {
                "didAddress": "8068",
                "category": "BOOT_IMAGE",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 200,
                "canfdSwdlReflashTime": 100
            },
            "D027": {
                "didAddress": "D027",
                "category": "BOOT_IMAGE",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 200,
                "canfdSwdlReflashTime": 100
            },
            "8033": {
                "category": "IMAGE",
                "didAddress": "8033",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                'swdlReflashTime': 4500,
                'canfdSwdlReflashTime': 2500
            },
            "F188": {
                "category": "STRATEGY",
                "didAddress": "F188",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                'swdlReflashTime': 350,
                'canfdSwdlReflashTime': 150
            }
        },
        # TCU
        TCU: {
            TCU1: {
                # base part number & location
                CCPU_BOOTLOADER: {
                    "category": "",
                    "did_address": "8068",
                    "base_number": "14H240",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H240-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product"]},
                VMCU_BOOTLOADER: {
                    "category": "",
                    "did_address": "D027",
                    "base_number": "14H241",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H241-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/vmcu_bootloader"]},
                CCPU: {
                    "category": "",
                    "did_address": "F120",
                    "base_number": "14H090",
                    "destination": "KERNEL",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H090-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product"]},
                VMCU: {
                    "category": "",
                    "did_address": "F188",
                    "base_number": "14H085",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H085-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product"]},
                "modem": {
                    "category": "",
                    "did_address": "F121",
                    "base_number": "14H090",
                    "destination": "MODEM",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H090-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product"]},
            },
            TCU2: {
                # base part number & location
                CCPU_BOOTLOADER: {
                    "category": "",
                    "did_address": "8068",
                    "base_number": "14H478",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H478-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/sa515m"]},
                VMCU_BOOTLOADER: {
                    "category": "",
                    "did_address": "D027",
                    "base_number": "14H628",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H628-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/vmcu/bootloader"]},
                CCPU: {
                    "category": "",
                    "did_address": "F120",
                    "base_number": "14H477",
                    "destination": "KERNEL",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H477-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/sa515m"]},
                VMCU: {
                    "category": "",
                    "did_address": "F188",
                    "base_number": "14H413",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H413-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/vmcu"]},
                "modem": {
                    "category": "",
                    "did_address": "F121",
                    "base_number": "14H477",
                    "destination": "MODEM",
                    FILE_FILTER: r"[0-9a-zA-Z]+-14H477-[0-9a-zA-Z]+",
                    LOCATION: ["out/target/product/sa515m"]},
            },
            # VADR File Settings
            "8068": {
                "category": "BOOT_IMAGE",
                "didAddress": "8068",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 200,
                "canfdSwdlReflashTime": 200
            },
            "D027": {
                "category": "BOOT_IMAGE",
                "didAddress": "D027",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 200,
                "canfdSwdlReflashTime": 200
            },
            "F120": {
                "category": "STRATEGY",
                "didAddress": "F120",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 4500,
                "canfdSwdlReflashTime": 4500
            },
            "F188": {
                "category": "STRATEGY",
                "didAddress": "F188",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 350,
                "canfdSwdlReflashTime": 350
            },
            "F121": {
                "category": "STRATEGY",
                "didAddress": "F121",
                "responseOnFailedActivation": "NONE",
                "otaActivationTime": 40,
                "programmingMethods": ["ETH_SFTP", "SWDL"],
                "inhaleExhale": "N",
                "swdlReflashTime": 2000,
                "canfdSwdlReflashTime": 2000
            },
        },
        SYNC: {
            CCPU: {
                "artifact_description": "sync4-os-collection",
                BASE_PART_NUMBER: "14G682",
                ARTIFACT: "supplementary_artifacts",
                NEXUS_EXTENSION: ".vbf",
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_FILTER: r"[0-9a-zA-Z]+-14G682-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                FILE_SETTINGS: {
                    "14G682": {
                        "didAddress": "8033",
                        "category": "IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "4500",
                        "canfdSwdlReflashTime": "4500"
                    },
                },
            },
            CCPU_BOOTLOADER: {
                "artifact_description": {
                    "high": "u-boot-40-h", "low": "u-boot-40-l",
                    "prod": "-prod"
                },
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H236",
                ARTIFACT: "ccpu_artifacts",
                FILE_FILTER: r"([0-9a-zA-Z]+-14H236-[0-9a-zA-Z]+[-B0]*[._A-Za-z]*)",
                "file_suffix": {
                    DEVELOPMENT: ".devsecure.vbf",
                    PRODUCTION: ".prodsecure.vbf",
                },
                FILE_SETTINGS: {
                    "14H236": {
                        "didAddress": "8068",
                        "category": "BOOT_IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "200",
                        "canfdSwdlReflashTime": "200"
                    }
                },
            },
            VMCU: {
                "artifact_description": "VMCU", "file_prefix": "swuaFlat_",
                ARTIFACT: "vmcu_artifacts", FILE_FILTER: r"swuaFlat_[0-9a-zA-Z]+-14G676-[0-9a-zA-Z]+",
                LOCATION: {
                    PRODUCTION: ["Appl_ImageFile/Production-Signed", "Appl_ImageFile"],
                    DEVELOPMENT: ["Appl_ImageFile"]
                },
                "file_suffix": '.vbf', BASE_PART_NUMBER: "14G676",
                "vbf_description": "SYNC VMCU load", NEXUS_EXTENSION: ".zip",
                "database": "Appl/Config/Database",
                FILE_SETTINGS: {
                    "14G676": {
                        "didAddress": "F188",
                        "category": "STRATEGY",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "350",
                        "canfdSwdlReflashTime": "350"
                    },
                },
            },
            VMCU_BOOTLOADER: {
                "artifact_description": "VMCU", "file_prefix": 'swuaFlat_',
                ARTIFACT: "vmcu_artifacts", FILE_FILTER: "swuaFlat_[0-9a-zA-Z]+-14H234-[0-9a-zA-Z]+",
                LOCATION: {
                    PRODUCTION: ["Appl_ImageFile/Production-Signed", "Appl_ImageFile"],
                    DEVELOPMENT: ["Appl_ImageFile"]
                },
                "file_suffix": '.vbf', BASE_PART_NUMBER: "14H234",
                "vbf_description": "SYNC4 VMCU Bootloader",
                NEXUS_EXTENSION: ".zip",
                FILE_SETTINGS: {
                    "14H234": {
                        "didAddress": "D027",
                        "category": "BOOT_IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "200",
                        "canfdSwdlReflashTime": "200"
                    },
                },
            },
            CALIBRATION_FILES: {
                "artifact_description": "VMCU", "file_extension": '.vbf',
                ARTIFACT: "vmcu_artifacts", NEXUS_EXTENSION: ".zip",
                LOCATION: {
                    PRODUCTION: ["Appl_ImageFile/Production-Signed", "Appl_ImageFile"],
                    DEVELOPMENT: ["Appl_ImageFile"]
                },
                DESCRIPTION: {
                    "Audio Calibration": {
                        FILE_FILTER: "swuaFlat_[0-9a-zA-Z]+-14G680-[0-9a-zA-Z]+", "file_prefix": 'swuaFlat_'
                    },
                    "Illumination Calibration": {
                        FILE_FILTER: "swuaFlat_[0-9a-zA-Z]+-14J003-[0-9a-zA-Z]+", "file_prefix": 'swuaFlat_'
                    },
                },
                FILE_SETTINGS: {
                    "14G680": {
                        "didAddress": "F10A",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "200",
                        "canfdSwdlReflashTime": "200"
                    },
                    "14J003": {
                        "didAddress": "F16B",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": "200",
                        "canfdSwdlReflashTime": "200"
                    }
                },
            },
            "apps": {
                ARTIFACT: "package_artifacts", "artifact_description": "",
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "didAddress": "8060",
                    "category": "APPLICATION",
                    "responseOnFailedActivation": "NONE",
                    "otaActivationTime": 40,
                    "programmingMethods": ["ETH_SFTP", "SWDL"],
                    "activationMethod": "SINGLE_IGNITION_CYCLE_REQUIRED",
                    "stoppable": "NO",
                    "inhaleExhale": "N",
                    "swdlReflashTime": "7000",
                    "canfdSwdlReflashTime": "7000"
                }
            },
            "maps": {
                ARTIFACT: "package_artifacts", "artifact_description": "",
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "14H008": {
                        "didAddress": "8060",
                        "category": "SYNC_MAP_DATA",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "activationMethod": "INSTANTANEOUS",
                        "stoppable": "YES",
                        "inhaleExhale": "N",
                        "swdlReflashTime": "7000",
                        "canfdSwdlReflashTime": "7000"
                    },
                    "14H009": {
                        "didAddress": "8060",
                        "category": "SYNC_VOICE_DATA",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "activationMethod": "SINGLE_IGNITION_CYCLE_REQUIRED",
                        "stoppable": "NO",
                        "inhaleExhale": "N",
                        "swdlReflashTime": "7000",
                        "canfdSwdlReflashTime": "7000"
                    }
                }
            }
        },
        PHOENIX: {
            CCPU: {
                ARTIFACT: "supplement_VBF_XBF_artifact",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VBF/XBF",
                NEXUS_ARTIFACT_ID: r"[0-9a-zA-Z]+-14H567-[0-9a-zA-Z]+",
                NEXUS_EXTENSION: ".vbf", BASE_PART_NUMBER: "14H567",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H567-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "14H567": {
                        "didAddress": "8033",
                        "category": "IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 60,
                        "programmingMethods": ["ETH_SFTP", "SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 1800,
                        "canfdSwdlReflashTime": None
                    },
                },
            },
            CCPU_BOOTLOADER: {
                ARTIFACT: "supplement_VBF_XBF_artifact",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VBF/XBF",
                NEXUS_ARTIFACT_ID: r"[0-9a-zA-Z]+-14H565-[a-zA-Z]+[0-9]{6}",
                NEXUS_EXTENSION: ".vbf", BASE_PART_NUMBER: "14H565",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H565-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "14H565": {
                        "didAddress": "8068",
                        "category": "BOOT_IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 60,
                        "programmingMethods": ["ETH_SFTP"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": None,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            CCPU_BOOTLOADER_SECURE: {
                ARTIFACT: "supplement_VBF_XBF_artifact",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VBF/XBF",
                NEXUS_ARTIFACT_ID: r"[0-9a-zA-Z]+-14H565-[a-zA-Z]+[0-9]{5}",
                NEXUS_EXTENSION: ".vbf", BASE_PART_NUMBER: "14H565",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H565-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "14H565": {
                        "didAddress": "8068",
                        "category": "BOOT_IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 60,
                        "programmingMethods": ["ETH_SFTP"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 1800,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            # Android Guest
            ANDROID_GUEST: {
                ARTIFACT: "supplement_VBF_XBF_artifact",
                HTML_ARTIFACT: "PHX-AOSP/manifest VBF/XBF",
                NEXUS_ARTIFACT_ID: r"[0-9a-zA-Z]+-14H648-[0-9a-zA-Z]+",
                NEXUS_EXTENSION: ".vbf", BASE_PART_NUMBER: "14H648",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H648-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {PRODUCTION: "", DEVELOPMENT: ""},
                FILE_SETTINGS: {
                    "14H648": {
                        "didAddress": "8073",
                        "category": "BOOT_IMAGE",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": 40,
                        "programmingMethods": ["ETH_SFTP"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": None,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            VIP_SBL: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14J048",
                FILE_FILTER: r"[0-9a-zA-Z]+-14J048-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {DEVELOPMENT: "VIP/image/sbl", PRODUCTION: "VIP/image/sbl"},
                VARIANT: {JSON: "phoenix_hi-belford-user", HTML: "PHOENIX/phx-fsb Artifacts"},
                FILE_SETTINGS: {
                    "14J048": {
                        "didAddress": "",
                        "category": "SECONDARY_BOOTLOADER",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            VIP_APP: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H535",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H535-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {DEVELOPMENT: "VIP/image/sfi", PRODUCTION: "VIP/image/sfi"},
                PART_II_PART_NUMBER: "VIP/artifacts/MDX",
                FILE_SETTINGS: {
                    "14H535": {
                        "didAddress": "F188",
                        "category": "STRATEGY",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            CHIME: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H645",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H645-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {DEVELOPMENT: "VIP/image/calibration/chime", PRODUCTION: "VIP/image/calibration/chime"},
                FILE_SETTINGS: {
                    "14H645": {
                        "didAddress": "F16D",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            DI_GAUGES: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H584",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H584-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {
                    DEVELOPMENT: "VIP/image/calibration/di_gauges", PRODUCTION: "VIP/image/calibration/di_gauges"},
                FILE_SETTINGS: {
                    "14H584": {
                        "didAddress": "F16C",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            FUSA: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H646",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H646-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {
                    DEVELOPMENT: "VIP/image/calibration/fusa", PRODUCTION: "VIP/image/calibration/fusa"},
                FILE_SETTINGS: {
                    "14H646": {
                        "didAddress": "F16E",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            ILLUMINATION: {
                NAME: "VIP_SFI-VIP_SFI",
                HTML_ARTIFACT: "PHOENIX/phx-fsb VIP",
                NEXUS_ARTIFACT_ID: "VIP_SFI",
                NEXUS_EXTENSION: "tar.gz", BASE_PART_NUMBER: "14H583",
                FILE_FILTER: r"[0-9a-zA-Z]+-14H583-[0-9a-zA-Z]+", "file_suffix": '.vbf',
                LOCATION: {
                    DEVELOPMENT: "VIP/image/calibration/illumination",
                    PRODUCTION: "VIP/image/calibration/illumination"
                },
                FILE_SETTINGS: {
                    "14H583": {
                        "didAddress": "F16B",
                        "category": "ECU_CONFIGURATION",
                        "responseOnFailedActivation": "NONE",
                        "otaActivationTime": None,
                        "programmingMethods": ["SWDL"],
                        "inhaleExhale": "N",
                        "swdlReflashTime": 90,
                        "canfdSwdlReflashTime": None
                    }
                }
            },
            NEXUS_URL: {
                JSON: {
                    PHX_NEXUS: {NEXUS_ARTIFACT_ID: "AAA_Readme", VARIANT: ""},
                    AOS_NEXUS: {NEXUS_ARTIFACT_ID: "AAA_Readme", VARIANT: ""}
                },
                HTML: {
                    PHX_NEXUS: {NEXUS_ARTIFACT_ID: "AAA_Readme", VARIANT: "PHOENIX/phx-fsb Metadata"},
                    AOS_NEXUS: {NEXUS_ARTIFACT_ID: "AAA_Readme", VARIANT: "PHX-AOSP/manifest Metadata"}
                }
            },
        }
    }



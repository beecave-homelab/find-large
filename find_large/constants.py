"""Constants used throughout the find-large-files package."""

import os
from typing import Final

# Default search parameters
DEFAULT_DIR: Final[str] = "."
DEFAULT_SIZE_GB: Final[float] = 1
DEFAULT_SIZE_MB: Final[float] = 100

# Size conversion constants
KB_TO_BYTES: Final[int] = 1024
MB_TO_BYTES: Final[int] = KB_TO_BYTES * 1024
GB_TO_BYTES: Final[int] = MB_TO_BYTES * 1024
TB_TO_BYTES: Final[int] = GB_TO_BYTES * 1024

# Hidden folders to include in search
INCLUDE_HIDDEN_FOLDERS: Final[set[str]] = {".git", ".config", ".huggingface", ".local"}

# System folders to exclude from search
EXCLUDE_FOLDERS: Final[list[str]] = [
    # System directories
    "/System",
    "/private",
    "/var/log",
    "/Library/Extensions",
    "/System/Library/PrivateFrameworks",
    "/Library/Kexts/",
    # User Library directories
    os.path.expanduser("~/Library/Mail"),
    os.path.expanduser("~/Library/Messages"),
    os.path.expanduser("~/Library/Safari"),
    os.path.expanduser("~/Library/Calendars"),
    os.path.expanduser("~/Library/Keychains"),
    os.path.expanduser("~/Library/Containers/com.apple.notes"),
    os.path.expanduser("~/Library/Application Support/AddressBook"),
    os.path.expanduser("~/Library/Application Support/MobileSync"),
    os.path.expanduser("~/Library/Application Support/CallHistoryTransactions"),
    os.path.expanduser("~/Library/Application Support/CloudDocs"),
    os.path.expanduser("~/Library/Application Support/com.apple.sharedfilelist"),
    os.path.expanduser("~/Library/Application Support/Knowledge"),
    os.path.expanduser("~/Library/Application Support/com.apple.TCC"),
    os.path.expanduser("~/Library/Application Support/FileProvider"),
    os.path.expanduser("~/Library/Application Support/FaceTime"),
    os.path.expanduser("~/Library/Application Support/com.apple.avfoundation/Frecents"),
    os.path.expanduser("~/Library/Application Support/CallHistoryDB"),
    # Additional Library directories
    os.path.expanduser("~/Library/Assistant/SiriVocabulary"),
    os.path.expanduser("~/Library/Daemon Containers"),
    os.path.expanduser("~/Library/Autosave Information"),
    os.path.expanduser("~/Library/IdentityServices"),
    os.path.expanduser("~/Library/HomeKit"),
    os.path.expanduser("~/Library/Sharing"),
    os.path.expanduser("~/Library/com.apple.aiml.instrumentation"),
    os.path.expanduser("~/Library/Trial"),
    os.path.expanduser("~/Library/AppleMediaServices"),
    os.path.expanduser("~/Library/DuetExpertCenter"),
    os.path.expanduser("~/Library/Accounts"),
    os.path.expanduser("~/Library/Biome"),
    os.path.expanduser("~/Library/IntelligencePlatform"),
    os.path.expanduser("~/Library/Shortcuts"),
    os.path.expanduser("~/Library/Suggestions"),
    os.path.expanduser("~/Library/Weather"),
    # Group Containers
    os.path.expanduser("~/Library/Group Containers/group.com.apple.stocks-news"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.photolibraryd.private"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.accessibility.voicebanking"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.stocks"),
    os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.secure-control-center-preferences"
    ),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.chronod"),
    os.path.expanduser("~/Library/Group Containers/com.apple.MailPersonaStorage"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.private.translation"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.calendar"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.newsd"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.ip.redirects"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.siri.userfeedbacklearning"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.gamecenter"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.tips"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.tv.sharedcontainer"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.ManagedSettings"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.sharingd"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.weather"),
    os.path.expanduser("~/Library/Group Containers/com.apple.systempreferences.cache"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.feedbacklogger"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.notes"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.tipsnext"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.Safari.SandboxBroker"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.transparency"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.reminders"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.mail"),
    os.path.expanduser("~/Library/Group Containers/com.apple.bird"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.DeviceActivity"),
    os.path.expanduser("~/Library/Group Containers/com.apple.Home.group"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.iCloudDrive"),
    os.path.expanduser("~/Library/Group Containers/com.apple.PreviewLegacySignaturesConversion"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.AppleSpell"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.mlhost"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.PegasusConfiguration"),
    os.path.expanduser("~/Library/Group Containers/group.com.apple.shortcuts"),
    os.path.expanduser("~/Library/Group Containers/com.apple.MessagesLegacyTransferArchive"),
    # Containers
    os.path.expanduser("~/Library/Containers/com.apple.VoiceMemos"),
    os.path.expanduser("~/Library/Containers/com.apple.archiveutility"),
    os.path.expanduser("~/Library/Containers/com.apple.Maps/Data/Maps"),
    os.path.expanduser("~/Library/Containers/com.apple.Home"),
    os.path.expanduser("~/Library/Containers/com.apple.Safari"),
    os.path.expanduser("~/Library/Containers/com.apple.CloudDocs.MobileDocumentsFileProvider"),
    os.path.expanduser("~/Library/Containers/com.apple.mail"),
    os.path.expanduser("~/Library/Containers/com.apple.MobileSMS"),
    os.path.expanduser("~/Library/Containers/com.apple.Notes"),
    os.path.expanduser("~/Library/Containers/com.apple.news"),
    os.path.expanduser("~/Library/Containers/com.apple.corerecents.recentsd/Data/Library/Recents"),
    os.path.expanduser("~/Library/Containers/com.apple.stocks"),
    os.path.expanduser("~/Library/Containers/com.apple.Safari.WebApp"),
    # Additional system directories
    os.path.expanduser("~/Library/ContainerManager"),
    os.path.expanduser("~/Library/PersonalizationPortrait"),
    os.path.expanduser("~/Library/Photos/Libraries/Syndication.photoslibrary"),
    os.path.expanduser("~/Library/Metadata/CoreSpotlight"),
    os.path.expanduser("~/Library/Metadata/com.apple.IntelligentSuggestions"),
    os.path.expanduser("~/Library/Cookies"),
    os.path.expanduser("~/Library/CoreFollowUp"),
    os.path.expanduser("~/Library/StatusKit"),
    os.path.expanduser("~/Library/DoNotDisturb"),
    # Cache directories
    os.path.expanduser("~/Library/Caches/com.apple.HomeKit"),
    os.path.expanduser("~/Library/Caches/CloudKit"),
    os.path.expanduser("~/Library/Caches/com.apple.Safari"),
    os.path.expanduser("~/Library/Caches/com.apple.findmy.imagecache"),
    os.path.expanduser("~/Library/Caches/com.apple.findmy.fmfcore"),
    os.path.expanduser("~/Library/Caches/com.apple.containermanagerd"),
    os.path.expanduser("~/Library/Caches/FamilyCircle"),
    os.path.expanduser("~/Library/Caches/com.apple.homed"),
    os.path.expanduser("~/Library/Caches/com.apple.findmy.fmipcore"),
    os.path.expanduser("~/Library/Caches/com.apple.ap.adprivacyd"),
    # Other
    os.path.expanduser("~/.Trash"),
    os.path.expanduser("~/Pictures/Photos Library.photoslibrary"),
    os.path.expanduser("~/Dropbox"),
    os.path.expanduser("~/Library/CloudStorage/Dropbox"),
    os.path.expanduser("~/Library/Containers/com.apple.CloudPhotosConfiguration"),
    os.path.expanduser(
        "~/Library/Containers/com.apple.dp.PrivateFederatedLearning.DPMLRuntimePluginClassB/"
    ),
]

# Size units for display
SIZE_UNIT_GB: Final[str] = "GB"
SIZE_UNIT_MB: Final[str] = "MB"
SIZE_UNIT_TB: Final[str] = "TB"

[app]
title = Teams Filter
package.name = teamsfilter
package.domain = org.nick403
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
android.api = 34
android.ndk = 25b
android.build_tools_version = 34.0.0

# Permissions
android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE,MODIFY_AUDIO_SETTINGS,FOREGROUND_SERVICE,INTERNET

# Add extra manifest chunk for the notification listener service
android.add_manifest_xml = ./android_manifest_snippets.xml

# Use service python file for background listener
android.services = filter_service:TeamsFilterService

[buildozer]
log_level = 2
warn_on_root = 1

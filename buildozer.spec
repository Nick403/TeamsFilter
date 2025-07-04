[app]
title = Teams Filter
version=1.0
package.name = teamsfilter
package.domain = org.example
source.dir = .
source.include_exts = py,json,xml,kv,md
requirements = kivy,pyjnius
orientation = portrait

# Permissions
android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE,MODIFY_AUDIO_SETTINGS,FOREGROUND_SERVICE

# Add extra manifest chunk for the notification listener service
android.add_manifest_xml = ./android_manifest_snippets.xml

# Use service python file for background listener
android.services = filter_service:TeamsFilterService

[buildozer]
log_level = 2
warn_on_root = 1

[app]
# (str) Title of your application
title = HenrySmith Autos Ltd

# (str) Package name
package.name = henrysmithautos

# (str) Package domain (reverse DNS)
package.domain = org.henrysmith

# (str) Source code where the main.py is located (relative to this file)
source.dir = src

# (str) List of file extensions to include in the package
source.include_exts = py,kv,png,jpg,jpeg,svg,html,css,js

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements, comma separated
# Adjust these to match your app's Python dependencies. Keep kivy in the list.
requirements = python3,kivy==2.1.0,requests,pillow

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (int) Fullscreen (1) or not (0)
fullscreen = 0

# (str) Presplash image. Uncomment and set if you have one.
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon file
# icon.filename = %(source.dir)s/assets/icon.png

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) Android API to target
android.api = 31
android.minapi = 21
# (str) Pin NDK if necessary. Leave commented to let buildozer manage it.
# android.ndk = 23b

# (int) Target SDK version (optional)
# android.target = 31

# (str) Supported orientations for Android
# android.orientation = portrait


[buildozer]
# (int) Log level (0 = error, 1 = warning, 2 = info, 3 = debug)
log_level = 2

# (int) Warn if running as root (1 = warn)
warn_on_root = 1


[app:android]
# Additional Android packaging options
# (list) Add any Java .jar files to the libs/ directory
# android.add_jars = libs/some-lib.jar

# (str) Android entrypoint, usually set automatically to org.kivy.android.PythonActivity
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Additional source directories to include
# android.add_src = src/android

# (str) Gradle dependencies
# android.gradle_dependencies = com.google.android.gms:play-services-auth:19.0.0

# (bool) Use the new Android toolchain (recommended)
# android.new_toolchain = True

[app]
title = Auto Expense Tracker
package.name = expensetracker
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Pinned to Python 3.11.9 and stable Kivy/Pyjnius so C-compilation succeeds
requirements = python3==3.11.9,kivy==2.3.1,pyjnius==1.6.1,requests,urllib3,chardet,idna,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_SMS,RECEIVE_SMS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Build for modern 64-bit Android phones (2x faster & prevents log truncation)
android.archs = arm64-v8a

# Use stable python-for-android release
p4a.branch = release-2024.01.21

[buildozer]
# Set log_level to 1 so GitHub logs never truncate
log_level = 1
warn_on_root = 0

[app]
title = Auto Expense Tracker
package.name = expensetracker
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_SMS,RECEIVE_SMS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0

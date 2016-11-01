from addict import Dict


cordova_tag = '<script type="text/javascript" src="cordova.js"></script>'
cordova_re = r'^<script.*(src=("|\')cordova\.js("|\')).*>'

build_tool_version = '23.0.3'
gradle_plugin = 'apply plugin: \'com.android.application\''
sdk_version = '23'

keystore = Dict()
keystore.path = '/etc/digger/debug.keystore'
keystore.storepass = 'android'
keystore.keypass = 'android'
keystore.alias = 'androiddebug'

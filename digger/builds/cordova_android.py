import os

from digger import config
from digger.base.build import BaseBuild
from digger.helpers import android as android_helper


class CordovaBuildAndroid(BaseBuild):
  def __init__(self, **kwargs):
    super(CordovaBuildAndroid, self).__init__(**kwargs)

  def sign(self, storepass=None, keypass=None, keystore=None, apk=None, alias=None, name='app'):
    if keystore is None:
      (keystore, storepass, keypass, alias) = android_helper.get_default_keystore()
    dist = '%s/%s.apk' % ('/'.join(apk.split('/')[:-1]), name)

    android_helper.jarsign(storepass, keypass, keystore, apk, alias, path=self.path)
    android_helper.zipalign(apk, dist, build_tool=config.build_tool_version, path=self.path)

  def prepare(self):
    # add android platform as we don't want the build to fail because of missing
    # android platform in the config.xml file.
    self.run_cmd(['cordova', 'platform', 'add', 'android'], 'prepare')

    # clean stuff first
    # then prepare
    self.run_cmd(['cordova', 'clean'], 'prepare')
    self.run_cmd(['cordova', 'prepare'], 'prepare')

  def validate(self):
    # nothing to validate here.
    # just create the validate.log file.
    with open('%s/validate.log' % self.path, 'a'):
      os.utime('%s/validate.log' % self.path, None)

  def build(self, mode='debug'):
    # run something like
    # cordova build android --debug
    # OR
    # cordova build android --release
    self.run_cmd(['cordova', 'build', "android", "--" + mode], 'build')


  def test(self):
    # nothing to test here.
    # just create the test.log file.
    with open('%s/test.log' % self.path, 'a'):
      os.utime('%s/test.log' % self.path, None)

  def get_export_path(self):
    """
    Gets the apk(s) path that can be exported outside of the container.
    """
    return ','.join(android_helper.find_apks(self.path))

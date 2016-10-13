import os
import shutil

from digger import config
from digger.base.build import BaseBuild
from digger.helpers import android as android_helper


class CordovaAndroidBuild(BaseBuild):
  def __init__(self, **kwargs):
    super(CordovaAndroidBuild, self).__init__(**kwargs)

  def sign(self, storepass=None, keypass=None, keystore=None, apk=None, alias=None, name='app'):
    if keystore is None:
      (keystore, storepass, keypass, alias) = android_helper.get_default_keystore()
    dist = '%s/%s.apk' % ('/'.join(apk.split('/')[:-1]), name)

    android_helper.jarsign(storepass, keypass, keystore, apk, alias, path=self.path)
    android_helper.zipalign(apk, dist, build_tool=config.build_tool_version, path=self.path)

  def prepare(self):
    # no need to create a Cordova project.
    # skipping `cordova create` call.

    # if Android platform is not there, add it.
    if os.path.exists('%s/platforms/android' % self.path) is False:
      self.run_cmd(['cordova', 'platform', 'add', 'android'], 'prepare')

    # if we have a package.json file, do npm run.
    # however, since things in node_modules are platform dependent,
    # remove the things in node_modules first.
    if os.path.exists('%s/package.json' % self.path):
      if os.path.exists('%s/node_modules' % self.path):
        shutil.rmtree('%s/node_modules' % self.path)
      self.run_cmd(['npm', 'install'], 'prepare')

  def validate(self):
    # nothing to validate here.
    # just touch the log file
    self.touch_log('validate')

  def build(self, mode='debug'):
    # run something like
    # cordova build android --debug
    # OR
    # cordova build android --release
    self.run_cmd(['cordova', 'build', "android", "--%s" % mode], 'build')

  def test(self):
    # nothing to test here.
    # just touch the log file
    self.touch_log('test')

  def get_export_path(self):
    """
    Gets the apk(s) path that can be exported outside of the container.
    """
    return ','.join(android_helper.find_apks(self.path))

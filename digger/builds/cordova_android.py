import os
import shutil
import json
import re

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


class CordovaLightAndroidBuild(CordovaAndroidBuild):
  def __init__(self, tmp_folder=None, *args, **kwargs):
    super(CordovaLightAndroidBuild, self).__init__(*args, **kwargs)
    self.tmp_folder = tmp_folder
    if self.tmp_folder is None:
      self.tmp_folder = '%s_tmp' % self.path.split('/')[-1:][0]
    self.tmp_path = '%s/%s' % (os.path.dirname(self.path), self.tmp_folder)

  def is_cordova_light(self):
    if os.path.exists('%s/config.xml' % self.path) is True or os.path.exists('%s/www/config.xml' % self.tmp_path) is True:
      return False
    return True

  def create_cordova_app(self):
    self.run_cmd(['cordova', 'create', '--copy-from', '%s/www' % self.path, self.tmp_path], 'tmp')

  def add_plugins(self):
    with open('%s/www/config.json' % self.tmp_path) as f:
      config = json.load(f)
      plugins = config.get('plugins', [])
      cmd = ['cordova', 'plugin', 'add']
      [cmd.append(item['url']) for item in plugins]
      self.run_cmd(cmd, 'tmp', cwd=self.tmp_path)

  def prepare_index_file(self):
    with open('%s/www/index.html' % self.tmp_path, 'r+') as f:
      index_file = f.read()
      f.seek(0)
      if re.match(config.cordova_re, index_file) is None:
        f.write(index_file.replace('</body>', '\t%s\n\t</body>' % config.cordova_tag))
      else:
        f.write(index_file)
      f.truncate()

  def cleanup(self):
    shutil.rmtree(self.path)
    os.rename(self.tmp_path, self.path)

  def prepare(self, *args, **kwargs):
    if self.is_cordova_light() is False:
      return super(CordovaLightAndroidBuild, self).prepare(*args, **kwargs)
    self.create_cordova_app()
    self.add_plugins()
    self.prepare_index_file()
    self.cleanup()
    return super(CordovaLightAndroidBuild, self).prepare(*args, **kwargs)

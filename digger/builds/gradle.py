import os
import re
import stat

from digger import config
from digger import errors
from digger.base.build import BaseBuild
from digger.helpers import android as android_helper


class GradleBuild(BaseBuild):
  def __init__(self, cache_folder='/gradle-cache', **kwargs):
    super(GradleBuild, self).__init__(**kwargs)
    self.cache_folder = cache_folder
    self.src_folder = None

  def ensure_cache_folder(self):
    """
    Creates a gradle cache folder if it does not exist.
    """
    if os.path.exists(self.cache_folder) is False:
      os.makedirs(self.cache_folder)

  def is_app_folder(self, folder):
    """
    checks if a folder 
    """
    with open('%s/%s/build.gradle' % (self.path, folder)) as f:
      for line in f.readlines():
        if config.gradle_plugin in line:
          return True
    return False

  def get_src_folder(self):
    """
    Gets the app source folder from settings.gradle file.

    Returns:
      A string containing the project source folder name (default is "app")
    """
    with open('%s/settings.gradle' % self.path) as f:
      for line in f.readlines():
        if line.startswith('include'):
          matches = re.findall(r'\'\:?(.+?)\'', line)
        if len(matches) == 0:
          continue
        for folder in matches:
          if self.is_app_folder(folder):
            return folder
    return 'app'

  def get_build_tool_version(self):
    """
    Gets the build tool version to be used by zipalign from build.gradle file.

    Returns:
      A string containing the build tool version, default is 23.0.2.
    """
    with open('%s/%s/build.gradle' % (self.path, self.src_folder)) as f:
      for line in f.readlines():
        if 'buildToolsVersion' in line:
          matches = re.findall(r'buildToolsVersion \"(.+?)\"', line)
          if len(matches) == 1:
            return matches[0]
    return config.build_tool_version

  def sign(self, storepass=None, keypass=None, keystore=None, apk=None, alias=None, name='app'):
    """
    Signs (jarsign and zipalign) a target apk file based on keystore information, uses default debug keystore file by default.

    :param storepass(str): keystore file storepass
    :param keypass(str): keystore file keypass
    :param keystore(str): keystore file path
    :param apk(str): apk file path to be signed
    :param alias(str): keystore file alias
    :param name(str): signed apk name to be used by zipalign
    """
    self.src_folder = self.get_src_folder()
    if keystore is None:
      (keystore, storepass, keypass, alias) = android_helper.get_default_keystore()
    dist = '%s/%s.apk' % ('/'.join(apk.split('/')[:-1]), name)
    android_helper.jarsign(storepass, keypass, keystore, apk, alias, path=self.path)
    android_helper.zipalign(apk, dist, build_tool=self.get_build_tool_version(), path=self.path)

  def validate(self):
    """
    Validates the app project before the build.

    This is the first step in the build process.

    Needs to be implemented by the subclass.
    """
    if os.path.exists('%s/gradlew' % self.path) is False:
      raise errors.InvalidProjectStructure(message='Missing gradlew project root folder')

    self.touch_log('validate')

  def prepare(self):
    """
    Prepares the android project to the build process.

    Checks if the project uses either gradle or ant and executes the necessary steps.
    """
    self.src_folder = self.get_src_folder()
    st = os.stat('%s/gradlew' % self.path)
    os.chmod('%s/gradlew' % self.path, st.st_mode | stat.S_IEXEC)

  def build(self, mode='debug'):
    """
    Builds the app project after the execution of validate and prepare.

    This is the third and last step in the build process.

    Needs to be implemented by the subclass.
    """
    self.ensure_cache_folder()
    ref = {
      'debug': 'assembleDebug',
      'release': 'assembleRelease'
    }
    cmd = [
      './gradlew',
      ref.get(mode, mode),
      '--gradle-user-home',
      self.cache_folder 
    ]
    self.run_cmd(cmd, 'build')

  def test(self):
    """
    Runs the app unit tests.

    Needs to be implemented by the subclass.
    """
    self.run_cmd(['./gradlew', 'test'], 'test')

  def get_export_path(self):
    """
    Gets the apk(s) path that can be exported outside of the container.
    """
    return ','.join(android_helper.find_apks(self.path))

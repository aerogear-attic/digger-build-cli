import re

from digger import config
from digger.base.build import BaseBuild
from digger.helpers import android as android_helper


class AntBuild(BaseBuild):
  def __init__(self, **kwargs):
    super(AntBuild, self).__init__(**kwargs)

  def get_target(self):
    """
    Reads the android target based on project.properties file.

    Returns
      A string containing the project target (android-23 being the default if none is found)
    """
    with open('%s/project.properties' % self.path) as f:
      for line in f.readlines():
        matches = re.findall(r'^target=(.*)', line)
        if len(matches) == 0:
          continue
        return matches[0].replace('\n', '')
    return 'android-%s' % (config.sdk_version)

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
    target = self.get_target()
    build_tool = android_helper.get_highest_build_tool(target.split('-')[1])
    if keystore is None:
      (keystore, storepass, keypass, alias) = android_helper.get_default_keystore()
    dist = '%s/%s.apk' % ('/'.join(apk.split('/')[:-1]), name)
    android_helper.jarsign(storepass, keypass, keystore, apk, alias, path=self.path)
    android_helper.zipalign(apk, dist, build_tool=build_tool, path=self.path)

  def prepare(self):
    """
    Prepares the android project to the build process.

    Prepare the ant project to be built
    """
    cmd = [
      'android', 'update', 'project',
      '-p', self.path,
      '-t', self.get_target()
    ]
    self.run_cmd(cmd, 'prepare')

  def validate(self):
    """
    Validates the app project before the build.

    This is the first step in the build process.

    Needs to be implemented by the subclass.
    """
    self.run_cmd(['ant'], 'validate')

  def build(self, mode='debug'):
    """
    Builds the app project after the execution of validate and prepare.

    This is the third and last step in the build process.

    Needs to be implemented by the subclass.
    """
    self.run_cmd(['ant', mode], 'build')

  def test(self):
    """
    Runs the app unit tests.

    Needs to be implemented by the subclass.
    """
    self.run_cmd(['ant', 'test'], 'test')

  def get_export_path(self):
    """
    Gets the apk(s) path that can be exported outside of the container.
    """
    return ','.join(android_helper.find_apks(self.path))

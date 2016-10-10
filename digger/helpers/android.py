import functools
import os

from digger import config
from digger.helpers import common


def jarsign(storepass, keypass, keystore, source, alias, path=None):
  """
  Uses Jarsign to sign an apk target file using the provided keystore information.

  :param storepass(str) - keystore storepass
  :param keypass(str) - keystore keypass
  :param keystore(str) - keystore file path
  :param source(str) - apk path
  :param alias(str) - keystore alias
  :param path(str) - basedir to run the command
  """
  cmd = [
    'jarsigner',
    '-verbose',
    '-storepass',
    storepass,
    '-keypass',
    keypass,
    '-keystore',
    keystore,
    source,
    alias
  ]
  common.run_cmd(cmd, log='jarsign.log', cwd=path)


def zipalign(source, dist, build_tool=None, version='4', path=None):
  """
  Uses zipalign based on a provided build tool version (defaulit is 23.0.2).

  :param source(str) - source apk file to be zipaligned
  :param dist(str) - zipaligned apk file path to be created
  :param build_tool(str) - build tool version to be used by zipalign (default is 23.0.2)
  :param version(str) - zipalign version, default is 4
  :param path(str) - basedir to run the command
  """
  if build_tool is None:
    build_tool = config.build_tool_version
  android_home = os.environ.get('AG_MOBILE_SDK', os.environ.get('ANDROID_HOME'))
  cmd_path = [
    android_home,
    '/build-tools',
    '/%s' % build_tool,
    '/zipalign'
  ]
  cmd = [
    ''.join(cmd_path),
    '-v',
    version,
    source,
    dist,
  ]
  common.run_cmd(cmd, log='zipalign.log', cwd=path)


def get_default_keystore(prefix='AG_'):
  """
  Gets the default keystore information based on environment variables and a prefix.

  $PREFIX_KEYSTORE_PATH - keystore file path, default is opt/digger/debug.keystore
  $PREFIX_KEYSTORE_STOREPASS - keystore storepass, default is android
  $PREFIX_KEYSTORE_KEYPASS - keystore keypass, default is android
  $PREFIX_KEYSTORE_ALIAS - keystore alias, default is androiddebug
  
  :param prefix(str) - A prefix to be used for environment variables, default is AG_.

  Returns:
    A tuple containing the keystore information: (path, storepass, keypass, alias)
  """
  path = os.environ.get('%s_KEYSTORE_PATH' % prefix, config.keystore.path)
  storepass = os.environ.get('%s_KEYSTORE_STOREPASS' % prefix, config.keystore.storepass)
  keypass = os.environ.get('%s_KEYSTORE_KEYPASS' % prefix, config.keystore.keypass)
  alias = os.environ.get('%s_KEYSTORE_ALIAS' % prefix, config.keystore.alias)
  return (path, storepass, keypass, alias)


def get_highest_build_tool(sdk_version=None):
  """
  Gets the highest build tool version based on major version sdk version.

  :param sdk_version(int) - sdk version to be used as the marjor build tool version context.

  Returns:
    A string containg the build tool version (default is 23.0.2 if none is found)
  """
  if sdk_version is None:
    sdk_version = config.sdk_version
  android_home = os.environ.get('AG_MOBILE_SDK', os.environ.get('ANDROID_HOME'))
  build_tool_folder = '%s/build-tools' % android_home
  folder_list = os.listdir(build_tool_folder)
  versions = [folder for folder in folder_list if folder.startswith('%s.' % sdk_version)]
  if len(versions) == 0:
    return config.build_tool_version
  return versions[::-1][0]


find_apks = functools.partial(common.find, pattern='*.apk')

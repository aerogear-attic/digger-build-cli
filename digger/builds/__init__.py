import os

from digger import errors

from .ant import AntBuild
from .cordova_android import CordovaAndroidBuild
from .gradle import GradleBuild

ref = {
  'gradle': {
    'is_valid': lambda path: os.path.exists('%s/build.gradle' % path),
    'builder': lambda path: GradleBuild.from_path(path)
  },
  'ant': {
    'is_valid': lambda path: os.path.exists('%s/build.xml' % path),
    'builder': lambda path: AntBuild.from_path(path)
  },
  'cordova_android': {
    # one big improvement would be:
    # * parse config.xml file
    # * check if the root element is "widget" from namespace "http://www.w3.org/ns/widgets"
    # then we can be sure that it is a Cordova project.
    # we also need to check if we want to build an IOS app or Android app for the Cordova.
    # for now, we don't do that and support Android only.
    'is_valid': lambda path: os.path.exists('%s/config.xml' % path),
    'builder': lambda path: CordovaAndroidBuild.from_path(path)
  }
}

def from_path(path):
  """
  Selects and returns a build class based on project structure/config from a given path.

  :param path(str): required path argument to be used
  """
  for item in ref:
    build = ref[item]
    valid_ = build['is_valid']
    if valid_(path) is True:
      return build['builder'](path)
  raise errors.InvalidProjectStructure()
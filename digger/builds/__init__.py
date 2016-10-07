import os

from .ant import AntBuild
from .cordova_android import CordovaBuildAndroid
from .gradle import GradleBuild


def from_path(path):
  """
  Selects and returns a build class based on project structure/config from a given path.

  :param path(str): required path argument to be used
  """
  if os.path.exists('%s/build.gradle' % path):
    return GradleBuild.from_path(path)

  elif os.path.exists('%s/config.xml' % path):
    # one big improvement would be:
    # * parse config.xml file
    # * check if the root element is "widget" from namespace "http://www.w3.org/ns/widgets"
    # then we can be sure that it is a Cordova project.
    # we also need to check if we want to build an IOS app or Android app for the Cordova.
    # for now, we don't do that and support Android only.
    return CordovaBuildAndroid.from_path(path)

  else:
    return AntBuild.from_path(path)

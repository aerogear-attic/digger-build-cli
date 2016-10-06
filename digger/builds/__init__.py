import os

from .ant import AntBuild
from .gradle import GradleBuild


def from_path(path):
  """
  Selects and returns a build class based on project structure/config from a given path. 

  :param path(str): required path argument to be used
  """
  if os.path.exists('%s/build.gradle' % path):
    return GradleBuild.from_path(path)
  return AntBuild.from_path(path)

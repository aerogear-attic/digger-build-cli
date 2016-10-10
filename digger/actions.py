from digger import builds
from .base.action import BaseAction, Argument

__ALL__ = ['BuildAction', 'ExportAction', 'InspectAction', 'LogAction']


class BuildAction(BaseAction):
  """
  Build action that inherits from BaseAction to trigger application builds based on an 
  app source code folder path.
  """
  _cmd_ = 'build'
  _help_ = 'build your android app'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')
  mode = Argument('--mode', '-m', default='debug', action='store', help='build mode: debug(default) or release')

  def handler(self, path='/app', mode='debug'):
    """
    Handler that executes the application build based on its platform (using the ``project`` package).

    param: path(str): the project source code path, default is '/app'.
    param: target(str): the platform target, android-23 is the default for android platform if no value is provided.

    Returns:
      Doesn't return a value but prints the output in the STDOUT/STDERR.
    """
    options = {
      'path': path
    }
    project = builds.from_path(path)
    project.prepare()
    project.validate()
    project.build(mode=mode)


class ExportAction(BaseAction):
  """
  Export action that inherits from BaseAction to show the apk(s) path to be exported from the container.
  """
  _cmd_ = 'export'
  _help_ = 'export apk file(s)'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')

  def handler(self, path='/app'):
    """
    Handler that prints the apk file(s) path that can be exported from the container (using the ``project`` package).

    :param path(str): the project source code path, default is '/app'.

    Returns:
      Doesn't return a value but prints the output in the STDOUT/STDERR (separated by a comma).
    """
    options = {
      'path': path
    }
    project = builds.from_path(path)
    print(project.get_export_path())


class InspectAction(BaseAction):
  """
  Inspect action that inherits from BaseAction to show the app project structure in the STDOUT.
  """
  _cmd_ = 'inspect'
  _help_ = 'inspect your app files'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')

  def handler(self, path='/app'):
    """
    Handler that prints the project file structure in the STDOUT (using the ``project`` package).

    :param path(str): the project source code path, default is '/app'.

    Returns:
      Doesn't return a value but prints the output in the STDOUT/STDERR (separated by a comma).
    """
    options = {
      'path': path
    }
    project = builds.from_path(path)
    print(project.inspect())


class LogAction(BaseAction):
  """
  Log action that inherits from BaseAction to retrieve the build logs in the STDOUT.
  """
  _cmd_ = 'log'
  _help_ = 'read build log'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')
  ctx = Argument('--ctx', '-c', default='all', action='store', help='log context')

  def handler(self, path='/app', ctx='all'):
    """
    Handler that prints the project build log into the STDOUT (using the ``project`` package).

    :param path(str): the project source code path, default is '/app'.
    :param ctx(str): build log context file to be used, available options: validate, prepare, build or all.

    Returns:
      Doesn't return a value but prints the output in the STDOUT/STDERR (separated by a comma).
    """
    options = {
      'path': path
    }
    project = builds.from_path(path)
    project.log(ctx=ctx)


class TestAction(BaseAction):
  """
  Inspect action that inherits from BaseAction to show the app project structure in the STDOUT.
  """
  _cmd_ = 'test'
  _help_ = 'run the test task'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')

  def handler(self, path='/app'):
    """
    Handler that prints the project file structure in the STDOUT (using the ``project`` package).

    :param path(str): the project source code path, default is '/app'.

    Returns:
      Doesn't return a value but prints the output in the STDOUT/STDERR (separated by a comma).
    """
    options = {
      'path': path
    }
    project = builds.from_path(path)
    project.test()


class SignAction(BaseAction):
  _cmd_ = 'sign'
  _help_ = 'sign app binary'

  path = Argument('--path', '-p', default='/app', action='store', help='app source path')
  storepass = Argument('--storepass', '-sp', default='android', action='store', help='android storepass')
  keypass = Argument('--keypass', '-kp', default='android', action='store', help='android keypass')
  keystore = Argument('--keystore', '-ls', default=None, action='store', help='android keystore filename')
  alias = Argument('--alias', '-a', default='debug', action='store', help='android keystore alias')
  binary = Argument('--binary', '-b', default=None, action='store', help='binary path to sign')
  name = Argument('--name', '-n', default='app', action='store', help='output filename')

  def handler(self, path='/app', storepass='android', keypass='android', keystore='android', alias='debug', binary=None, name='app'):
    options = {
      'storepass': storepass,
      'keypass': keypass,
      'keystore': keystore,
      'alias': alias,
      'apk': binary,
      'name': name
    }
    project = builds.from_path(path)
    project.sign(**options)

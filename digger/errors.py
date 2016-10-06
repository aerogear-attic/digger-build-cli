class BaseError(Exception):
  """
  Base exception class to be used whitin the module.

  Every subclass error class should define an instance message property. 
  """
  def __init__(self, message=None):
    """
    Constructor that takes an optional message parameter to be displayed.

    :param message(str): error message to be shown.
    """
    self.message = message

  def print_error(self):
    """Prints the error into teh STDOUT"""
    print('Error: %s' % self.message)


class InvalidPathError(BaseError):
  """Raised when an app folder path cannot be found."""
  def __init__(self, path, **kwargs):
    """
    Error class constructor to be used
    
    :param path(str): path to be shown and invalid in the error log.
    """
    BaseError.__init__(self, **kwargs)
    self.path = path
    self.message = 'Invalid path: %s' % self.path


class InvalidZipFileError(BaseError):
  """Raised when the module can't unzip the app file (usually when the zipfile is corrupted)."""
  def __init__(self, path, **kwargs):
    """
    Error class constructor to be used
    :param path(str): zipfile path.
    """
    BaseError.__init__(self, **kwargs)
    self.path = path
    self.message = 'Invalid zipfile in path: %s' % self.path


class InvalidCMDError(BaseError):
  """Raised when and invalid command is used in the CLI."""
  def __init__(self, cmd, **kwargs):
    """
    Error class constructor to be used
    :param cmd(str): invalid cmd name used by the user.
    """
    BaseError.__init__(self, **kwargs)
    self.cmd = cmd
    self.message = 'Invalid cmd: %s' % self.cmd


class MethodNotImplementedError(BaseError):
  """Raised when a handler from a BaseAction subclass was not implemented."""
  def __init__(self, **kwargs):
    """
    Error class constructor to be used
    """
    BaseError.__init__(self, **kwargs)


class DownloadError(BaseError):
  """Raised when the module can't download the app source code from a given url."""
  def __init__(self, **kwargs):
    """
    Error class constructor to be used
    :param cmd(str): invalid cmd name used by the user.
    """
    BaseError.__init__(self, **kwargs)


class InvalidProjectStructure(BaseError):
  """
  Raised when the module can't build the app due to an invalid project structure.
  Example: gradlew file is missing from the gradle project.
  """
  def __init__(self, **kwargs):
    """
    Error class constructor to be used
    :param cmd(str): invalid cmd name used by the user.
    """
    BaseError.__init__(self, **kwargs)

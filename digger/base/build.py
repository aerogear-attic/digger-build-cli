from __future__ import print_function

import os
import zipfile
import base64
import abc
from six import with_metaclass

from digger import errors
from digger.helpers import common


class BaseBuild(with_metaclass(abc.ABCMeta, object)):
  """
  Base project to be used as base class (subclassing) for specific platform projects (android, ios, etc).
  """

  @classmethod
  def from_url(cls, url, **kwargs):
    """
    Downloads a zipped app source code from an url.

    :param url: url to download the app source from

    Returns
      A project instance.
    """
    username = kwargs.get('username')
    password = kwargs.get('password')
    headers = kwargs.get('headers', {})
    auth = None
    path = kwargs.get('path', '/tmp/app.zip')
    dest = kwargs.get('dest', '/app')
    if username and password:
      auth = base64.b64encode(b'%s:%s' % (username, password))
    if auth:
      headers['Authorization'] = 'Basic %s' % auth.decode('utf8')
    r = request.get(url, headers=headers, stream=True)
    if r.status_code != 200:
      err_msg = 'Could not download resource from url (%s): %s'
      err_args = (r.status_code, url)
      raise errors.DownloadError(err_msg % err_args)
    with open('/tmp/app.zip', 'wb+') as f:
      chunks = r.iter_content(chunk_size=1024)
      [f.write(chunk) for chunk in chunks if chunk]
    return cls.from_zip(path, dest)

  @classmethod
  def from_path(cls, path):
    """
    Instantiates a project class from a given path.

    :param path: app folder path source code

    Returns
      A project instance.
    """
    if os.path.exists(path) is False:
      raise errors.InvalidPathError(path)
    return cls(path=path)

  @classmethod
  def from_zip(cls, src='/tmp/app.zip', dest='/app'):
    """
    Unzips a zipped app project file and instantiates it.

    :param src: zipfile path
    :param dest: destination folder to extract the zipfile content

    Returns
      A project instance.
    """
    try:
      zf = zipfile.ZipFile(src, 'r')
    except FileNotFoundError:
      raise errors.InvalidPathError(src)
    except zipfile.BadZipFile:
      raise errors.InvalidZipFileError(src)
    [zf.extract(file, dest) for file in zf.namelist()]
    zf.close()
    return cls.from_path(dest)

  def __init__(self, path=None):
    """
    Creates a new project instance with an optional path if provided.

    :param path(optional): project folder source code

    Returns
      A project instance.
    """
    self.path = path
  
  def inspect(self, tab_width=2, ident_char='-'):
    """
    Inspects a project file structure based based on the instance folder property.

    :param tab_width: width size for subfolders and files.
    :param ident_char: char to be used to show identation level

    Returns
      A string containing the project structure.
    """
    startpath = self.path
    output = []
    for (root, dirs, files) in os.walk(startpath):
      level = root.replace(startpath, '').count(os.sep)
      indent = ident_char * tab_width * (level)
      if level == 0:
        output.append('{}{}/'.format(indent, os.path.basename(root)))
      else:
        output.append('|{}{}/'.format(indent, os.path.basename(root)))
      subindent = ident_char * tab_width * (level + 1)
      [output.append('|{}{}'.format(subindent, f)) for f in files]
    return '\n'.join(output)

  def log(self, ctx='all'):
    """
    Gets the build log output.

    :param ctx: specifies which log message to show, it can be 'validate', 'build' or 'all'.
    """
    path = '%s/%s.log' % (self.path, ctx)
    if os.path.exists(path) is True:
      with open(path, 'r') as f:
        print(f.read())
      return
    validate_path = '%s/validate.log' % self.path
    build_path = '%s/build.log' % self.path
    out = []
    with open(validate_path) as validate_log, open(build_path) as build_log:
      for line in validate_log.readlines():
        out.append(line)
      for line in build_log.readlines():
        out.append(line)
    print(''.join(out))

  def run_cmd(self, cmd, ctx='log'):
    common.run_cmd(cmd, log='%s.log' % ctx, cwd=self.path)

  def touch_log(self, ctx='log'):
    common.touch_log(log='%s.log' % ctx, cwd=self.path)

  @abc.abstractmethod
  def test(self):
    """
    Runs the app unit tests.

    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='test method not implemented')

  @abc.abstractmethod
  def validate(self):
    """
    Validates the app project before the build.

    This is the first step in the build process.

    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='validate method not implemented')    

  @abc.abstractmethod
  def prepare(self):
    """
    Prepares the app project to the build process, executes after the validate step is executed.

    This is the second step in the build process.

    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='prepare method not implemented')

  @abc.abstractmethod
  def build(self):
    """
    Builds the app project after the execution of validate and prepare.

    This is the third and last step in the build process.

    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='build method not implemented')

  @abc.abstractmethod
  def get_export_path(self):
    """
    Gets the build output file (an apk file for android builds) to be exported from the container.
    
    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='export method not implemented')

  def sign(self):
    """
    Gets the build output file (an apk file for android builds) to be exported from the container.
    
    Needs to be implemented by the subclass.
    """
    raise errors.MethodNotImplementedError(message='sign method not implemented')

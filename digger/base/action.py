import inspect
from six import with_metaclass

import digger
from digger import errors



__ALL__ = ['Argument', 'BaseAction']


class Argument(object):
  """Class that stores arguments (argparse based) in BaseAction class"""

  def __init__(self, name, flag, **kwargs):
    """
    Argument class constructor, should be used inside a class that inherits the BaseAction class.

    :param name(str): the optional argument name to be used with two slahes (--cmd)
    :param flag(str): a short flag for the argument (-c)
    :param \*\*kwargs: all keywords arguments supported for argparse actions.
    """
    self.name = name
    self.flag = flag
    self.options = kwargs


class MetaAction(type):
  """
  A metaclass that registers digger actions whenever the class is instantiated.
  """
  def __new__(cls, name, bases, namespace, **kwds):
    result = type.__new__(cls, name, bases, dict(namespace))
    digger.register_action(result)
    return result


class BaseAction(with_metaclass(MetaAction, object)):
  """
  A class that should be subclassed to create a new action in the cli parser.

  This action will become a subparser using its properties that subclass the class Argument as 
  optional arguments for the subparser in context.

  The subclass should define a ``_cmd_`` and ``_help_`` properties together with a instance handler method
  to receive the cli parameters.

  ``_cmd_`` becomes the subparser command and ``_help_`` is the help/info text about the command itself.

  It also implements the ``__call__`` method to be used as a function to parse the command args.

  Example:
  
  .. code-block:: python
     :linenos:

     class FooAction(BaseAction):
       _cmd_ = 'foo'
       _help_ = 'some foo random action'
       
       Argument('--say', '-s', default='hello', help='say something, default value is hello')

       def handler(self, say=None):
         print('Foo is saying: %s.' % say)
  """
  _cmd_ = None
  _help_ = None

  @classmethod
  def meta(cls, name):
    """
    Used to get the ``_cmd_`` and ``_help_`` class properties.
    
    :param name(str): the property name to be retrieved.

    Returns:
      The class properties that starts and ends with one underscore char based on the provided name.
    """
    return getattr(cls, '_%s_' % name)

  @classmethod
  def props(cls):
    """
    Class method that returns all defined arguments within the class.
    
    Returns:
      A dictionary containing all action defined arguments (if any).
    """
    return {k:v for (k, v) in inspect.getmembers(cls) if type(v) is Argument}

  def __call__(self, **kwargs):
    """
    Special method to call the handler instance method with a function interface.
    
    Returns:
      The handler instance method result.
    """
    return self.handler(**kwargs)

  def handler(self, **kwargs):
    """Method to be overwrtten  by the subclass to execute the actual command."""
    raise errors.MethodNotImplementedError(message='%s handler method not implemented' % self.meta('cmd'))



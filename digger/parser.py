import argparse

import digger
from digger import errors


_parser = argparse.ArgumentParser('AeroGear abcd')
_subparsers = _parser.add_subparsers()
_actions = {}


def register_action(action):
  """
  Adds an action to the parser cli.

  :param action(BaseAction): a subclass of the BaseAction class
  """
  sub = _subparsers.add_parser(action.meta('cmd'), help=action.meta('help'))
  sub.set_defaults(cmd=action.meta('cmd'))
  for (name, arg) in action.props().items():
    sub.add_argument(arg.name, arg.flag, **arg.options)
    _actions[action.meta('cmd')] = action


def register_actions(*args):
  """
  Accepts N arguments to be added as parser actions.

  :param \*args: N number of actions that inherits from BaseAction.
  """
  [register_action(action) for action in args]


def run(*args, **kwargs):
  """
  Runs the parser and it executes the action handler with the provided arguments from the CLI.

  Also catches the BaseError interrupting the execution and showing the error message to the user.

  Default arguments comes from the cli args (sys.argv array) but we can force those arguments  when writing tests:

  .. code-block:: python

    parser.run(['build', '--path', '/custom-app-path'].split())
  
  .. code-block:: python

    parser.run('build --path /custom-app-path')
  """
  cmd = _parser.parse_args(*args, **kwargs)
  if hasattr(cmd, 'cmd') is False:
    return _parser.print_help()
  Action = _actions.get(cmd.cmd)
  action = Action()
  try:
    action(**{k:getattr(cmd, k) for k in action.props().keys()})
  except errors.BaseError as e:
    e.print_error()


def bootstrap():
  register_actions(*digger.get_actions())

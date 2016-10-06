"""Commandline tool for container builds

CLI tool to build mobile apps inside a container

"""

__version__ = '0.2.0'


_actions = []


def register_action(action):
  if action.__name__ != 'BaseAction' and not action in _actions:
    _actions.append(action)
  

def get_actions():
  return _actions

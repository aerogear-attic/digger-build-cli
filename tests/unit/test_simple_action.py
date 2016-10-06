#!/usr/bin/env python
import sys

from digger import parser
from digger.base.action import BaseAction, Argument


class FooAction(BaseAction):
  _cmd_ = 'foo'
  _help_ = 'some random action'

  arg1 = Argument('--arg1', '-a1', default='default value', help='some help')

  def handler(self, arg1='default value'):
    print(arg1)


def test_foo_action_no_args(capsys):
  parser.bootstrap()
  parser.run(['foo'])
  out, err = capsys.readouterr()
  assert out == 'default value\n'

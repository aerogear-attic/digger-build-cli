"""
  This file is a smoke test for the CLI parsing.
  Commands are executed as they are executed from a command line.
"""

from __future__ import print_function

import os

import pytest

from digger import parser
from digger.helpers import android as android_helper


current_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = '%s/tmp' % current_dir
app_dir = '%s/welcome-android-gradle-master' % tmp_dir


@pytest.fixture
def cli():
  # do not remove following line even though your IDE
  # tells imports are not used.
  # this line registers the actions.
  # noinspection PyUnresolvedReferences
  from digger import actions
  parser.bootstrap()
  return parser


def test_inspect(cli):
  cmd = 'inspect --path %s' % app_dir
  parser.run(cmd.split())


def test_build(cli):
  cmd = 'build --path %s' % app_dir
  parser.run(cmd.split())


def test_log(cli):
  cmd = 'log --path %s' % app_dir
  parser.run(cmd.split())


def test_test(cli):
  cmd = 'test --path %s' % app_dir
  parser.run(cmd.split())


def test_export(cli):
  cmd = 'export --path %s' % app_dir
  parser.run(cmd.split())


def test_sign(capsys, cli):
  cmd = 'export --path %s' % app_dir
  parser.run(cmd.split())
  out, err = capsys.readouterr()
  apk = [f.replace('\n', '') for f in out.split(',') if f.replace('\n', '').endswith('app-debug-unaligned.apk')]
  apk = apk[0]
  cmd = 'sign --path %s --binary %s --name welcome-gradle' % (app_dir, apk)
  parser.run(cmd.split())
  assert len([i for i in android_helper.find_apks(app_dir) if 'welcome-gradle.apk' in i]) > 0

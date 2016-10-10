import os

import pytest

from digger import parser
from digger import builds
from digger.helpers import android as android_helper


current_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = '%s/../tmp' % current_dir
app_dir = '%s/welcome-android-gradle-master' % tmp_dir
keystore = '%s../odra.keystore' % current_dir


@pytest.fixture
def cli():
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
  apk = [f.replace('\n', '') for f in out.split(',') if f.replace('\n', '').endswith('-debug-unaligned.apk')]
  apk = apk[0]
  cmd = 'sign --path %s --binary %s --name blank-gradle' % (app_dir, apk)
  parser.run(cmd.split())
  out, err = capsys.readouterr()
  assert len([i for i in android_helper.find_apks(app_dir) if 'blank-gradle.apk' in i]) > 0

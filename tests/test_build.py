import os
import shutil

import pytest

from digger import builds

current_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = '%s/tmp' % current_dir
zip_dir = '%s/fixtures' % current_dir


@pytest.fixture
def clean_tmp_folder():
  if os.path.exists(tmp_dir) is False:
    os.makedirs(tmp_dir)
  for folder in os.listdir(tmp_dir):
    shutil.rmtree('%s/%s' % (tmp_dir, folder))


@pytest.fixture
def file_list():
  return ['%s/%s' % (zip_dir, item) for item in os.listdir(zip_dir)]


@pytest.fixture
def folder_list(file_list):
  folders = []
  for path in file_list:
    fname = path.split('/')[-1:][0].replace('.zip', '')
    project_path = '%s/%s' % (tmp_dir, fname)
    folders.append(project_path)
  return folders


@pytest.mark.usefixtures('download_templates')
def test_unzip(download_templates, clean_tmp_folder, folder_list):
  for path in folder_list:
    _path = '%s%s' % (path.replace('/tmp/', '/fixtures/'), '.zip')
    project = builds.GradleBuild.from_zip(_path, tmp_dir)
    assert os.path.exists(path) is True


def test_file_list(file_list):
  def check(folder, item):
    assert item.startswith(folder)
  [check(zip_dir, item) for item in file_list]


def test_inspect(capsys, folder_list):
  for folder in folder_list:
    project = builds.GradleBuild(path=folder)
    out = project.inspect()
    assert len(out) > 0


def test_projects(capsys, folder_list):
  for project in folder_list:
    project = builds.from_path(project)
    project.validate()
    project.prepare()
    project.build()
    paths = project.get_export_path()
    assert len(paths) > 0
    for path in paths.split(','):
      assert os.path.exists(path)

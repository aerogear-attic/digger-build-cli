import os

import pytest
import requests


@pytest.fixture
def colors():
  class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
  return colors


@pytest.fixture
def template_names():
  #commented apps need special treatment
  names = [
    #'blank-android-app',
    'blank-android-gradle',
    'helloworld-android-gradle',
    #'helloworld-android',
    'oauth-android-app',
    #'pushstarter-android-app',
    'saml-android-app',
    'sync-android-app',
    'welcome-android-gradle'
    #'welcome-android'
  ]
  return names


@pytest.fixture
def template_urls(template_names):
  branch = 'master'
  url = 'https://github.com/feedhenry-templates/%s/archive/%s.zip'
  return [url % (tmpl, branch) for tmpl in template_names]


@pytest.fixture(params=['./tests/fixtures'])
def download_templates(request, template_urls, template_names, colors):
  branch = 'master'
  folder = request.param
  if os.path.exists(folder) is False:
    os.makedirs(folder)
  for url in template_urls:
    fname = template_names[template_urls.index(url)]
    print('%s==>%s Downloading %s template' % (colors.BOLD, colors.ENDC, fname))
    r = requests.get(url, stream=True)
    if r.status_code != 200:
      print('%s==>%s Invalid url: %s (%s)' % (colors.FAIL, colors.ENDC, url, r.status_code))
      continue
    print('%s==>%s Downloaded %s template' % (colors.BOLD, colors.ENDC, fname))
    print('%s==>%s Saving %s template' % (colors.BOLD, colors.ENDC, fname))
    with open('%s/%s-%s.zip' % (folder, fname, branch), 'wb+') as f:
      chunks = r.iter_content(chunk_size=1024)
      [f.write(chunk) for chunk in chunks if chunk]
    print('%s==>%s Saved %s template' % (colors.OKGREEN, colors.ENDC, fname))


@pytest.fixture(params=['./tests/zipfiles'])
def download_devnexus():
  branch = 'master'
  folder = request.param
  url = 'https://github.com/odra/devnexus-android/archive/%s.zip' % branch

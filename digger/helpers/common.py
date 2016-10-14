import fnmatch
import os
import subprocess
import sys
import io
import os
from contextlib import redirect_stdout
import copy

def run_cmd(cmd, log='log.log', cwd='.', stdout=sys.stdout, bufsize=1, encode='utf-8'):
  """
  Runs a command in the backround by creating a new process and writes the output to a specified log file.

  :param log(str) - log filename to be used
  :param cwd(str) - basedir to write/create the log file
  :param stdout(pipe) - stdout process pipe (can be default stdout, a file, etc)
  :param bufsize(int) - set the output buffering, default is 1 (per line)
  :param encode(str) - string encoding to decode the logged content, default is utf-8

  Returns:
    The process object
  """
  logfile = '%s/%s' % (cwd, log)
  
  if os.path.exists(logfile):
    os.remove(logfile)
  proc_args = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'cwd': cwd,
    'universal_newlines': True
  }

  proc = subprocess.Popen(cmd, **proc_args)
  
  while True:
    line = proc.stdout.readline()
    if proc.poll() is None:
      stdout.write(line)
    else:
      break
  out, err = proc.communicate()

  with open(logfile, 'w') as f:
    if out:
      f.write(out)
    else:
      f.write(err)


def find(root_dir, pattern='*'):
  matches = []
  for (root, dirnames, filenames) in os.walk(root_dir):
    for filename in fnmatch.filter(filenames, pattern):
      matches.append(os.path.join(root, filename))
  return matches


def touch_log(log, cwd='.'):
  """
  Touches the log file. Creates if not exists OR updates the modification date if exists.
  :param log:
  :return: nothing
  """
  logfile = '%s/%s' % (cwd, log)
  with open(logfile, 'a'):
    os.utime(logfile, None)

import fnmatch
import os
import subprocess
import sys


def run_cmd(cmd, log='log.log', cwd='.', stdout=subprocess.PIPE, bufsize=1, encode='utf-8'):
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
  #with open(logfile, 'a') as fh:
  with subprocess.Popen(cmd, stdout=stdout, bufsize=bufsize, cwd=cwd) as proc:
    with open(logfile, 'ba') as fh:
      fh.write(proc.stdout.read())
    #subprocess.Popen(cmd, stdout=stdout, bufsize=bufsize, cwd=cwd)
    #process.wait()
  '''
  with open(logfile, 'a') as f:
    for line in iter(process.stdout.readline, b''):
      chunk = line.decode(encode)
      print(chunk)
      f.write(chunk)
  process.stdout.close()
  '''


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
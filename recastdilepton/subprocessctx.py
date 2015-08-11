import logging
from contextlib import contextmanager
import subprocess
import os

log = logging.getLogger(__name__)

@contextmanager
def subprocess_in_env(envscript = None,workdir = None, outlog = os.devnull, errlog = os.devnull):
  if not workdir:
    workdir = os.getcwd()
    
  if not os.path.exists(workdir):
    os.makedirs(workdir)
    
  setupenv = 'source {0} && '.format(os.path.abspath(envscript)) if envscript else ''
  
  #helpful SO lesson on scoping: 
  #http://stackoverflow.com/questions/4851463/python-closure-write-to-variable-in-parent-scope#comment5388645_4851555

  def check_call(what):
    try:
      subprocess.check_call('{0} {1}'.format(setupenv,what),
        cwd = workdir, shell = True, stdout = open(outlog,'w'), stderr = open(outlog,'w'))
    except subprocess.CalledProcessError:
      log.error('subprocess failed: called with {0} {1}'.format(setupenv,what))
      raise RuntimeError
  yield check_call

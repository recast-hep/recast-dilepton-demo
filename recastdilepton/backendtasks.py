import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
  workdir = 'workdirs/{}'.format(ctx['jobguid'])

  proc = subprocess.Popen(['recastworkflow-dilepton',workdir], stderr = subprocess.PIPE)  
  proc.wait()

def resultlist():
  return ['plots','mini.root','Output.root']

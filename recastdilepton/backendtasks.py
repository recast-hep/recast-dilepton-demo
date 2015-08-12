import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
  workdir = 'workdirs/{}'.format(ctx['jobguid'])

  proc = subprocess.Popen(['recastworkflow-dilepton',workdir], stderr = subprocess.PIPE)

  while proc.poll() is None:
    s = proc.stderr.readline()
    lvl,msg =  s.strip().split(':',1)
    log.log(getattr(logging,lvl),msg)
    time.sleep(0.01)

  log.info('finished')

def resultlist():
  return ['plots','mini.root','Output.root']

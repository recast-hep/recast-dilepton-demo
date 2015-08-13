import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
  workdir = 'workdirs/{}'.format(ctx['jobguid'])

  proc = subprocess.Popen(['recastworkflow-dilepton',workdir], stderr = subprocess.STDOUT, stdout = subprocess.PIPE)

  while proc.poll() is None:
    s = proc.stdout.readline()
    splitup = s.strip().split(':',1)
    if len(splitup)==2:
      try:
        log.log(getattr(logging,splitup[0]),splitup[1])
      except AttributeError:
        log.info(s)
    else:
      log.info(s)

    time.sleep(0.01)

  log.info('finished')

def resultlist():
  return ['fitresults.yaml','prepare.yield','*.log']

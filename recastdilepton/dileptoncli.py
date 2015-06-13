import click
import adagetasks
import logging
import adage
import os

from adage import mknode

def build_dag(workdir):
  rules = []
  dag = adage.mk_dag()
  
  def inwrk(path):
    return '{0}/{1}'.format(os.path.abspath(workdir),path)

  def rsrc(path):
    return pkg_resources.resource_filename('recastdilepton','resources/{}'.format(path))

  download_stage = mknode(dag,adagetasks.downlaod.s(inwrk('inputs/info.yaml'),inwrk('grid_download'),inwrk('files.list')))

  miniroot_stage = mknode(dag,adagetasks.createminiroot.s(workdir,inwrk('files.list')), depends_on = [download_stage])

  make_SR_histos_stage = mknode(dag,adagetasks.make_SR_histos.s(workdir,inwrk('mini.root')), depends_on = [miniroot_stage])

  make_plots = mknode(dag, adagetasks.plot_SRs.s(inwrk('Output.root'),inwrk('plots')),depends_on = [make_SR_histos_stage])

  return dag,rules


@click.command()
@click.argument('workdir')
@click.option('-l','--logger',default = __name__)
def dileptoncli(workdir,logger):
  log = logging.getLogger(logger)
  adagetasks.log = log

  dag,rules = build_dag(workdir)
  log.info('running dilepton from workdir {0}'.format(workdir))
 
  #adage.rundag(dag,rules,loggername = logger, track = True, workdir = workdir, trackevery = 60)
  adage.rundag(dag,rules)

  log.info('done')


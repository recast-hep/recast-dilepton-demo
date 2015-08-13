import click
import adagetasks
import logging
import adage
import os
import yaml

from fileaccess import rsrc,workdir_access_methods
from adage import mknode




def build_dag(workdir):
  rules = []
  dag = adage.mk_dag()

  inwrk,inpt = workdir_access_methods(workdir)

  info = yaml.load(open(inpt('input.yaml')))
  download = mknode(dag,adagetasks.download.s(info['datasetname'],inwrk('grid_download'),inwrk('files.list')))

  miniroot = mknode(dag,adagetasks.createminiroot.s(
    inwrk('files.list'),
    inwrk('mini.root'),
    inwrk('mini.log')
  ),
  depends_on = [download])

  prepareAndYields = mknode(dag,adagetasks.prepareAndYields.s(
    info['modelName'],
    inpt(info['efficiencyFile']),
    inpt(info['xsectionFile']),
    inwrk('mini.root'),
    inwrk('prepare.root'),
    inwrk('prepare.yield'),
    inwrk('prepare.log'),
  ),
  depends_on = [miniroot])

  fit = mknode(dag, adagetasks.runFit.s(
    inwrk('fitworkdir'),
    inwrk('prepare.root'),
    inwrk('fit.tgz'),
    'fromscript.tgz',
  ),
  depends_on = [prepareAndYields])

  postFit = mknode(dag, adagetasks.extractFitResults.s(
    inwrk('fit.tgz'),
    inwrk('postfitworkdir'),
    info['modelName'],
    inwrk('fitresults.yaml'),
  ),
  depends_on = [fit])

  return dag,rules



@click.command()
@click.argument('workdir')
@click.option('-l','--logger',default = __name__)
def dileptoncli(workdir,logger):
  logging.basicConfig(level = logging.INFO)

  log = logging.getLogger(logger)
  dag,rules = build_dag(workdir)
  log.info('running dilepton from workdir {0}'.format(workdir))
  adage.rundag(dag,rules)

  log.info('done')

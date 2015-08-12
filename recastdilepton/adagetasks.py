from adage import adagetask

import subprocess
import shutil
import os
#import ROOT
import yaml

from fileaccess import rsrc
from subprocessctx import subprocess_in_env

@adagetask
def download(inputdataset,downloaddir,listfilename):
  print "skipping download"  
  with subprocess_in_env(envscript = rsrc('downloadenv.sh')) as check_call:
    check_call('dq2-get -H {} {}'.format(downloaddir ,inputdataset))
  
  with open(listfilename,'w') as listfile:
    for file in os.listdir(downloaddir):
      listfile.write('{}/{}\n'.format(os.path.abspath(downloaddir),file))


@adagetask
def createminiroot(inputlist,outminifile,outputlog):
  with subprocess_in_env(envscript = rsrc('minienv.sh'), outlog = outputlog, errlog = outputlog+'.err') as check_call:
    check_call('./DileptonAnalysis -m {} -mc -truth -maxsyst 1 -unblind -nomllalpgenfilter -f {}'.format(outminifile,inputlist,outputlog))


@adagetask
def prepareAndYields(model,efficiencyFile,xsectionFile,inputroot,outputroot,outputyield,outputlog):
  with subprocess_in_env(envscript = rsrc('prepareenv.sh'), outlog = outputlog, errlog = outputlog) as check_call:
    check_call('python preparehistfit.py {inputroot} {inputeff} {xsecfile} {modelName} {outputroot} {outputyield}'.format(
        inputroot   = inputroot,
        inputeff    = efficiencyFile,
        xsecfile    = xsectionFile,
        modelName   = model,
        outputroot  = outputroot,
        outputyield = outputyield)
    )

@adagetask
def runFit(fitworkdir,fitinputroot,fitoutputgz,fitcodearchive):
  with subprocess_in_env(envscript = rsrc('fitenv.sh')) as check_call:
    check_call('{script} {workdir} {input} {output} {code}'.format(
      script = './run_fit_recast.sh',
      workdir = fitworkdir,
      input = fitinputroot,
      output =  fitoutputgz,
      code = fitcodearchive
      )
    )

@adagetask
def extractFitResults(fitarchive,postfitworkdir,modelname,outputyaml):
  with subprocess_in_env(envscript = rsrc('fitenv.sh')) as check_call:
    check_call('{script} {fitarchive} {workdir} {model} {output}'.format(
      script = './post_fit.sh',
      fitarchive = fitarchive,
      workdir = postfitworkdir,
      model = modelname,
      output = outputyaml
      )
    )

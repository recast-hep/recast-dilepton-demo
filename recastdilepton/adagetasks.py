from adage import adagetask

import subprocess
import shutil
import os
import ROOT
import yaml

import pkg_resources
def rsrc(path):
  return pkg_resources.resource_filename('recastdilepton','resources/{}'.format(path))

@adagetask
def downlaod(infoyaml,downloaddir,listfilename):
  inputdataset = yaml.load(open(infoyaml))['inputdataset']  
  subprocess.call('source {} && dq2-get -H {} {}'.format(rsrc('downloadenv.sh'),downloaddir ,inputdataset), shell = True)
  with open(listfilename,'w') as listfile:
    for file in os.listdir(downloaddir):
      listfile.write('{}/{}\n'.format(os.path.abspath(downloaddir),file))

@adagetask
def createminiroot(workdir,filelist):
  coderoot = '{}/d3pdreader'.format(os.environ['DILEPTONCODE'])
  minirootdest = '{}/mini.root'.format(coderoot)
  if  os.path.exists(minirootdest):
    os.remove(minirootdest)
  print "GO"
  subprocess.call('source {} && ./DileptonAnalysis -maxsyst 1 -mc -m -f {}'.format(rsrc('ntupleenv.sh'),filelist),
  			  shell = True,stdout = open('{}/mini.log'.format(workdir),'w')
				      ,stderr = open('{}/mini.err'.format(workdir),'w'))
  print "DONE"
  print "createmini done"
  assert os.path.exists(minirootdest)
  shutil.move(minirootdest,'{}/mini.root'.format(workdir))

@adagetask
def make_SR_histos(workdir,minirootfile):
  coderoot = '{}/fasthistomaker'.format(os.environ['DILEPTONCODE'])
  outputrootdest = '{}/Output.root'.format(coderoot)
  if  os.path.exists(outputrootdest):
    os.remove(outputrootdest)
  subprocess.call('source {} && ./fasthistomaker {}'.format(rsrc('fastshistoenv.sh'),minirootfile), shell = True)
  assert os.path.exists(outputrootdest)
  shutil.move(outputrootdest,'{}/Output.root'.format(workdir))

@adagetask
def plot_SRs(outputrootfile,outputdir):
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)

  f = ROOT.TFile.Open(outputrootfile)
  c = ROOT.TCanvas()
  allplotsname = '{}/plots.pdf'.format(outputdir)
  c.SaveAs(allplotsname+'[')
  for k in f.GetListOfKeys():
    if '_SR' in k.GetName():
      hist = f.Get(k.GetName())
      hist.SetFillColor(38)
      hist.Draw('hist')
      c.SaveAs(allplotsname)
      c.SaveAs('{}/{}'.format(outputdir,k.GetName()+'.png'))
  c.SaveAs(allplotsname+']')


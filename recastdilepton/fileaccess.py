import os
import pkg_resources

#resource file access
def rsrc(path):
  return pkg_resources.resource_filename('recastdilepton','resources/{}'.format(path))

def workdir_access_methods(workdir):
  #workdir file access
  def inwrk(path):
    return '{0}/{1}'.format(os.path.abspath(workdir),path)
  
  #input file access
  def inpt(path):
    return inwrk('inputs/{}'.format(path))
  
  return inwrk,inpt
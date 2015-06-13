#first argument is code directory

kinit lheinric@CERN.CH -k -t ~/recast_auth/lheinric.keytab 
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup 17.7.0 slc5
export CXXFLAGS="-D__USE_XOPEN2K8${CXXFLAGS:+ ${CXXFLAGS}}"

cd $1
svn co svn+ssh://lheinric@svn.cern.ch/reps/atlasinst/Institutes/Stockholm/SUSY/weakprod_21fb/d3pdreader/trunk d3pdreader

cd d3pdreader
./update_packages.sh 

patch -p0 -i ../printf_bug.diff

./make.sh 2>&1 | tee make.log

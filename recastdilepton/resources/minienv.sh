#!/bin/zsh
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
asetup 17.7.0 slc5
export CXXFLAGS="-D__USE_XOPEN2K8${CXXFLAGS:+ ${CXXFLAGS}}"
cd $DILEPTONCODE/dilepton_d3pdreader

echo "we are now in $PWD trying to source prep.sh"
ls $PWD|grep prep.sh
echo "grep above"
source $PWD/prep.sh


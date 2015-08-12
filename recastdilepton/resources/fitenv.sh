echo "setting environment for fitting"
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh
localSetupROOT 5.34.14-x86_64-slc5-gcc43-opt --quiet
cd $DILEPTONCODE/pMSSM-TwoLep-Fit

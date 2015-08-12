set -e
~/recast_auth/gettoken.sh
export DILEPTONCODE=$PWD/code
mkdir $DILEPTONCODE
cd code
svn co svn+ssh://svn.cern.ch/reps/atlas-lheinric/recast_dilepton/dilepton_d3pdreader/trunk dilepton_d3pdreader
git clone https://github.com/lukasheinrich/pMSSM-TwoLep-Glue.git   
git clone https://github.com/lukasheinrich/pMSSM-TwoLep-Fit.git

(../recastdilepton/resources/minienv_mk.sh)
(source ../recastdilepton/resources/fitenv.sh && ./create_fit_archive.sh svn+ssh://svn.cern.ch/reps/atlas-lheinric/recast_dilepton/histfitter_code/trunk fromscript.tgz)

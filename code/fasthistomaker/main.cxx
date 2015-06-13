// Histo maker by projection
// Stockholm University - Experimental Particle Physics Group 2013-03-03
// TODO
// keep h_total_norm done
// read input        done
// save output       done
// binning           done
// event weight      done

///////// Loop over samples and directories in python ///////
// Create:
//  - a vector of channels
//  - a vector of cut levels
//         each cut has a CutName to go into the histo name and a string to make a TCut
//  - a vector of variables 
//  - a 3D matrix to define plots to be made enable_histo[nchannels][ncuts][nvariables] = true / false
//  - for each element of enable_histo  = 1  book an histogram  <channel>_<variable>_<cutlevel>



#include <vector>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <TString.h>
#include <TROOT.h>
#include <TFile.h>
#include <TH1F.h>
#include <TCut.h>
#include <TChain.h>


using namespace std;

int main(int argc, char **argv) 
{
  Bool_t DEBUG=false;

  const   Int_t nchannels=3;
  enum    Channels {ee,mm,em};
  TString ChannelName[nchannels]={"ee","mm","em"};  // will put together emu and mue

  ////////////////////////////////////////////////
  ///////////////  Cut definitions ///////////////
  ////////////////////////////////////////////////

  TString    ChannelSelection[nchannels];
  ChannelSelection[ee]="(lepton1_pdgid==11&&lepton2_pdgid==11)";
  ChannelSelection[mm]="(lepton1_pdgid==13&&lepton2_pdgid==13)";
  ChannelSelection[em]="((lepton1_pdgid==11&&lepton2_pdgid==13)||(lepton1_pdgid==13&&lepton2_pdgid==11))";

  const   Int_t             ncuts=15;

  TString HistoCutName      [ncuts]; // name of the cuts as they should appear in the name of the histo

  TString EventWeightString [ncuts]; // should contain pile up, trigger, lepton, etc...

  TString    CutDefinition  [ncuts]; // Actual cut criteria to be used in the projection

  TString    BaselineLLOSCut="(lepton1_issignal==1 && lepton2_issignal==1 && lepton1_charge*lepton2_charge<0 && mll>20)";


  ////// Initialise the cuts from textfile ////
  //    format of each line in the file cut_definitions.txt :
  //    cutname_as_in_the_output.root  | Cut_definition |  weights_to_be_used
  Int_t MAXCUTS=0;
  FILE *f_cuts;
  char cut_name[40];
  char cut_definition[500];
  char weight_name[500];
  f_cuts=fopen("cut_definitions.txt", "r");
  while ( fscanf(f_cuts,"%s",cut_name) != EOF )
    {
      fscanf(f_cuts,"%s %s",cut_definition,weight_name);

      if(DEBUG) {
        cout << "cut_name           = " << cut_name       << endl;
        cout << "cut_definition     = " << cut_definition << endl;
        cout << "weight_name        = " << weight_name    << endl << endl;
      }
      HistoCutName     [MAXCUTS] = cut_name;
      CutDefinition    [MAXCUTS] = BaselineLLOSCut+"&&"+TString(cut_definition);
      EventWeightString[MAXCUTS] = weight_name;

      MAXCUTS++;
    } // end while
  fclose(f_cuts);





  //////////////////////////////////////////////////////////////////
  ///// define the variables and the histo binning per variable ////
  //////////////////////////////////////////////////////////////////
  const   Int_t nvariables=30;
  TString VariableName   [nvariables];  // name as it will appear in histo
  TString VariableFormula[nvariables];  // formula used to compute that variable

  Int_t  nbins[nvariables];
  Float_t xmin[nvariables];
  Float_t xmax[nvariables];

  ////// define 3D matrix of histos to be done ////////
  Bool_t enable_histo[nchannels][ncuts][nvariables]={};
  for(Int_t ichan=0;ichan<nchannels;++ichan){
    for(int icut = 0;icut < ncuts && icut<MAXCUTS; ++icut) {
      for(int ivar = 0;ivar < nvariables; ++ivar) {
	enable_histo[ichan][icut][ivar]=true;
	if(DEBUG) cout << "enable_histo[][][]" << enable_histo[ichan][icut][ivar] << endl;
      }
    }
  }

  // here is an initialisation "by hand"
  //   enable_histo[ee][0][0]=true;
  //   enable_histo[ee][1][1]=true;
  //   // need to allow for different names from different channels
  //   VariableName[0]="el1el2_Mass"; VariableFormula[0]="mll";                                    nbins[0]=200; xmin[0]=20; xmax[0]=400;
  //   VariableName[1]="el1mu1_Mass"; VariableFormula[1]="mll";                                    nbins[1]=200; xmin[1]=20; xmax[1]=400;
  //   VariableName[2]="mu1mu2_Mass"; VariableFormula[2]="mll";                                    nbins[2]=200; xmin[2]=20; xmax[2]=400;
  //   VariableName[3]="mll";         VariableFormula[3]="mll";                                    nbins[3]=200; xmin[3]=20; xmax[3]=400;
  //   VariableName[4]="METrel";      VariableFormula[4]="sqrt(metrelx*metrelx+metrely*metrely)";  nbins[4]= 40; xmin[4]= 0; xmax[4]=400;
  

  ////// Initialise the variables from textfile ////
  // the file contains:
  // enable_flag   |     variable_name_to_appear_in_histo |   definition_from_mini_susy |  nbins |  xmin |  xmax
  Int_t MAXVARIABLES=0;
  Int_t enable;
  FILE *f_variables;
  char variable_name[100];
  char variable_formula[200];
  int  nbin_from_file;
  float xmin_from_file, xmax_from_file;
  f_variables=fopen("variable_definitions.txt", "r");
  while ( fscanf(f_variables,"%i",&enable) != EOF )
    {
      if(DEBUG) cout << "enable = " << enable << endl;
      fscanf(f_variables,"%s %s %i %f %f",variable_name,variable_formula,&nbin_from_file,&xmin_from_file,&xmax_from_file);

      if(DEBUG) {
        cout << "variable_name     = " << variable_name     << endl;
        cout << "variable_formula  = " << variable_formula  << endl;
	cout << "nbin_from_file    = " << nbin_from_file << endl;
	cout << "xmin_from_file    = " << xmin_from_file << endl;
	cout << "xmax_from_file    = " << xmax_from_file << endl;
      }
      VariableName   [MAXVARIABLES] =variable_name;
      VariableFormula[MAXVARIABLES] =variable_formula;
      nbins          [MAXVARIABLES] =nbin_from_file;
      xmin           [MAXVARIABLES] =xmin_from_file;
      xmax           [MAXVARIABLES] =xmax_from_file;

      MAXVARIABLES++;
    } // end while
  fclose(f_variables);



  ////////// Open input file 
  if(argc<=1) {
    cout << "No input file name provided : going to abort. "<< endl;
    cout << "need to provide the file name as first argument " << endl;
    abort();
  }
  TH1F  * h_total_norm = new TH1F("h_total_norm","integral is sum of mc weights",10,190000,230000);  

  TString InputFileName=argv[1];
  cout << "Going to open input file with name : " << InputFileName.Data() << endl;

  ////////// Create the output .root file /////////
  TString OutName="Output.root";
  TFile * outfile = new TFile(OutName, "RECREATE");

  //////// Fetch the normalisation histogram from the input histo
  TFile * inputfile  = new TFile(InputFileName, "READ"); 

  h_total_norm->Sumw2();
  //h_total_norm->SetDirectory(outfile);  gDirectory->cd(OutName+":/");
  h_total_norm= (TH1F*) inputfile->Get("h_total_norm"); 

  //h_total_norm->SetDirectory(outfile);  gDirectory->cd(OutName+":/");
  gDirectory->cd(OutName+":/");
  h_total_norm->Write("h_total_norm",TObject::kWriteDelete);

  if(DEBUG) {
    cout << "h_total_norm->GetEntries(); (1) = " << h_total_norm->GetEntries() << endl;
    cout << "h_total_norm->GetName()     (1) = " << h_total_norm->GetName() << endl;
    cout << "h_total_norm->Integral();   (1) = " << h_total_norm->Integral() << endl;
  }
  inputfile->Close();



  TChain * fChain = new TChain ("none/minisusy");
  fChain->Add(InputFileName);

//   fChain->SetBranchStatus("*",0); 
//   fChain->SetBranchStatus("NL20",1); 
//   fChain->SetBranchStatus("NB20new",1); 
//   fChain->SetBranchStatus("NF30new",1); 
//   fChain->SetBranchStatus("mll",1); 
//   fChain->SetBranchStatus("mt2",1); 
//   fChain->SetBranchStatus("metrelx",1); 
//   fChain->SetBranchStatus("metrely",1); 
//   fChain->SetBranchStatus("mc_weight",1); 
//   fChain->SetBranchStatus("pu_weight_unblind",1); 
//   fChain->SetBranchStatus("le_weight",1); 
//   fChain->SetBranchStatus("tr_weight_unblind",1); 
//   fChain->SetBranchStatus("hfor_weight",1); 
//   fChain->SetBranchStatus("bt_weight",1); 


//    fChain->SetBranchStatus("bt_weight_vector",1); 
//    vector<float>   *bt_weight_vector;
//    TBranch        *b_bt_weight_vector; 
//    fChain->SetBranchAddress("bt_weight_vector", &bt_weight_vector, &b_bt_weight_vector); 

//   fChain->SetBranchStatus("lepton1_pdgid",1); 
//   fChain->SetBranchStatus("lepton2_pdgid",1); 
//   fChain->SetBranchStatus("lepton1_issignal",1); 
//   fChain->SetBranchStatus("lepton2_issignal",1); 
//   fChain->SetBranchStatus("lepton1_charge",1); 
//   fChain->SetBranchStatus("lepton2_charge",1); 



  if(DEBUG) { cout << "InputFileName is " << InputFileName << endl; }


  ////////// Define the weights /////////
  TString WeightString=""; // this will be the product of the weight and the cut


  ////////// Book and bin the histograms ///////
  TString histoName;
  TH1F * h_histo [nchannels][ncuts][nvariables];
  for(Int_t ichan=0;ichan<nchannels;++ichan){

    for(int icut = 0;icut < ncuts && icut<MAXCUTS; ++icut) {

      for(int ivar = 0;ivar < nvariables && ivar<MAXVARIABLES ; ++ivar) {

	if(enable_histo[ichan][icut][ivar]) {
	  
	  histoName=ChannelName[ichan]+"_"+VariableName[ivar]+"_"+HistoCutName[icut];
	  
	  if(DEBUG) {	  cout << "creating histogram for cut: "<< histoName.Data() << endl; }
	  
	  h_histo[ichan][icut][ivar] = new TH1F(histoName.Data(), histoName.Data(), nbins[ivar], xmin[ivar], xmax[ivar]);
	  h_histo[ichan][icut][ivar]->Sumw2();
	  gDirectory->cd(OutName+":/");

	} // if enable_histo[ichan][icut][ivar]

      } // ivar

    } // icut

  } // ichan

  ////////// project the relevant histograms /////
  for(Int_t ichan=0;ichan<nchannels;++ichan){

    for(int icut = 0;icut < ncuts && icut<MAXCUTS ; ++icut) {

      for(int ivar = 0;ivar < nvariables && ivar < MAXVARIABLES; ++ivar) {
	if(DEBUG) {	 cout << "ichan = " << ichan << " icut = " << icut << " ivar = " << ivar <<  " enable_histo = " << enable_histo[ichan][icut][ivar] << endl; }
	if(enable_histo[ichan][icut][ivar]) {
	  
	  histoName=ChannelName[ichan]+"_"+VariableName[ivar]+"_"+HistoCutName[icut];

	  //WeightString = "(mc_weight*pu_weight_unblind*le_weight*tr_weight_unblind*hfor_weight*bt_weight_vector[0])*(";

	  WeightString  = EventWeightString[icut];         // pileup, trigger , leptons, btag....
	  WeightString +="*(";
 	  WeightString +=CutDefinition[icut];       // ZV or ZW, MET, jets, ....
 	  WeightString +="&&"+(ChannelSelection[ichan]); // ee or mm or em
 	  WeightString +=")" ;
  
	  if(DEBUG) {	
	    cout << "filling histogram  = "<< histoName.Data() << endl;
	    
	    cout << "variable formula   = " << VariableFormula[ivar].Data() << endl;
	    
	    cout << "WeightString       = " << WeightString.Data() << endl << endl;
	  } // DEBUG
	  if(DEBUG) {cout << "test 20095"<< endl; }
	  fChain->Project(histoName,(VariableFormula[ivar]).Data(),WeightString.Data());
	  if(DEBUG) {cout << "test 20096"<< endl; }
	} // if enable_histo[ichan][icut][ivar]
	if(DEBUG) {cout << "test 20097"<< endl; }
      } // ivar
      if(DEBUG) {cout << "test 20098"<< endl; }
    } // icut
    if(DEBUG) {cout << "test 20099"<< endl; }
  } // ichan
  delete fChain;
  if(DEBUG) {cout << "test 20100"<< endl; }
  outfile->Write(0);
  if(DEBUG) {cout << "test 20101"<< endl; }
  outfile->Close();
  if(DEBUG) {cout << "test 20102"<< endl; }
  delete outfile;
  if(DEBUG) {cout << "test 20103"<< endl; }
} // main


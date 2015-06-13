# run with python ./script.py
# This script reads in all the mini.root and makes OutputD4PD.root

from ROOT import *
import sys, os, string, shutil

gROOT.Reset()

# data directory
#inputdir="data/"

# contains all  MC
inputdir="mc/"

tag1="MERGE.ANA13."
tag2="mini.root"
tag3="mc12.10"

for file in os.listdir(inputdir) :
    if( tag1  in file and tag2 in file and tag3 in file) :
                    print "file     = ",file
                    print "inputdir = ",inputdir

                    AddSystName=""

                    # 0     1      2       3         4                                  5    6
                    # MERGE.ANA13. data12. periodJp. Egamma.                            v03. mini.root
                    # MERGE.ANA13. mc12.   116602.   gg2zzjimmy_auet2ct10_zz4mu_mtrigp. v03. Output.root
                    file_fields=file.rsplit(".")
                    newfilename = file_fields[0]+"."+file_fields[1]+"."+file_fields[2]+"."+file_fields[3]+"."+file_fields[4]+AddSystName+"."+file_fields[5]+".Output.root"

                    command="./fasthistomaker "+inputdir+"/"+file
                    print "command = ",command
                    os.system(command)
                    
                    command ="mv Output.root ./"+newfilename
                    print "command = ",command
                    os.system(command)

print "the end"

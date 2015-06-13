
ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --libs)  -lTreePlayer 
ROOTGLIBS     = $(shell root-config --glibs) -lTreePlayer 

CXX           = g++
CXXFLAGS      =-I$(ROOTSYS)/include -Wall -pedantic 

LD            = g++
SOFLAGS       = -m32


CXXFLAGS      = $(ROOTCFLAGS)
LIBS          = $(ROOTLIBS)
GLIBS         = $(ROOTGLIBS)

SHELL     =/bin/bash
CXXFLAGS  += -I ${ROOTSYS}/include  

ObjSuf=o

SRC  = ${shell ls *.cxx}
OBJS = ${SRC:.cxx=.$(ObjSuf)}

all:  fasthistomaker

fasthistomaker: $(OBJS) 
	$(CXX) -o $@ $(OBJS) $(CXXFLAGS) $(LIBS)

%.$(ObjSuf):%.cxx
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f *.o *.o~ core

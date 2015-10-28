#!/software/python-2.7.2-gnu/bin/python
import os
import re
import pp
import sys
import glob
import math
import commands
import linecache
import exc
import threading
import subprocess
import multiprocessing 
import time
import signal
import Queue
import shutil
import overlap
import numpy
from numpy import *

queue= Queue.Queue()

class Fchk(threading.Thread):
    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q= q
        print "Started"
    def run(self):
        while True:
            data= self.q.get()
            if type(data).__name__=='str':
                p= subprocess.Popen(data.rsplit())
            elif type(data).__name__=='tuple':
                print "===============================TUPLE!================================"
                p= subprocess.Popen(data[0].rsplit(),stdout=open(data[1],'w'))
            p.wait()
            self.q.task_done()
        print "Popen"

#####################################################Creating the pool of threads #######################################################################
cpu= multiprocessing.cpu_count()                                                 # Number of CPU's
print cpu
for i in range(cpu):                                                             # starting Handlers
     t= Fchk(queue)
     t.setDaemon(True)
     t.start()

##################################INPUT FILENAMES###########################
fchk=raw_input("Specify the name of the fchk file-> ")
log=raw_input("Specify the name of the log file-> ")
esn=raw_input("Specify the excited state number -> ")
eps=float(raw_input("Specify the accuracy of the (X+Y) term -> "))
#######################################################################Final Dictionary##################################################################
Spectra={} #Dictionary, which has the following structure: {Distance:{Excited State Number:(Energy,Osc.Str.,[(homo,lumo,coeff),(...)])}}
Orbitals=set()
Lambda=0
#####################################################MAKING DIRECTORIES AND SORTING FILES INTO THEM######################################################
Spectra=exc.Exc(log)                                                        # Modifying the general dictionary
################################################################################ FILTER  ################################################################
dlt=[]
print "BEFORE", Spectra[esn][2], len(Spectra[esn][2])
#     Filtering X and Y        
Pairs=[x[:-1] for x in Spectra[esn][2]]
for i,x in enumerate(Spectra[esn][2]):
    if x[:-1] in Pairs[i+1:]:
        ip= Pairs[i+1:].index(x[:-1])+i+1
        print ip, type(Spectra[esn][2][i][2])
        Spectra[esn][2][i]=x[:-1][0],x[:-1][1],str(float(Spectra[esn][2][ip][2]) + float(Spectra[esn][2][i][2]))
        dlt.append(ip)

dlt.sort()
print dlt
while dlt !=[]:
    indx=dlt.pop()
    del Spectra[esn][2][indx]
print "AFTER", Spectra[esn][2],len(Spectra[esn][2])

#########################################################################################################################################################
Transition=zeros(len(Spectra[esn][2]))
index=[]

#   GRABBING ORBITALS FOR CUBEGEN   #
for i,x in enumerate(Spectra[esn][2]):
    if fabs(float(x[2]))<eps:
        continue
    Orbitals.add(x[0])
    Orbitals.add(x[1])
    index.append(i)
print "ORBITALS------>",Orbitals
print "Index----->",index

#   Grabbing existing orbitals   #
exist=glob.glob('???')
#        CALL cubegen        #
while len(Orbitals)!=0:                                                # Cycle through number orbitals
    orb= Orbitals.pop()                                                          # Pop the orbital from dictionary
    if orb in exist:
        print " I will skip orbital ",orb 
        continue
    ipt="/software/g09-A.02/g09/cubegen 0 MO="+ orb+ " "+ fchk+ " "+ orb+" -4 h"  # Creating Cubegen files- for MO
    queue.put(ipt)
queue.join()

Overlap=zeros(len(index))
Kappa= zeros(len(index))
t= overlap.Overlap("","")

for i,x in enumerate(index):
     Trans= Spectra[esn][2][x]
     Kappa[i]= Trans[2]
     t.renew(Trans[0],Trans[1])
     Overlap[i]= t.Calc_Overlap()
Lambda=dot(Overlap,Kappa**2)/sum(Kappa**2)
print Kappa
print Overlap
print Lambda
with open('Lambda','a') as f:
   f.write("File-> "+ fchk + " Excitation-> "+ esn+ " Overlap-> "+repr(Overlap)+" X+Y-> "+ repr(Kappa)+ " Lambda-> "+repr(Lambda)+ '\n')


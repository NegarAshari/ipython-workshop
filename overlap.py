#!/software/python-2.7.2-gnu/bin/python
import os
import re
import sys
import glob
import math
import commands
import linecache
import threading
import subprocess
import multiprocessing 
import time
import signal
import Queue
import shutil
import numpy
from numpy import *
from numpy.linalg import *


class Overlap:
    def __init__(self,orb1,orb2):

           self.Orbitals =[]
           if (orb1!="") and (orb2!=""):
               self.orb1=orb1
               self.orb2=orb2
               Origin=empty((3))
               f=open(self.orb1,'r')
               self.data1= f.readlines()
               f.close()
               f=open(self.orb2,'r')
               self.data2= f.readlines()
               f.close()
               print "Files have been read!!"

    def renew(self,orb1,orb2):
           self.orb1=orb1
           self.orb2=orb2
           Origin=empty((3))
           f=open(self.orb1,'r')
           self.data1= f.readlines()
           f.close()
           f=open(self.orb2,'r')
           self.data2= f.readlines()
           f.close()
           print "Files have been read!!"

    def File_Decomposer(self, data):
            self.data= data
            for i,x in enumerate(self.data):
                if i<=1:
                    continue     #Comments
                if i==2:
                    line=x.rsplit()
                    self.NAtoms= abs(int(line[0]))
                    Origin=asarray([float(xx) for xx in line[1:]])
                    print self.NAtoms, Origin, type(Origin)
                if i==3:
                   line=x.rsplit()
                   self.Nx=int(line[0])
                   dx= asarray(line[1:])
                if i==4:
                   line=x.rsplit()
                   self.Ny=int(line[0])
                   dy= asarray(line[1:])
                if i==5:
                   line=x.rsplit()
                   self.Nz=int(line[0])
                   dz= asarray(line[1:])
                   break
            print self.Nx, self.Ny, self.Nz
            self.dv=det(array((dx,dy,dz)))
            print dx, dy, dz, self.dv

            self.data= self.data[self.NAtoms+7:] #There is only orbital values in self.data now
#           print "SELF",self.data
            Orbital= empty((self.Nx,self.Ny,self.Nz))
            ix,iy,iz= 0,0,0        #Counters to check the data

            for cnt, dt in enumerate(self.data):
                current=asarray([float(v) for v in dt.rsplit()])
#               print cnt, current
                for ic,xc in enumerate(current):
                    if iz< self.Nz:
                        Orbital[ix][iy][iz]= xc
                        iz+=1 
                    elif (iy+1)< self.Ny:   
                        iy+=1
                        iz= 0
#                       print ix,iy,iz
                        Orbital[ix][iy][iz]= xc
                        iz+=1
                    elif (ix+1)< self.Nx:
                         ix+=1
                         iy=0
                         iz=0        
#                        print ix,iy,iz
                         Orbital[ix][iy][iz]= xc
                         iz+=1
            print "IX,IY,IZ",ix,iy,iz
            return Orbital
    def Calc_Overlap(self):
            if self.orb1 not in self.Orbitals:
                Orbital1=self.File_Decomposer(self.data1)
                self.Orbitals.append(self.orb1)
                save(self.orb1,Orbital1)
            else:
                Orbital1=load(self.orb1+'.npy')
                print "Orbital "+self.orb1+" has been loaded!! "

            if self.orb2 not in self.Orbitals:
                Orbital2=self.File_Decomposer(self.data2)
                self.Orbitals.append(self.orb2)
                save(self.orb2,Orbital2)
            else:
                Orbital2=load(self.orb2+'.npy')
                print "Orbital "+self.orb2+" has been loaded!! "

            self.OverlapValue= sum(fabs(Orbital1*Orbital2))*self.dv
            with open('Overlap','a') as f:
                f.write(repr(self.orb1)+' '+repr(self.orb2)+' '+repr(self.OverlapValue)+'\n')
            return self.OverlapValue
    def __del__(self):
        print "Overlap Object has finished its work!"
#       with open('Overlap','a') as f:
#           f.write(repr(self.orb1)+' '+repr(self.orb2)+' '+repr(self.OverlapValue)+'\n')
#       print "Overlap Value is", self.OverlapValue


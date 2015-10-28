import os
import re
import sys
import glob
import math
import commands
import linecache

##############################Excitation Energies##########################
def Exc(log_file):
    Excited_States={}
    Orbitals_Coeff=[] # Contains the list of tuples of the form [(homo,lumo,coefficient),(...)]
    es=commands.getoutput('grep -n Excited ' + log_file).rsplit()
    number_es= es.count('State')                 # Number of Excited States
    n1= int(es[es.index('eV',0,len(es))-6][:-1]) #Defining the line number, containing first excited state
#   Excited_States= Excited_States.fromkeys(range(1,number_es+1))
    line=linecache.getline(log_file,n1)          # Reading line number n1 from the file log_file
    while "SavETr:" not in line:                 # Until reaching end of region that contains information about excitations
       if "->" in line:                          # Orbital Section
           nline= line.replace('->','').rsplit()
           Orbitals_Coeff.append(tuple(nline))
       elif "<-" in line:
           nline= line.replace('<-','').rsplit()
           Orbitals_Coeff.append(tuple(nline))
       elif len(line.strip())==0:
           Excited_States[Excitation_Number]=Excitation_Energy,Oscillat_Strength,Orbitals_Coeff # Modifying Excited_States dictionary
           Excitation_Number= ''                                                                # Excitation Number
           Excitation_Energy= ''                                                                # Excitation Energy
           Oscillat_Strength= ''                                                                # Oscillator strength
           Orbitals_Coeff=[]
           line= linecache.getline(log_file, n1)
       elif "This state for optimization and/or second-order correction." in line:
           n1+=1
       elif "Excited" in line:
           nline= line.rsplit()
           Excitation_Number= nline[2][:-1]           #Excitation Number
#          print 'Excited State', Excitation_Number
#          print nline
           Excitation_Energy= nline[4]                # Excitation Energy
           Oscillat_Strength= nline[8][2:]            # Oscillator strength
       n1+= 1
       line=linecache.getline(log_file,n1)

    Excited_States[Excitation_Number]=Excitation_Energy,Oscillat_Strength,Orbitals_Coeff # Modifying Excited_States dictionary
    return Excited_States

####################################### Modifying vmd files ####################################################
def Change_Cube_Vmd(source, path_cube, file_cube, path):
  with open(source,'r+') as f:
     data= f.readlines()
  lines= [i for i,x in enumerate(data) if 'cube' in x]                            # Taking two strings from vmd file using grep 
  line1= data[lines[0]].rsplit()                                                  # Creating list
  line2= data[lines[1]].rsplit()                                                  # Creating list
  line1[2]= path_cube+ '/'+ file_cube                                             # Modifying path
  line2[3]= file_cube                                                             # Modifying path
  data[lines[0]]= ' '.join(line1)+ '\n'
  data[lines[1]]= ' '.join(line2)+ '\n'
  with open(path, 'w') as f:
     f.writelines(data)

######################################FormChk Excited Density###################################################
def Density_Ci(source, path):
  with open(source,'r+') as f:
     data= f.readlines()
  lines= [i for i,x in enumerate(data) if 'Total SCF Density' in x]
  lines+= [i for i,x in enumerate(data) if 'Total CI Rho(1) Density' in x]        
  line= data[lines[1]]
  data[lines[1]]= data[lines[0]]                 
  data[lines[0]]= line
  with open(path, 'w') as f:
     f.writelines(data)



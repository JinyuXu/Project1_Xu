# -*- coding: utf-8 -*-

"""Main module."""
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

def ld(pos=0,velocity=0,timestep=0.1,temp=300,wallsize=5,totaltime=1000,gamma=0.1):
    # define constant
    m=1
    eps=1
    timepass=0
    indexnum=0
    index=[]

    # integrate
    while timepass < totaltime :
        indexnum +=1
        index.append([indexnum,timepass,pos,velocity])
        a=-gamma*velocity/m + ss.norm.var(loc=0,scale=2*temp*gamma*1*timestep)
        velocity = a*timestep
        pos= (2*velocity-a*timestep)/2*timestep
        timepass+=timestep
        
    
    return pos, velocity, index


        


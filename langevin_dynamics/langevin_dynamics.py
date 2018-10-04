# -*- coding: utf-8 -*-

"""Main module."""
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import argparse


def getinput():
    input = argparse.ArgumentParser()
    input.add_argument('--initial_position', type = float, default = 0, help = 'Initial position of the particle, default = 0' )
    input.add_argument('--initial_velocity', type = float, default = 0, help = 'Initial velocity of the particle, default = 0' )
    input.add_argument('--temperature', type = float, default = 300, help = 'Temperature of the molecule, default = 300' )
    input.add_argument('--damping_coefficient', type = float, default = 0.1, help = 'Damping Coefficient of the molecule, default = 0.1' )
    input.add_argument('--time_step', type = float, default = 0.2, help = 'Time interval of the simulation, default = 0.01' )
    input.add_argument('--wall_size', type = float, default = 5, help = 'Wall size of the simulation, default = 5' )
    input.add_argument('--total_time', type = float, default = 1000, help = 'Total time of the simulation, default = 1000' )
    inp = input.parse_args()
    return inp

def acceleration(gamma=0.1,velocity=0,temperature=300,timestep=0.1,mass=1):
    sigma=np.sqrt(2*temperature*gamma*1*timestep)
    return (-gamma*velocity/mass + np.random.normal(0,sigma))*timestep

def checkwall(position, wallsize):
    if position >= wallsize or position<=0:
        return True
    else:
        return False
    

def lgmotion(velocity,timestep):
    return velocity*timestep

def integrate(position=0,velocity=0,temperature=300,gamma=0.1,timestep=0.1,wallsize=5,totaltime=1000,mass=1):
    
    timepass=0
    indexnum=0
    index=[]
    
    while timepass < totaltime :
        indexnum +=1
        index.append([indexnum,timepass,position,velocity])
        timepass+=timestep
        velocity += acceleration(gamma, velocity, temperature, timestep)
        position += lgmotion(velocity, timestep)
        if checkwall(position,wallsize):
            if position >= wallsize:
                position = wallsize
                index.append([indexnum+1,timepass,position,velocity])
            else:
                position= 0
                index.append([indexnum+1,timepass,position,velocity])
            break
        
    return timepass,index


def filecreation(index):
    indexf=np.array(index)
    timef=indexf[:,1]
    positionf=indexf[:,2]
    velocityf=indexf[:,3]
    with open('Langevin_Motion.txt','w+') as file:
        file.write('Index Time Position Velocity \n')
        for i in range(len(timef)):
            file.write('{}  {:.3f}  {:.5f}  {:.5f} \n'.format(i,timef[i],positionf[i],velocityf[i]))

def histogram(arr):
    plt.figure(0)
    plt.hist(arr,bins=20)
    plt.title('100 runs of Langevin Motion')
    plt.xlabel('Time passed')
    plt.ylabel('Number of runs')
    plt.savefig('histogram.png')

def trajectory(x,y):
    plt.figure(1)
    plt.plot(x,y)
    plt.title('Position vs Time')
    plt.xlabel('Time passed')
    plt.ylabel('Position')
    plt.savefig('trajectory.png')


def main():
    #get input for simulation
    inp=getinput()
    
    #run for 100 times, collecting all the relavant data

    t_arr=[] #time
    for i in range(100):
        t,idx=integrate(position=inp.initial_position,velocity=inp.initial_velocity,temperature=inp.temperature,gamma=inp.damping_coefficient,timestep=inp.time_step,wallsize=inp.wall_size,totaltime=inp.total_time,mass=1)
        t_arr.append(t)
    
    
    #plot the histogram of 100 runs
    histogram(t_arr)

    #plot the position vs time plot of the last run
    trjdata=np.array(idx)
    xdata=trjdata[:,1]
    ydata=trjdata[:,2]
    trajectory(xdata,ydata)

    #write the index in to a txt file of the first run
    filecreation(idx)

if __name__ == '__main__':
    main()

    


    
    







        


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `langevin_dynamics` package."""

import numpy as np
import unittest
import pytest
import scipy.stats as ss
import random
import os


from langevin_dynamics import langevin_dynamics as LD

class Test(unittest.TestCase):

    def test_acceleration(self):
        #unit test for acceleration
        gamma = 0.7
        velocity = 10
        temperature = 300
        randomF_arr = []
        #generate random acceleration
        for i in range(3200):
            randomF_arr.append(LD.acceleration(gamma,velocity,temperature,0.1,1))
        _ , p = ss.shapiro(randomF_arr)
        mean = np.mean(randomF_arr)
        var = np.var(randomF_arr)
        theta = 2*temperature*gamma
        #perform shapiro test to see if the accelerations follows random distribution
        self.assertLessEqual(0.05,p)
        self.assertTrue(mean<= 7.5 or mean >= 6.5)
        self.assertTrue(var>=theta*(.95) or var<=theta*(1.05))
    
    def test_lgmotion(self):
        #unit test for motion simulation
        result=LD.lgmotion(3,5)
        self.assertEquals(result,15)

    def test_checkwall(self):
        #unit test for checkwall function
        randomposition = random.random()*5+0.01
        randomposition = random.random()*(-5)+0.01
        self.assertFalse(LD.checkwall(randomposition,5))
        self.assertFalse(LD.checkwall(randomposition,5))
        self.assertTrue(LD.checkwall(-5,5))
        self.assertTrue(LD.checkwall(5,5))
     

    def test_integrate(self):
        #unit test for integration
        time,indx = LD.integrate()
        self.assertEquals(indx[0][3],0)
        self.assertEquals(indx[0][2],0)
        self.assertEquals(indx[0][0],1)

    def test_filecreation(self):
        #unit test for file created
        testindex=np.zeros((7,4))
        LD.filecreation(testindex)
        with open('Langevin_Motion.txt') as testfile:
            line1 = testfile.readline()
            self.assertEquals(line1,'Index Time Position Velocity \n')

    def test_getinput(self):
        #unit test for getting input and its default input
        input1 = LD.getinput()
        self.assertEquals(input1.initial_position,0)
        self.assertEquals(input1.initial_velocity,0)
        self.assertEquals(input1.temperature,300)
        self.assertEquals(input1.damping_coefficient,0.1)
        self.assertEquals(input1.time_step,0.01)
        self.assertEquals(input1.wall_size,5)
        self.assertEquals(input1.total_time,1000)

    def test_histogram(self):
        #unit test for histogram graph
        timepass = [0,1,2,3,4,5,6,7]
        LD.histogram(timepass)
        self.assertTrue(os.path.isfile('histogram.png'))

    
    def test_trajectory(self):
        #unit test for trajectory graph
        time = np.linspace(0,7,20)
        position = np.linspace(0,7,20)
        LD.trajectory(time,position)
        self.assertTrue(os.path.isfile('trajectory.png'))        

    def test_main(self):
        LD.main()
        self.assertTrue(os.path.isfile('trajectory.png'))
        self.assertTrue(os.path.isfile('histogram.png'))
        with open('Langevin_Motion.txt') as testfile:
            line1 = testfile.readline()
            self.assertEquals(line1,'Index Time Position Velocity \n')
        


'''
@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
'''
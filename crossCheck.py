'''
Description:
   An attempt to make an interface to the emdCompCylProj.py code from Cari Cesarotti.
   The code generates a set of events, each containing a number "partricles" (sets of pt, eta and phi numbers).

Authour: 
   William Fawcett, 
   University of Cambridge
   May 2020
'''



import numpy as np
import math
import os

from ExampleGenerator.Particle import Particle
from ExampleGenerator.Event import Event 


def normalize(array):
   norm = np.linalg.norm(array)
   return array/norm



def generate_particles(n_particles, PtScale=100, etaLimit=2.7):
   '''
   Randomly generate a list of Particle objects in a very quick and dirty way.
   Lets pretend this returns pTs in units of GeV.
   Returns a python list of Particle objects. 
   Each Particle object contains a  randomly generated pT, eta, and phi value. 
   The pT values are generated from a falling exponential, the phi values from a flat distribution from [-pi,pi] and the eta values from a normal distribution constrained by |eta| < etaLimit.
   '''

   #phis = np.random.uniform(low=0, high=2*math.pi, size=n_particles)
   phis = np.random.uniform(low=-math.pi, high=math.pi, size=n_particles-1)
   pts = np.random.exponential(size=n_particles-1, scale=PtScale)

   # not actually that bad of an approximation, although pT should be correlated but whatever
   etas = []
   while( len(etas) < n_particles-1):
      eta = np.random.normal(loc=0.0, scale=1.5)
      if abs(eta) < etaLimit:
         etas.append(eta)
      if len(etas) == n_particles-1:
         break

   particles = []
   NegEtMiss = Particle(0,0,0)
   for i in range(n_particles-1):
      temp = Particle(pts[i], etas[i], phis[i])
      particles.append(temp)
      NegEtMiss += temp

   # Make sure vector sum of pT = 0
   print('NegEtMiss', NegEtMiss)
   EtMiss = Particle(NegEtMiss.pt, 0, NegEtMiss.phi + math.pi)
   print('MET', EtMiss)
   particles.append(EtMiss)

   ptsum = Particle(0,0,0)
   for part in particles:
      ptsum += part
   print('result', ptsum)


   
   return particles



def main():

   output_directory = 'data' # a place to store the output files 

   # An example: generate a single event with 4 particles
   particles = generate_particles(4)
   event = Event(particles)
   # Print out what I think are the ring coordinates 
   pts, phis = event.get_ring_coordinates()
   print(pts)
   print(phis)

   # Now consider a bunch of events, each event has a different number of particles
   n_particles_in_event = [4,5,2,6,9,8]
   events = []
   ringSample = []
   ringPtSample = []
   for n_particles in n_particles_in_event:
      event = Event( generate_particles(n_particles) ) 
      pts, phis = event.get_ring_coordinates()
      ringSample.append(phis)
      ringPtSample.append(pts)
   # Format in the same way as in emdCompCylProj
   ringSample = np.array(ringSample)
   ringPtSample = np.array(ringPtSample)


   # Copy the rest of the code from emdCompCylProj
   nList = n_particles_in_event # hope this is the right thing to do
   from EventIsotropy.cylGen import ringGen, ringGenShift
   from EventIsotropy.emdVar import _cdist_phicos, emd_Calc

   if not os.path.exists(output_directory):
       os.makedirs(output_directory)

   for i in range(5):
       ringPoints1 = ringSample[i]
       ringPT1 = ringPtSample[i]
       print('considering the following:')
       print('ring points', ringPoints1)
       print('ringPT1:', ringPT1)
       print('')
       for j in range(5):
           emdSpec=[]
           # SET THE SECOND EVENT WITH j 
           ringPT2 = ringPtSample[j]
           for num in range(1000):
               ringPoints2 = ringGenShift(nList[j]) # The shift just randomly orients the ring, doesn't change particle spacing
               M = _cdist_phicos(ringPoints1,ringPoints2)  # M is distance in phi according to 1 - cos phi metric
               emdval = emd_Calc(ringPT1, ringPT2, M) # so you pass energy weight of event 1, energy weight of event 2, and the distance matrix
               emdSpec.append(emdval)
           f= open(f"{output_directory}/emdRingtoRing_{i}_{j}.dat","w+")
           for emdVal in emdSpec:
               f.write(str(emdVal)+ ' ')
           f.close()


if __name__ == "__main__":
   main()

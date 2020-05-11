import math
from lorentz import FourMomentum

class Particle():
   '''
   Store information for one particle.
   '''

   def __init__(self, pt, eta, phi, mass=0):
      # Expect phi to be [-pi, pi]
      self.pt = pt
      self.eta = eta 
      self.phi = phi
      self.px = self.pt * math.cos(self.phi)
      self.py = self.pt * math.sin(self.phi)
      self.pz = self.pt * math.sinh(self.eta)
      self.p = math.sqrt(self.px**2 + self.py**2 + self.pz**2)
      self.mass = mass 
      if mass==0:
         self.e = self.p
      else:
         self.e = math.sqrt(self.p**2 + self.mass**2)
      self.momentum = FourMomentum( self.e, self.px, self.py, self.pz)

   def __repr__(self):
      return f'({self.pt}, {self.eta}, {self.phi})'

   def __add__(self, other):

      new_momentum = self.momentum + other.momentum
      return Particle(new_momentum.pt, new_momentum.eta, new_momentum.phi)


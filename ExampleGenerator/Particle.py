class Particle():
   '''
   Store information for one particle.
   '''
   def __init__(self, pt, eta, phi):
      self.pt = pt
      self.eta = eta 
      self.phi = phi
   def __repr__(self):
      return f'({self.pt}, {self.eta}, {self.phi})'

class Event():
   '''
   Store all of the particles in an event.
   '''
   def __init__(self, particle_list):
      self.particles = particle_list
      self.n_particles = len(self.particles)

   def get_ring_coordinates(self):
      '''
      Return the ring coordinates for this event as two numpy arrays:
      pTs and phis (in that order). 
      '''
      pts, phis = [], [] 
      for particle in self.particles: 
         phis.append( particle.phi )
         pts.append( particle.pt )
      return np.array(pts), np.array(phis)

   def get_cylinder_coordinates(self):
      '''
      Return the cylinder coordinates for this event as three numpy arrays:
      pTs, phis and etas (in that order). 
      '''
      pts, phis = self.get_ring_coordinates()
      etas = [x.eta for x in self.particles]
      return pts, phis, np.array(etas)



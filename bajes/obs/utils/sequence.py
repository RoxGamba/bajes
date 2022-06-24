import imp
from json import load
import numpy as np
from scipy.interpolate import interp1d
from ... import __path__ 

class Sequence(object):

    def __init__(self, name='SLy') -> None:
        self.name = name
        self.path = __path__[0] + '/obs/utils/eos/sequences/'+name+'_sequence.txt'

        self.data = self._load_sequence()
        self.data = self._cut_sequence()
        self.interpolators    = self._interpolate_sequence()
        pass

    def _load_sequence(self):
        p   =  np.genfromtxt(self.path, names=True)
        p_n = {key: p[key] for key in p.dtype.names}
        return p_n
    
    def _cut_sequence(self):
        # find stable sequence
        dat  = self.data
        M    = dat['M']
        i_MM = np.argmax(M)
        self.max_mass = M[i_MM]
        self.min_maxx = min(M)
        return {key: dat[key][:i_MM] for key in dat.keys()}
        
    def _interpolate_sequence(self):
        """
        Interpolate R(M) and Lambda_2(M)
        """
        dat = self.data
        fL = interp1d(dat['M'], dat['lam'])
        fR = interp1d(dat['M'], dat['R'])
        return fL, fR

    def lambda_of_m(self, m=1.35):
        return self.interpolators[0](m)

    def R_of_m(self, m=1.35):
        return self.interpolators[1](m)

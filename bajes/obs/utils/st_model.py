import numpy as np
from scipy.interpolate import RectBivariateSpline
from ... import __path__ 

def reshape(x,y,z, Nx, Ny):
    """
    Reshape to build the interpolator
    """
    x_1d = np.unique(x)
    y_1d = np.unique(y)
    z_2d = z.reshape(Nx, Ny)
    return x_1d, y_1d, z_2d

class ST_model(object):

    def __init__(self, name='SLy4') -> None:
        self.name = name
        self.path = __path__[0] + '/obs/utils/eos/st_models/'+name+'.dat'

        self._load_model()
        self.interpolator = self._interpolate_model_2d()
        pass

    def _load_model(self) -> None:
        """
        rho:0 R:1 M:2 chi[0]:3 abs(alpha_A):4 beta:5 alpha:6 log(alpha):7 
        """
        p   =  np.genfromtxt(self.path)
        self.M    = p[:,2]
        self.qa   = p[:,4]
        self.log_alpha = p[:,7]
        self.R    = p[:,1]
        self.max_mass   = max(self.M)        ;self.min_mass   = min(self.M)
        self.max_logalp = max(self.log_alpha);self.max_logalp = min(self.log_alpha)
        pass
        
    def _interpolate_model_2d(self):
        """
        Interpolate q(M, log_alpha) and Lambda_2(M)
        """
        N_M      = len(np.unique(self.M))
        N_alpha  = len(np.unique(self.log_alpha))
        x,y,z    = reshape(self.M, self.log_alpha, self.qa, N_M, N_alpha)
        f_q      = RectBivariateSpline(x, y, z)
        return f_q

    def q_of_m_logalpha(self, m=1.35, log_alpha=-3.):
        return self.interpolators(m, log_alpha)

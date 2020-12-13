import sys
sys.path.append('../src/')
sys.path.append('../utils/')
from qbmm_manager import *
from stats_util import *
import numpy.polynomial.hermite as hermite_poly
import pytest

def test_wheeler():
    """
    This function tests QBMM Wheeler inversion by comparing
    against numpy's Gauss-Hermite for given mu and sigma
    """
    num_nodes = 4
    config = {}
    config['qbmm'] = {}
    config['qbmm']['governing_dynamics']   = '4*x - 2*x**2'
    config['qbmm']['num_internal_coords']  = 1
    config['qbmm']['num_quadrature_nodes'] = num_nodes
    config['qbmm']['method']       = 'qmom'
    ###
    ### QBMM
    qbmm_mgr = qbmm_manager( config )
    
    ###
    ### Tests
    
    # Anticipate success
    tol = 1.0e-10  # Round-off error in moments computation
    success = True
    
    # Test 1
    mu    = 5.0
    sigma = 1.0
    ###
    ### Reference solution
    sqrt_pi   = np.sqrt( np.pi )
    sqrt_two  = np.sqrt( 2.0 )
    h_abs, h_wts = hermite_poly.hermgauss( num_nodes )
    g_abs = sqrt_two * sigma * h_abs + mu
    g_wts = h_wts / sqrt_pi
    
    ###
    ### QBMM
    moments = raw_gaussian_moments_univar( qbmm_mgr.num_moments, mu, sigma )
    my_abs, my_wts = qbmm_mgr.moment_invert( moments )

    ###
    ### Errors & Report
    diff_abs = my_abs - g_abs
    diff_wts = my_wts - g_wts

    error_abs = np.linalg.norm( my_abs - g_abs )
    error_wts = np.linalg.norm( my_wts - g_wts )

    assert error_abs < tol
    assert error_wts < tol

if __name__ == "__main__":

    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from pytest import main

        main([__file__])

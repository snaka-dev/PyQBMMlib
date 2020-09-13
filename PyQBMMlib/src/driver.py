from qbmm_manager import *
import scipy.special as sc

import collections

try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections

def rawmoments_bivar_uncorr_gaussian(mu1,mu2,sig1,sig2,i,j):
    return (1./math.pi) * 2**((-4.+i+j)/2.) * \
        math.exp( -(mu1**2./(2. * sig1**2))-(mu2**2./(2 * sig2**2.)) ) * \
        sig1**(-1.+i) * sig2**(-1+j) * \
        ( \
          -math.sqrt(2.) * \
          (-1.+(-1.)**i) * \
          mu1 * \
          sc.gamma(1.+i/2.) * \
          sc.hyp1f1(1+i/2.,3./2.,mu1**2./(2. * sig1**2.))  \
          + (1.+(-1.)**i) * \
          sig1 * \
          sc.gamma((1.+i)/2.)  * \
          sc.hyp1f1((1.+i)/2.,1./2.,mu1**2./(2. * sig1**2.))
        ) * ( \
        -math.sqrt(2.) * \
        (-1+(-1)**j) * \
        mu2 * \
        sc.gamma(1.+j/2.) * \
        sc.hyp1f1(1.+j/2.,3./2.,mu2**2./(2. * sig2**2.)) + \
        (1.+(-1)**j) * \
        sig2 * \
        sc.gamma((1.+j)/2.) * \
        sc.hyp1f1((1.+j)/2.,1./2.,mu2**2./(2. * sig2**2.)) \
        )

def power(my_list,exp):
    print(my_list)
    print(exp)
    return [ math.pow(x,exp) for x in my_list ]

def quadrature(weights,abscissa,index):
    if isinstance(index,collectionsAbc.Iterable):
        if len(index) == 2:
            return sum(weights[:] * \
                    abscissa[0][:]**index[0] * \
                    abscissa[1][:]**index[1]   
                    )
        if len(index) == 3:
            return sum(weights[:] * \
                    abscissa[0][:]**index[0] * \
                    abscissa[1][:]**index[1] * \
                    abscissa[2][:]**index[2]   
                    )
    else:
        return sum(weights[:]*abscissa[:]**index)



if __name__ == '__main__':
    
    config = {}
    config['governing_dynamics']   = ' dx + x = 1'
    config['num_internal_coords']  = 2
    config['num_quadrature_nodes'] = 2
    config['method']       = 'chyqmom'
    config['adaptive']     = False
    config['max_skewness'] = 30
    config['permutation'] = 12

    # Initialize moment set
    # SHB comment: the line below was incorrect (though not used)! 
    #  the required numebr of moments
    #  depends upon the inversion algorithm. also, it's usually 0:2n+1 where
    #  n is the number of quadrature nodes.
    # moments = np.zeros( config['num_quadrature_nodes'] )


    sig1 = 0.1; sig2 = 0.2
    mu1  = 1; mu2  = 2

    if config['num_internal_coords'] == 1:
        # test from p55 Marchisio + Fox 2013 exercise 3.2
        moments = [ 1., 0., 1., 0., 3., 0., 15., 0. ]

        if config['method'] == 'qmom':
            moments = moments[0:config['num_quadrature_nodes']*2]
        elif config['method'] == 'hyqmom':
            if config['num_quadrature_nodes'] == 2:
                moments = moments[0:3]
            elif config['num_quadrature_nodes'] == 3:
                moments = moments[0:5]
        else:
            print('Cannot find moment set for you sorry!, aborting...')
            exit()
    elif config['num_internal_coords'] == 2:
        # Current test moment setup for CHyQMOM with 2x2 nodes

        # indices = np.array( [ [0,0], [1,0], [0,2], [2,0], [1,1], [0,2] ] )
        # moments = np.zeros(len(indices))
        indices = [ [0,0], [1,0], [0,1], [2,0], [1,1], [0,2] ]
        config['indices'] = indices
        moments = zeros(len(indices))
        for i in range(len(indices)):
            moments[i] = \
                rawmoments_bivar_uncorr_gaussian( \
                        mu1,mu2,sig1,sig2,indices[i][0],indices[i][1] \
                        )

    qbmm_mgr = qbmm_manager( config )

    print('moments in:',moments)
    abscissas, weights = qbmm_mgr.inversion_algorithm( moments, config )

    print('w: ',weights)
    print('x: ',abscissas)

    if config['num_internal_coords']==1:
        testidx = 1.1
    elif config['num_internal_coords']==2:
        testidx = [1.1,1.4]
    elif config['num_internal_coords']==3:
        testidx = [1.1,1.4,3.2]

    quad = quadrature(weights,abscissas,testidx)

    print('Testing quadrature...','Index:',testidx,'Moment:',quad)


    if config['method'] == 'qmom' and config['num_quadrature_nodes']==4:
        print("Expected result (order irrelevant):  \n  \
                w:  0.0459,  0.4541, 0.4541, 0.0459 \n  \
                x: -2.3344, -0.7420, 0.7420, 2.3344")
    if config['method'] == 'hyqmom':
        if config['num_quadrature_nodes']==2:
            print("Expected result (order irrelevant):  \n  \
                    w:  0.5, 0.5 \n  \
                    x:   -1, 1.")
        if config['num_quadrature_nodes']==3:
            print("Expected result (order irrelevant):  \n  \
                    w:  0.166, 0.667, 0.166 \n  \
                    x:   -1.732, 0, 1.732")


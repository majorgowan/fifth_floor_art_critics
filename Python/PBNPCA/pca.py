def pca(data, ncomp):
    # given a list of lists of features, compute the
    # leading principal components (PC)
    #
    # The leading PC is the vector in the direction in
    # which the data varies maximally with length equal
    # to the variance along the axis
    #
    # The next PC is the direction in which the data
    # projected onto the complement of the first PC
    # varies maximally ... and so on
    #
    import numpy as np
    import scipy.linalg as spla
    ndim = len(data[0])
    data_mat = np.array(data)
    # compute mean vector
    meanvec = [np.mean(data[:,i]) for i in xrange(len(data[0,:]))]
    datadiff = np.array([d-meanvec for d in data])
    # scatter matrix
    scat = datadiff.transpose().dot(datadiff)
    # leading eigenvectors and eigenvalues of scatter matrix
    eigvals, eigvecs = spla.eigh(scat,eigvals=(ndim-ncomp,ndim-1))
    variances = [np.sqrt(e/ndim) for e in eigvals]
    # construct pca object
    pcaObj = {
            'ncomp':   ncomp,
            'meanvec': meanvec,
            'eigvecs': eigvecs,
            'eigvals': eigvals,
            'variances': variances
            }
    return pcaObj

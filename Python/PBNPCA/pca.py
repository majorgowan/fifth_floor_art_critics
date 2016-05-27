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
    variances = [e/ndim for e in eigvals]
    stds = [np.sqrt(e/ndim) for e in eigvals]
    # construct pca object
    pcaObj = {
            'ncomp':   ncomp,
            'meanvec': meanvec,
            'eigvecs': eigvecs,
            'eigvals': eigvals,
            'variances': variances,
            'stds': stds
            }
    return pcaObj

def pcaProject(vec, pcaObj):
    # project a given vector onto the eigenvectors
    # stored in pcaObj and return coefficient of each
    # component in projection
    #
    import numpy as np
    # number of components in pcaObj
    meanvec = pcaObj['meanvec']
    # subtract meanvec from vec
    diff = [a - meanvec[i] for i,a in enumerate(vec)]
    # dot product with pca
    comps = np.array(diff).dot(pcaObj['eigvecs'])
    return list(comps)

def pcaTrunc(vec, pcaObj, depth):
    # project a given vector onto the eigenvectors
    # stored in pcaObj and return
    #
    import numpy as np
    if depth > pcaObj['ncomp']:
        raise ValueError('depth cannot exceed ncomp in pcaObj')
    comps = pcaProject(vec, pcaObj)
    eigvecs = pcaObj['eigvecs']
    meanvec = pcaObj['meanvec']
    # reconstruct vector to desired depth
    trunc = np.zeros((len(vec),1))
    for i in xrange(depth):
        trunc = trunc + (comps[-i]*eigvecs[:,-i]).reshape((len(vec),1))
    trunc = trunc + np.array(meanvec).reshape((len(vec),1))
    return trunc.transpose()[0]


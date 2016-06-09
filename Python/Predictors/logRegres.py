# adapted from Harrington, "Machine Learning in Action"
import numpy as np

def sigmoid(inX):
    return 1.0/(1.0+np.exp(-inX))

def standardize(dataMatrix):
    # converts input so that each column has
    # mean 0 and std 1
    # if a column is uniform (std=0), do not
    # change std (obviously)
    #
    # change input matrix in-place, and return
    # object containing list of means and stds
    #
    m,n = np.shape(dataMatrix)
    means = []
    stds = []
    for column in xrange(n):
        x = dataMatrix[:,column]
        meanie = np.mean(x)
        std = np.std(x)
        x -= meanie
        if std > 0:
            x /= std
        means.append(meanie)
        stds.append(std)
    obj = { 'mean': means, \
            'std': stds }
    return obj

def standardize_predict(dataMatrix, obj):
    # shift and rescale data using given means and stds
    # (e.g. for out-of-sample testing)
    #
    m,n = np.shape(dataMatrix)
    nn = len(obj['mean'])
    if (nn != n):
        print('standardization error: incompatible matrix sizes')
        return None
    means = obj['mean']
    stds = obj['std']
    for column in xrange(n):
        x = dataMatrix[:,column]
        x -= means[column]
        if stds[column] != 0:
            x /= stds[column]
    return True

def unstandardize(dataMatrix, obj):
    m,n = np.shape(dataMatrix)
    nn = len(obj['mean'])
    if (nn != n):
        print('standardization error: incompatible matrix sizes')
        return None
    means = obj['mean']
    stds = obj['std']
    for column in xrange(n):
        x = dataMatrix[:,column]
        if stds[column] != 0:
            x *= stds[column]
        x += means[column]
    return True

def gradAscent(dataMatrix, classLabels, alpha=0.01, iterations=20, report=None):
    # n is number of training cases
    # m is number of features
    m,n = np.shape(dataMatrix)
    # initialize weights to unity
    weights = np.ones((1,n))
    # loop until convergence (for now just iterations times)
    for it in xrange(iterations):
        h = sigmoid(weights*dataMatrix.transpose())
        err = classLabels - h
        weights += alpha*err*dataMatrix
        if report:
            if not it % report:
                print(str(it) + '...' + str(weights))
                print('          error: ' + str(np.sum(err)))
    return weights

def predict(dataMatrix, weights):
    # predict probability of class "1" for each sample in dataMatrix
    return sigmoid(weights*dataMatrix.transpose()).tolist()[0]

def confusion(actual, predicted, thresh=0.5):
    tp = np.sum(int(p>=thresh) for i,p in enumerate(predicted) if actual[i]==1)
    fp = np.sum(int(p>=thresh) for i,p in enumerate(predicted) if actual[i]==0)
    tn = np.sum(int(p<thresh) for i,p in enumerate(predicted) if actual[i]==0)
    fn = np.sum(int(p<thresh) for i,p in enumerate(predicted) if actual[i]==1)
    return np.mat([[tn, fp],[fn,tp]])

def ROC(actual, predicted, step=0.1):
    thresh=step
    par = [0.0]
    acc = [None]
    fpr = [0.0]
    tpr = [0.0]
    while thresh < 1.0:
        par.append(thresh)
        conf = confusion(actual, predicted, thresh=thresh)
        tn = conf[0,0]
        fn = conf[1,0]
        tp = conf[1,1]
        fp = conf[0,1]
        fpr.append(float(fp)/(fp+tn))
        tpr.append(float(tp)/(tp+fn))
        acc.append(float(np.trace(conf))/np.sum(conf))
        print('par: ' + str(thresh) + \
                ', tpr: ' + str(float(tp)/(tp+fn)) + \
                ', fpr: ' + str(float(fp)/(fp+tn)))
        thresh += step
    par.append(1.0)
    tpr.append(1.0)
    fpr.append(1.0)
    acc.append(None)
    obj = { 'par': par, \
            'tpr': tpr, \
            'fpr': fpr, \
            'acc': acc }
    return obj

# -------------------------------------------
# fix up the following more efficient methods
def stocGradAscent0(dataMatrix, classLabels, alpha=0.01, niter=10):
    m,n = np.shape(dataMatrix)
    # initialize weights
    weights = np.ones((n,1))
    for it in xrange(niter):
        # loop over training examples
        for i in range(m):
            # compute probability of class "1"
            # given current weights
            # (probability of class "0" is 1-p("1") )
            h = sigmoid(np.sum(dataMatrix[i]*weights))
            # error is difference between true class
            # and predicted class
            error = classLabels[i] - h
            # adjust weights in direction opposite
            # the gradient of the (log) error
            weights = weights + alpha * error * dataMatrix[i].transpose()
            # supposed to converge towards the optimum weights
        print(str(it) + '. . . ' + str(weights.transpose()))
    return np.mat(weights).transpose()

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = np.shape(dataMatrix)
    weights = np.ones((n,1))
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4.0/(1.0+j+i) + 0.01
            randIndex = int(np.random.uniform(0,len(dataIndex)))
            h = sigmoid(np.sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + \
                        alpha * error * dataMatrix[randIndex].transpose()
            del(dataIndex[randIndex])
    return np.mat(weights).transpose()

def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights = wei.getA()
    dataMat,labelMat=loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

def classifyVector(inX, weights, thresh=0.5):
    prob = sigmoid(sum(inX*weights))
    if prob > thresh:
        return 1.0
    else:
        return 0.0


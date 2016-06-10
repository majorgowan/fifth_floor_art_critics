def focusDetect(hsvlist, size=(100,100)):
    # check image for brightness differences
    # between adjacent pixels (horizontally
    # and vertically)
    #
    # the higher the total the sharper the
    # focus
    #
    import numpy as np
    val = np.array([v for (h,s,v) in hsvlist])
    val.shape = size
    c = 0
    for row in val:
        for i,v in enumerate(row[:-1]):
            c += abs(v - row[i+1])
    for col in val.transpose():
        for i,v in enumerate(col[:-1]):
            c += abs(v - col[i+1])
    return c

def replaceChannel(tuples, newvec, channel):
    for itup, tup in enumerate(tuples):
        ll = list(tup)
        ll[channel] = newvec[itup]
        tuples[itup] = tuple(ll)

def defocusValue(hsvlist, size=(100,100), window=1):
    # apply a boxcar smoothing to the
    # value (brightness) channel
    #
    import numpy as np
    import copy as cp
    val = np.array([v for (h,s,v) in hsvlist])
    newlist = cp.copy(hsvlist)
    val.shape = size
    newval = []
    for i in xrange(size[0]):
        top = max(0,i-window)
        bot = min(size[0],i+window+1)
        for j in xrange(size[1]):
            left = max(0,j-window)
            right = min(size[1],j+window+1)
            newval.append(np.mean(val[top:bot,left:right]))
    replaceChannel(newlist, newval, 2)
    return newlist







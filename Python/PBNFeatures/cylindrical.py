def jpg_to_hsv(img):
    # convert a jpg image (in form of a PIL.Image object) to a list
    # of three lists of HSV (hue-saturation-value) data
    #
    import paletteTools as pt
    import colorsys
    rgblist = list(img.getdata())
    rgblist = [pt.normalizeRGB(c, addAlpha=False) for c in rgblist]
    hsvlist = [colorsys.rgb_to_hsv(*rgb) for rgb in rgblist]
    return hsvlist

def hsv_to_rgb(hsvlist):
    import colorsys
    rgblist = [colorsys.hsv_to_rgb(*hsv) for hsv in hsvlist]
    rgblist = [(int(256*r),int(256*g),int(256*b)) for (r,g,b) in rgblist]
    return rgblist

def hsv_stats(hsvlist, hue_bins=8):
    # given a list of hsv pixel values, return:
    #  * mean and std of saturation (radial) values,
    #  * mean and std of brightness/value (axial) values,
    #  * the number of pixels in each hue_bin
    #    ordered from most to least frequent
    #
    import numpy as np
    import readPBNData.description as rd
    satvals = [hsv[1] for hsv in hsvlist]
    valvals = [hsv[2] for hsv in hsvlist]
    huevals = [hsv[0] for hsv in hsvlist]
    sat_mean = np.mean(satvals)
    sat_std = np.std(satvals)
    val_mean = np.mean(valvals)
    val_std = np.std(valvals)
    binsize = 1.0/hue_bins
    binavg = len(hsvlist)/hue_bins
    hue_bins = rd.table( [int(h/binsize) for h in huevals] )
    hsv_statsobj = {
            'sat_mean': sat_mean,
            'sat_std': sat_std,
            'val_mean': val_mean,
            'val_std': val_std,
            'hue_bins': hue_bins
            }
    return hsv_statsobj

def completeSortHues(hue_bins, nhues=16):
    # make a copy and sort it
    hb = sorted(hue_bins[:])
    # insert colour counts of 0 for missing entries
    for n in xrange(nhues):
        if n not in [a[0] for a in hb]:
            hb.insert(n,(0, n))
    return hb

def plotHueDistribution(hue_bins, nhues=16):
    import colorsys
    import paletteTools as pt
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = plt.axes()
    # construct palette from central colour
    # in each hue_bin
    hue = [(i+0.5)/nhues for (i,n) in hue_bins]
    sat = len(hue)*[1.0]
    val = len(hue)*[1.0]
    # convert to rgba
    rgblist = [colorsys.hsv_to_rgb(*hsv) for hsv in zip(hue,sat,val)]
    # add trivial alpha channel
    rgba = [(r,g,b,1.0) for (r,g,b) in rgblist]
    pos = [a[0] for a in hue_bins]
    heights = [a[1] for a in hue_bins]
    plt.title('Distribution of hues in painting')
    plt.xlabel('hue bin')
    plt.ylabel('pixel count')
    plt.bar(pos, heights, width=0.8, color=rgba)

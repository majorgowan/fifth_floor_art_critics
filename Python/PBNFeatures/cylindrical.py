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


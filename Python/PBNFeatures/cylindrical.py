def jpg_to_hsv(img):
    # convert a jpg image (in form of a PIL.Image object) to a list
    # of three lists of HSV (hue-saturation-value) data
    #
    import paletteTools as pt
    import colorsys
    rgblist = list(img.getdata())
    rgblist = [pt.normalizeRGB(c) for c in rgblist]
    hsvlist = [colorsys.rgb_to_hsv(*rgb) for rgb in rgblist]
    return hsvlist

def jpg_to_hsv(img):
    # convert a jpg image (in form of a PIL.Image object) to a list
    # of three lists of HSV (hue-saturation-value) data
    #
    import colorsys
    rgblist = list(img.getdata())
    rgblist = [(1.0*r/256,1.0*g/256,1.0*b/256) for (r,g,b) in rgblist]
    hsvlist = [colorsys.rgb_to_hsv(*rgb) for rgb in rgblist]
    return hsvlist

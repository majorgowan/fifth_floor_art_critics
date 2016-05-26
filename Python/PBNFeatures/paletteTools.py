def normalizeRGB(rgb, addAlpha=True):
    # take an rgb 3-tuple of integers between 0 and 255
    # if addAlpha==True, return a 4-tuple of floats between 0 and 1
    #   with alpha=1
    # else return a 3-tuple of floats between 0 and 1
    normed = tuple([1.0*c/256 for c in rgb])
    if addAlpha:
        normed += (1.0,)
    return normed

def unflatten(palette, ncolours=None):
    # convert palette from flat list to list of 3-tuples
    ncolours = ncolours or len(palette)/3
    return [tuple(palette[a:a+3]) for a in xrange(0,3*ncolours,3)]

def CGApalette(ncolours=16):
    # retro 4-colour and 16-colour CGA palettes
    if (ncolours == 4):
        return ( 0, 0, 0,
                 255, 0, 0,
                 0, 255, 0,
                 255, 255, 0 )
    elif (ncolours == 16):
        return ( 0, 0, 0,
                 0, 0, 170,
                 0, 170, 0,
                 0, 170, 170,
                 170, 0, 0,
                 170, 0, 170,
                 170, 85, 0,
                 170, 170, 170,
                 85, 85, 85,
                 85, 85, 255,
                 85, 255, 85,
                 85, 255, 255,
                 255, 85, 85,
                 255, 85, 255,
                 255, 255, 85,
                 255, 255, 255 )
    else:
        return None

def paletteConvert(img, palette):
    # convert image to mode "P" given the palette provided
    # (list of 768 integers between 0 and 255 each set of
    #  three of which correspond to a colour in the palette)
    #
    # return a Pillow Image object containing converted image
    from PIL import Image
    # create a new 1-pixel image to hold the palette information
    palimage = Image.new(mode="P", size=(1,1))
    filler = 768-len(palette)
    palimage.putpalette(palette + (0,)*filler)
    return img.convert("RGB").quantize(palette=palimage)

def projectBW(img):
    # convert image to Black & White (not greyscale!)
    # and return number of white pixels and number 
    # of black pixels
    colours = img.convert(mode='1').getcolors()
    whites = [a[0] for a in colours if a[1]==255]
    blacks = [a[0] for a in colours if a[1]==0] 
    return blacks[0], whites[0]

def projectPal(img, ncolours=16):
    # convert image to mode P with given number of colours,
    # return a list of  # the number of pixels of each colour in palette
    # and the palette itself
    imgp = img.convert(mode='P', palette=Image.ADAPTIVE, colors=ncolours)
    colours = imgp.getcolors()
    # full palette (lots of zeros)
    palette = imgp.getpalette()
    # palette as RGB 3-tuples 
    palette = unflatten(palette, ncolours = len(colours))
    return colours, palette

def plotColourDistribution(colours, palette):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = plt.axes()
    # add trivial alpha channel to palette and rescale to 0-1
    rgba = [normalizeRGB(c) for c in palette]
    pos = [a[1] for a in colours]
    heights = [a[0] for a in colours]
    plt.bar(pos, heights, width=0.8, color=rgba)

def paletteToImage(palette):
    # takes a palette (list of RGB 3-tuples)
    # and returns a Pillow Image object
    # with a colourbar representation of the
    # palette
    from PIL import Image
    imgsize = (480,50)
    wid = imgsize[0]/len(palette)
    pixels = []
    for col in palette:
        pixels += wid*[col]
    pixels = imgsize[1]*pixels
    img = Image.new(mode='RGB',size=imgsize)
    img.putdata(pixels)
    return img

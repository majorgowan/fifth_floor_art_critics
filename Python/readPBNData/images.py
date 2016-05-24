def openZipImage(zipname, imagename, prefix=None):
    # given a zip filename and an image filename
    # check if image is in zip and return 
    #
    #   - Pillow Image object for the image
    #
    # optional argument is prefix (subdirectory)
    # in zipfile
    #
    import zipfile
    from StringIO import StringIO
    from PIL import Image
    # ZipFile object for requested zip file
    zf = zipfile.ZipFile(zipname,'r')
    # compose full image name
    if (prefix):
        fullimagename = prefix + '/' + imagename
    else:
        fullimagename = imagename
    # check if imagename is in zip
    if fullimagename not in zf.namelist():
        return None
    else:
        imageData = zf.read(fullimagename)
        dataEnc = StringIO(imageData)
        img = Image.open(dataEnc)
        return img

def miniatures(zipname, filelist, prefix=None, size=(100,100), verbose=False):
    # for all the images in filelist found in the zipfile
    # generate miniature versions of size size
    #
    # save miniatures to files
    #
    #   ../Data/FeatureData/[index]_mini_[size].jpg
    #
    # if they don't already exist
    #
    import os.path
    import description as rd
    inlist = set(rd.imagesInZip(zipname)).intersection(set(filelist))
    # create directory for miniatures if necessary
    if not os.path.exists('../Data/FeatureData'):
            os.makedirs('../Data/FeatureData')
    for imgfile in inlist:
        rootname = os.path.splitext(imgfile)[0]
        destfilename = '../Data/FeatureData/%s_mini_%d_x_%d.jpg' \
                        % (rootname,size[0],size[1])
        if not os.path.isfile(destfilename):
            img = openZipImage(zipname, imgfile, prefix)
            mini = img.resize(size=size)
            if verbose:
                print('saving file ' + destfilename)
            mini.save(destfilename)
        else:
            if verbose:
                print(destfilename + ' already exists')
    return inlist

def cutouts(zipname, filelist, prefix=None, size=(100,100), topleft=(0.25,0.25), verbose=False):
    # for all the images in filelist found in the zipfile
    # generate a small cut-out sample of size size
    # with top-left corner at **relative** position topleft
    #
    # save cut-outs to files
    #
    #   ../Data/FeatureData/[index]_cutout_[size]_[topleft].jpg
    #
    # where size and topleft are values in *pixels*
    #
    # if they don't already exist
    #
    import os.path
    import description as rd
    inlist = set(rd.imagesInZip(zipname)).intersection(set(filelist))
    # create directory for miniatures if necessary
    if not os.path.exists('../Data/FeatureData'):
            os.makedirs('../Data/FeatureData')
    for imgfile in inlist:
        rootname = os.path.splitext(imgfile)[0]
        # open full image
        img = openZipImage(zipname, imgfile, prefix)
        imgSize = img.size
        # compute top-left corner in pixels
        tlp = [int(imgSize[0]*topleft[0]),int(imgSize[1]*topleft[1])]
        tlp[0] = min(tlp[0],imgSize[0]-size[0])
        tlp[1] = min(tlp[1],imgSize[1]-size[1])
        # compose filename
        destfilename = '../Data/FeatureData/%s_cutout_%d_x_%d_topleft_%d_%d.jpg' \
                        % (rootname,size[0],size[1],tlp[0],tlp[1])
        if not os.path.isfile(destfilename):
            cutout = img.crop(box=(tlp[0],tlp[1],tlp[0]+size[0],tlp[1]+size[1]))
            if verbose:
                print('saving file ' + destfilename)
            cutout.save(destfilename)
        else:
            if verbose:
                print(destfilename + ' already exists')
    return inlist


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

def imagesInZip(zipname, filelist, prefix=None, maxLen=None, returntype='indices'):
    # given a zip filename and a list of image
    # filenames, return:
    #
    #   - list of rows in image zip file
    #
    # optional argument is prefix (subdirectory)
    # in zipfile
    #
    import zipfile
    # ZipFile object for requested zip file
    zf = zipfile.ZipFile(zipname,'r')
    if not maxLen:
        maxLen = len(filelist)
    if not prefix:
        prefix = '.'
    if (returntype == 'indices'):
        inlist = [i for i,x in enumerate(filelist[:maxLen])
                        if (prefix + '/' + x) in zf.namelist()]
    elif (returntype == 'names'):
        inlist = [x for x in filelist[:maxLen] if (prefix + '/' + x) in zf.namelist()]
    return inlist

def miniatures(zipname, filelist, prefix=None, size=(100,100)):
    # for all the images in imagelist found in the zipfile
    # generate miniature versions of size size
    #
    # save miniatures to files
    #
    #   ../Data/FeatureData/[index]_mini_[size].jpg
    #
    # if they don't already exist
    #
    import os.path
    inlist = imagesInZip(zipname, filelist, prefix=prefix, returntype='names')
    for imgfile in inlist:
        destfilename = '../Data/FeatureData/%05d_mini_%d_x_%d.jpg' \
                        % (imgfile,size[0],size[1])
        if os.path.isfile(destfilename):
            img = openZipImage(zipname, imgfile, prefix)
            mini = img.resize(size=size)
            print('saving file ' + destfilename)
            mini.save(destfilename)
        else:
            print(distfilename + ' already exists')
    return inlist


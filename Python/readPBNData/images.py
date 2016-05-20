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

def miniatures(zipname, filelist, prefix=None, size=(100,100)):
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
            print('saving file ' + destfilename)
            mini.save(destfilename)
        else:
            print(destfilename + ' already exists')
    return inlist


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

def imagesInZip(zipname, filelist, prefix=None, maxLen=None):
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
    # compose full image name
    if (prefix):
        inlist = [i for i,x in enumerate(filelist[:maxLen])
                    if (prefix + '/' + x) in zf.namelist()]
    else:
        inlist = [i for i,x in enumerate(filelist[:maxLen]) if x in zf.namelist()]
    return inlist


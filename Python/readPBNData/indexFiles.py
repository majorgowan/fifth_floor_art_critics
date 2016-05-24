def imageInfo(zipname, columns, overwrite=False):
    #
    # THIS METHOD RUNS VERY SLOWLY (MORE SLOWLY
    # THAN EVEN GENERATING MINIATURES!!!) ...
    # HARD TO IMAGINE BUT MIGHT BE BECAUSE OF
    # THE [list].index() CALL (???)
    #
    # scan a given zipfile and generate a csv file
    # with filename, artist, pixelwidth, pixelheight.
    # Save result in ../Data directory with same
    # name as zip file and extension csv
    #
    import os.path
    import zipfile
    import images as ri
    # generate output filename
    zipbase = os.path.splitext(zipname)[0]
    zipbaseroot = os.path.basename(zipbase)
    csvoutname = zipbase + ".csv"
    if not overwrite:
        # abort if csvoutname exists
        if os.path.isfile(csvoutname):
            print("CSV index file already exists!")
            return False
    with open(csvoutname,'w') as outfile:
        outfile.write("filename, artist, width, height\n")
        # get list of files in zip
        zflist = zipfile.ZipFile(zipname, 'r').namelist()[1:]
        for imgfile in zflist:
            imgbase = os.path.basename(imgfile)
            # look up artist
            ind = columns['filename'].index(imgbase)
            artist = columns['artist'][ind]
            # open image and get size
            img = ri.openZipImage(zipname,imgbase,prefix=zipbaseroot)
            width, height = img.size
            outfile.write(imgbase + "," \
                        + artist + "," \
                        + str(width) + "," \
                        + str(height) + "\n")
    return True

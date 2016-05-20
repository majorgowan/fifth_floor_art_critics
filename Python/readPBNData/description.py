def openZip(filename):
    # given a zip file, locate all csv files (not starting with '_'
    # and return:
    #
    #   - a list of filenames
    #   - a list of file-like objects pointing to csv files
    #
    import zipfile 
    import re
    # ZipFile object for requested zip file
    zf = zipfile.ZipFile(filename,'r')
    # find csv files (not starting with '_'
    csvs = [w for w in zf.namelist() if re.search('^[^_].*\.csv$',w)]
    # for each csv file in archive, convert to file-like object
    fileLike = []
    for csv in csvs:
        fileLike.append(zf.open(csv))
    return csvs, fileLike

def readCSV(fileLike, header=True):
    # return a list of lists containing data from a csv file
    # return column names
    from csv import reader
    lines = []
    head = None
    if (header):
        head = fileLike.readline().strip().split(',')
    for line in reader(fileLike):
        lines.append(line)
    if not header:
        head = ['col%03d' % i for i in range(len(lines[0]))]
    return lines, head

def columns(lines, head):
    # return a dictionary of columns with keys from column names
    cols = {}
    for i, name in enumerate(head):
        cols[name] = [line[i] for line in lines]
    return cols

def table(vector_input, ordered=True, numeric=False):
    # return list of tuples consisting of: 
    #
    #   (distinct elements in vector_input, number of occurrences in vector_input) 
    #
    from collections import Counter
    def num(val):
        try:
            return int(float(val))
        except ValueError:
            return 0
    if numeric:
        vector = [num(v) for v in vector_input]
    else:
        vector = vector_input
    freq = Counter(vector)
    data = []
    for item in set(vector):
        data.append((item, freq[item]))
    # sort by most frequent
    if (ordered):
        data = sorted(data, key=lambda item: item[1], reverse=True)
    return data

def imagesInZip(filename, strippath=True):
    # return list of jpg filenames in an zip file
    import zipfile
    import re
    import os.path
    zf = zipfile.ZipFile(filename,'r')
    if (strippath):
        return [os.path.basename(w) for w in zf.namelist() if re.search('.+\.jpg$',w)]
    else:
        return [w for w in zf.namelist() if re.search('.+\.jpg$',w)]

def sameArtist(artistName, columns, imageList=None):
    # return list of paintings by the specified artist
    # optional argument computes intersection with supplied imageList
    #
    fullList = [columns['filename'][i] for i,name in enumerate(columns['artist']) if name==artistName]
    if (imageList):
        return sorted(list(set(fullList).intersection(set(imageList))))
    else:
        return fullList

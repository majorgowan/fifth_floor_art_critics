def openZip(filename, start=0, end=None):
    # given a zip file, locate all csv files (not starting with '_'
    # and return:
    #
    #   - a list of filenames
    #   - a list of file-like objects pointing to csv files
    #
    import zipfile as zf
    import re
    # ZipFile object for requested zip file
    dataZip = zf.ZipFile(filename,'r')
    # find csv files (not starting with '_'
    csvs = [w for w in dataZip.namelist() if re.search('^[^_].*\.csv$',w)]
    # for each csv file in archive, convert to file-like object
    fileLike = []
    for csv in csvs:
        fileLike.append(dataZip.open(csv))
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

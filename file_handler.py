"""
Handles the opening and updating of
the config file, which is used by multiple
modules as shared data storage
"""
import json
def initialise_file(filename):
    """ opens a json file and returns the contents
    Arguments:
        filename - string
    Parameters:
        file contents - dictionary
    """
    jfile = open(filename, "r", encoding="utf-8")
    filecontents = json.load(jfile)
    jfile.close()
    return filecontents

def update_file(newfile):
    """ overwrites the input filename
    with an input dictionary

    Arguments:
       newfile - dictionary
    """
    jfile = open("appdata.json", "w", encoding="utf-8")
    json.dump(newfile, jfile)
    jfile.close()

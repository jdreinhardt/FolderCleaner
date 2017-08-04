import os
import sys
import getopt
import time

def deletionCandidateSearch (file, daysAgo):
    '''
    Uses the age parameter set using argv, or the defined default. 
    Gets the current unix time and subracts the seconds in a day times
    the number of days set to set an age watermark.
    '''
    now = time.time()
    ageWatermark = now - float(86400 * int(daysAgo))
    age = lastModified(file)
    if optVerbose == True:
        print("Age: " + str(round(((now - age) / 86400), 2)) + " days. File: " + file)
    if age < ageWatermark:
        return True
    else:
        return False

def lastModified (file):
    '''
    Returns the last modified date on a file that is pass in. 
    '''
    modifiedDate = os.path.getmtime(file)
    return modifiedDate

def deleteObject (obj):
    '''
    Responsible for deleting any object passed in. It assumes that 
    all objects are files. If an exception occurs it then tries the
    object as a folder. If both fail a False is returned.
    '''
    try:
        if optTestOnly != True:
            os.remove(obj)
        return True
    except:
        try:
            if optTestOnly != True:
                os.rmdir(obj)
            return True
        except:
            return False

def parseOldFiles (rootDir, daysAgo):
    '''
    Walks directory tree looking for files that are over the 
    specified age since last modified. Age is set in argv and
    not used outside of ageCheck()
    '''
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            #Build full file path for future queries
            filePath = os.path.join(dirName, fname)
            delCan = deletionCandidateSearch(filePath, daysAgo)
            if delCan == True:
                #If unsuccessful in delete attempt
                if deleteObject(filePath) != True:
                    if optSilent != True:
                        print("ERROR Deleting File: " + filePath)
                else:
                    if optVerbose == True:
                        print("DELETE file: " + filePath)
                    if optTestOnly == True:
                        print("NOTICE: " + filePath + " is older than the watermark")

def parseEmptyFolders (rootDir):
    '''
    Walks directory tree looking for empty folders. If found
    empty folders are deleted. 
    '''
    for dirName, subdirList, fileList in os.walk(rootDir):
        if os.listdir(dirName) == []:
            #Empty directory found
            if optVerbose == True:
                print("Empty directory found")
            if deleteObject(dirName) != True:
                if optSilent != True:
                    print("ERROR Deleting Folder: " + dirName)
            else:
                if optVerbose == True:
                    print("DELETE folder: " + dirName)
                if optTestOnly == True:
                        print("NOTICE: " + dirName + " is empty")

def parseLocation (rootDir, optFilesOnly, daysAgo):
    '''
    The base parse path that will engage all checks for
    files older than the set watermark, and any empty folder
    '''
    if optVerbose == True:
        print("INFO: start parse for old files in " + rootDir)
    parseOldFiles(rootDir, daysAgo)

    if optFilesOnly != True:
        if optVerbose == True:
            print("INFO: start parse for empty folders in " + rootDir)
        parseEmptyFolders(rootDir)

    if optVerbose == True:
        print("INFO: Processing complete")

def main (argv):
    locations = []

    #Globals used in multiple functions
    global optVerbose
    global optSilent
    global optTestOnly

    #Define default values if not set
    optVerbose = False
    optSilent = False
    optTestOnly = False

    daysAgo = 7
    optFilesOnly = False

    #Command-line argument parsing
    try:
        opts, args = getopt.getopt(argv, "hp:d:fvst", ["help","path","days","files","verbose","silent","testonly"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-p", "--path"):
            locations.append(a)
        elif o in ("-d", "--days"):
            daysAgo = a
        elif o in ("-f", "--files"):
            optFilesOnly = True
        elif o in ("-v", "--verbose"):
            optVerbose = True
        elif o in ("-s", "--silent"):
            if optVerbose == True:
                print("Cannot call both verbose and silent")
                sys.exit(1)
            else:
                optSilent = True
        elif o in ("-t", "--testonly"):
            optTestOnly = True
        else:
            assert False, "unhandled option"

    if locations == []:
        print("No path entered")
    else:
        for dirPath in locations:
            if os.path.isdir(dirPath) == True:
                parseLocation(dirPath, optFilesOnly, daysAgo)
            else:
                print(dirPath + " is not a valid path")

def usage ():
    '''
    Help parameters.
    '''
    usage = """
    -h --help       What you're reading
    -p --path       Path to parse (required)
    -d --days       Overwrite the default age parameter (default: 7)
    -f --files      Delete files only. Skip empty direcories
    -v --verbose    Verbose Output
    -s --silent     Silence all output
    -t --testonly   Run script with verbosity and no deletes
    """
    print(usage)

if __name__ == "__main__":
    main(sys.argv[1:])

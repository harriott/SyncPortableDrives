#!/usr/bin/python3
# vim: set tw=79:

"""
Print to file differences in two directory structures, ignoring file contents.

Looking recursively in two directories (which are defined below),
print to file the differences found in the subdirectory names,
highlighting odd subdirectories.

Reason for this:
SyncBackFree is a powerful synchronisation program, but with two drawbacks:
    * big changes in directory structure are hard to interpret and act upon
    * it seems to sync the existence of empty directories without reporting
So when I've changed a lot on my netbook, and wish to sync my directory
with my portable hard drive, I can run this module first, and use the output
to guide me through some manual directory synching before running SyncBackFree.

This program does not change anything, but just (re)writes the result file,
which is automatically named after this program.
"""
import os
import socket
import sys
import time
import datetime
import re

# Get the start time, to be able to check against later:
start = time.time()
# Get the datetime:
startd = datetime.datetime.now().isoformat(' ')

# Specify the parent directory's location:
drv = ['D:/', 'E:/']

# List of empty directories not to be flagged up
# (add regex's to this as required):
known_empty = [r'\.dropbox\.cache',
               r'Firefox\\.*default\\',
               r'SOFTWARE\\DOTNET\\ENGLISH',
               r'debian-7.5.0-i386-xfce-CD-1\\Snapshots',
               r'\\CDExPortable\\',
               r'\\Gigabyte GA M57SLI-S4\\',
               r'\\tempera\\admin\\images\\schemes',
               r'\\\.git\\',
               r'\\\.vim\\',
               r'\\vim-markdown\\\.git\\',
               r'\\vimfiles\\',
               r'i5800 Camera',
               r'Cross-platform\\ImageMagick',
               r'config\\soffice\.cfg\\modules\\']

# Get this script's filename without extension,
# for use as the name of the directory to be synched:
dtbs = (os.path.basename(os.path.splitext(sys.argv[0])[0]))
# and for use as the name of the output file:
outfile = dtbs + '.txt'
print('When this is done, you should open', outfile, '\n')


def dirlister(dirTolist):
    """ Prepare a subdirectory list, with relative paths included.
    (Progress is reported, and odd directories are highlighted.)"""
    print('Looking at contents of', dirTolist, ':')
    dlc = olc = 0
    # Initialise two lists just with the base folder path:
    dirList = [dirTolist]
    oddList = [dirTolist]
    for root, folders, files in os.walk(dirTolist):
        for subd in folders:
            # Report a progress count:
            dlc += 1
            print('\r', dlc, end=' ')
            # subd is just the folder name, need to add its path:
            abspath = os.path.join(root, subd)
            relpath = abspath.replace(dirTolist+"\\", "")
            # First check there's not an unwriteable
            # Unicode escape character gotten in there:
            if '\ufffd' in abspath:
                # Store such messed-up directory paths as ASCII:
                oddList.append(ascii(relpath))
                olc += 1
            else:
                # Check there's something in the subdirectory:
                if (os.listdir(abspath) or
                        # (treat known empty subdirectories normally:)
                        any(re.search(ke, abspath) for ke in known_empty)):
                    # Add relative path to the subdirectory name, and store it
                    # in the list for the directory to be compared:
                    dirList.append(relpath)
                else:
                    # Add relative path to the subdirectory name, and store it
                    # in the list of empty directories:
                    oddList.append(relpath)
                    olc += 1
                    # Store the full path of an empty directory in the list
                    # (thus highlighting it):
                    # dirList.append(abspath)
    print(' - subdirectory records loaded in')
    # Adjust the first (title) items:
    dlctxt = (' ---> contains ' + str(dlc) + ' subdirectories, these ones ')
    oddList[0] += (dlctxt + 'are oddly Empty:')
    dirList[0] += (dlctxt + 'are Unmatched:')
    return dirList, (dlc - olc), oddList


# Now build two lists of subdirectories, with counts.
# Initialise a list to contain the two pairs of lists:
list = [[], []]
# (taking care to ensure they've separate id's)
empt = [[], []]
# and the two counts:
sdc = [0, 0]
# Get the lists:
for d in range(0, 2):
    list[d], sdc[d], empt[d] = dirlister(drv[d] + dtbs)
print(sdc)


# Identify the index of the list to be picked through:
if sdc[0] < sdc[1]:
    d = 0
# Prepare an empty list to move unmatched items into:
listd = []
# Identify an index for the other (possibly longer) list:
dl = abs(d-1)

# Pick through one list now, comparing items with with the other list:
print('Cross-checking now for differences :')
for _ in range(sdc[d]+1):
    # Pull off the first item from the pick-list:
    item = list[d].pop(0)
    print('\r', _, end=' ')
    # If the item's in the other list, remove it from there too:
    try:
        list[dl].remove(item)
    # If not, save it to the (new) unmatched list:
    except ValueError:
        listd.append(item)
print(' - subdirectory records compared')


# Create a file object for output:
fo = open(outfile, 'w')

# Create a nice header:
wrt1 = '\n' + socket.gethostname()+' folder changes at '+startd+'\n'
wrt2 = '\n'+'\n'.join(empt[0])+'\n\n'+'\n'.join(empt[1])+'\n'
# Next the two lists of unmatched items
# (automatically headed by their title lines):
wrt3 = '\n'+'\n'.join(list[dl])+'\n\n'+'\n'.join(listd)+'\n'
# And the time taken:
wrt4 = '\ntook '+str(time.time()-start)+' seconds to find the differences'

# Write and close the file object:
fo.write(wrt1+wrt2+wrt3+wrt4)
fo.close()

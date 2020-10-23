#! /usr/bin/env python3
#
# based on https://anonscm.debian.org/viewvc/pkg-boost/boost/
#    trunk/debian/update-control.py
#

import re
import sys

from debian.deb822 import Deb822

gOldVersion = None
gNewVersion = None


class DpdkVersion:
    def __init__(self, version):
        (self.Major, self.Minor) = version.split('.')
        self.PackageVersion = self.Major + '.' + self.Minor


def replaceVersion(string, ver1, ver2):
    '''Search 'string' for a DpdkVersion ver1.  If
    SharedObjectVersion or PackageVersion of ver1 is found, replace by
    corresponding ver2 version string.  Return the updated string.'''
    string = re.sub(ver1.PackageVersion, ver2.PackageVersion, string)
    return string


def updateVersionedValue(paragraph, key):
    if key not in paragraph:
        return
    oldValue = paragraph[key]
    paragraph[key] = replaceVersion(paragraph[key], gOldVersion, gNewVersion)
    return (oldValue, paragraph[key])


def conflictsWithPrevious(paragraph):
    if 'Conflicts' not in paragraph:
        return False
    nameRe = re.sub('\d', '\\d', paragraph['Package'])
    return re.search(nameRe, paragraph['Conflicts']) is not None


def updateConflicts(paragraph, oldPkgName):
    newPkgName = paragraph['Package']
    needsConflict = ((newPkgName.endswith("-dev")
                      and not newPkgName.endswith("-all-dev"))
                     or conflictsWithPrevious(paragraph))
    if not needsConflict:
        return
    if 'Conflicts' in paragraph:
        if paragraph['Conflicts'].find(oldPkgName) == -1:
            paragraph['Conflicts'] += ', ' + oldPkgName
    else:
        paragraph['Conflicts'] = oldPkgName


def processSourceParagraph(p):
    updateVersionedValue(p, 'Source')


def processPackageParagraph(p):
    (oldPkgName, newPkgName) = updateVersionedValue(p, 'Package')
    updateVersionedValue(p, 'Depends')
    updateVersionedValue(p, 'Recommends')
    updateVersionedValue(p, 'Suggests')
    updateConflicts(p, oldPkgName)


def printParagraph(p):
    for key in p.keys():
        print("%s: %s" % (key, p[key]))


def processControl():
    firstParagraph = True
    for paragraph in Deb822.iter_paragraphs(open('control')):
        if firstParagraph:
            processSourceParagraph(paragraph)
            printParagraph(paragraph)
            firstParagraph = False
        else:
            processPackageParagraph(paragraph)
            print
            printParagraph(paragraph)


if len(sys.argv) < 3:
    print("Usage: cd debian/; %s <old version> <new version>"
          " > control_new" % sys.argv[0])
    exit(1)

gOldVersion = DpdkVersion(sys.argv[1])
gNewVersion = DpdkVersion(sys.argv[2])
processControl()
print

"""
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script translates an FCHK file to an XYZ file. Both filetypes
contain molecular structure information. FCHK is specific from
Gaussian09 while XYZ is widely used and can be read by various
molecular modeling softwares.

Run as: python fchk2xyz.py file.fchk
"""

import sys
from itertools import islice


# check input file
def check(argvs):
    if len(argvs) == 0:
        print("Error! No FCHK file specified.")
        print("Exiting now...")
        sys.exit()

    if argvs[1][-4:] != "fchk":
        print("Error! File is not FCHK format.")
        print("Exiting now...")
        sys.exit()

    fchkfile = sys.argv[1]

    return fchkfile


# get indeces of lines of interest on fchk file
def get_index(ifile):
    flags = {}
    with open(ifile) as fo:
        forceF = 0
        for num, line in enumerate(fo, 1):
            if 'Number of basis functions' in line:
                flags.update({'nbasis': num})

            elif 'Nuclear charges' in line:
                flags.update({'nuclCh': num})

            elif 'Current cartesian coordinates' in line:
                flags.update({'cartCord': num})

            elif 'Force Field' in line:  # for stop
                if forceF == 0:
                    forceF = num
                    flags.update({'forceF': num})
    return flags


# make xyz file from input fchk file
# user should expand dictionary at convenience
def make_xyz(ifile, indx):
    elem = {'1': 'H',
            '6': 'C', '7': 'N', '8': 'O', '9': 'F',
            '15': 'P', '16': 'S', '17': 'Cl',
            '22': 'Ti', '26': 'Fe', '27': 'Co', '28': 'Ni', '29': 'Cu',
            '30': 'Zn', '35': 'Br', '44': 'Ru', '53': 'I'}
    angs = 0.529177249
    nucl = []
    clst = []

    for key in indx:
        if key == 'nuclCh':
            a = indx[key]
        elif key == 'cartCord':
            b = indx[key]
        elif key == 'forceF':
            c = indx[key]

    with open(ifile) as lines:
        for line in islice(lines, a, b-1):
            buff = line.strip('\n')
            buff = buff.split()
            for i in range(len(buff)):
                buff[i] = str(int(float(buff[i])))
            for key in elem:
                for i in range(len(buff)):
                    buff[i] = buff[i].replace(key, elem[key])
            for i in range(len(buff)):
                nucl.append(buff[i])

    with open(ifile) as lines:
        for line in islice(lines, b, c-1):
            buff = line.strip('\n')
            buff = buff.split()
            for i in range(len(buff)):
                clst.append(float(buff[i])*angs)

    if len(clst) != 3*len(nucl):
        print("Error! Number of coordinates doesn't match number of atoms"
              "\nTerminating program.")
        sys.exit()

    ofile = open(ifile[:-5]+'.xyz', 'w')
    ofile.write(str(len(nucl))+'\n'+ifile+'\n')

    i = 0
    for j in range(0, len(clst), 3):
        clst[j] = "{0:.10f}".format(float(clst[j]))
        clst[j+1] = "{0:.10f}".format(float(clst[j+1]))
        clst[j+2] = "{0:.10f}".format(float(clst[j+2]))

        ws = '          '  # whitespace

        if float(clst[j]) < 0:
            clst[j] = ws[:-1]+clst[j]
        else:
            clst[j] = ws+clst[j]

        if float(clst[j+1]) < 0:
            clst[j+1] = ws[:-7]+clst[j+1]
        else:
            clst[j+1] = ws[:-6]+clst[j+1]

        if float(clst[j+2]) < 0:
            clst[j+2] = ws[:-7]+clst[j+2]
        else:
            clst[j+2] = ws[:-6]+clst[j+2]

        buff = nucl[i] + clst[j] + clst[j+1] + clst[j+2] + '\n'

        ofile.write(buff)
        i += 1

    ofile.close()


# MAIN PROGRAM
def main(argvs):
    fchk = check(argvs)
    make_xyz(fchk, get_index(fchk))


# RUN PROGRAM
argvs = sys.argv
main(argvs)

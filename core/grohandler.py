#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG = 1

from filehandler import *
from errorhandler import *

class GromacsAtom:
    '''Instance of an atom'''
    def __init__(self, natom, position, name, velocity=[0., 0., 0.]):
        self.natom = natom
        self.position = position
        self.name = name
        self.velocity = velocity

class GromacsResidue:
    '''Instance of a residue or molecule'''
    def __init__(self, nresidue, name, atoms=[]):
        self.nresidue = nresidue
        self.name = name
        self.atoms = atoms
    def add_atom(self, atom):
        self.atoms.append(atom)
    def n_atoms(self):
        return len(self.atoms)
        

class GromacsSystem:
    '''Instance of a simulation box'''
    def __init__(self, title="", dimentions=[], natoms=0, residues=[]):
        self.title = title
        self.dimentions = dimentions
        self.nAtoms = natoms
        self.residues = residues
    def add_residue(self, residue):
        self.residues.append(residue)
        self.nAtoms += residue.n_atoms()

def _parse_atom_info(line):
    '''Reads a line from a .gro file and returns an atom instance with the parsed
    information'''
    if (line[44:] == '\n'):
        return GromacsAtom(natom= int(line[15:20]),
                           name= line[10:15].replace(' ',''),
                           position= list(map(float,
                                              line[20:44],split()
                                              )
                                          )
                           )
    else:
        return GromacsAtom(natom= int(line[15:20]),
                           name= line[10:15].replace(' ',''),
                           position= list(map(float,
                                              line[20:44].split()
                                              )
                                          ),
                           velocity= list(map(float,
                                              line[44:68].split()
                                              )
                                          )
                           )

def _parse_residue_info(line):
    '''Reads a line from a .gro file and return the number of the current residue
    and its name'''
    _resName = line[5:10].replace(' ','')
    _resNumber = int(line[0:5])
    return _resNumber, _resName

def readGro(filename):
    '''Reads a .gro file and creates a system instance with it'''
    _inputFile = open(filename, 'r')
    _systemName = _inputFile.readline()
    _systemNAtoms = int(_inputFile.readline())
    
    
    
                
        
#BUG: Atom number must change independently from what's in the file.
def writeGro(system, output):
    '''Takes a system instance and writes a .gro file with its data'''
    with open(output, "w") as file:
        file.write(system.title+"\n")
        file.write(str(system.natoms).rjust(5)+"\n")
        for nres in range(len(system.residues)):
            for natm in range(len(system.residues[nres].atoms)):
                file.write(str(nres+1).rjust(5)+
                           system.residues[nres].name.ljust(5)+
                           system.residues[nres].atoms[natm].name.ljust(5)+
                           str(natm+1).rjust(5)+
                           '{:>8}{:>8}{:>8}'.format(*['%.3f'%x for x in
                            system.residues[nres].atoms[natm].position])+"\n")
        file.write('{:>10}{:>10}{:>10}'.format(*['%.5f'%x for x in
                    system.dimentions]))
    return True



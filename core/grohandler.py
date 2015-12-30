#!/usr/bin/python3
# -*- coding: utf-8 -*-

DEBUG = 1

#from filehandler import *
#from errorhandler import *
import numpy as np


class GromacsAtom:
    '''Instance of an atom'''

    def __init__(self, natom, position, name, velocity=[]):
        self.nAtom = natom
        self.position = position
        self.name = name
        self.velocity = velocity

    def set_position(self, new_position):
        '''Moves the atom to an specified position'''
        _oldPosition = np.array(self.position)
        self.position = new_position
        return np.array(new_position) - _oldPosition

    def translate(self, translation):
        '''Moves the atom along a specified vector'''
        _oldPosition = np.array(self.position)
        self.position = list(_oldPosition + np.array(translation))
        return self.position


class GromacsResidue:
    '''Instance of a residue or molecule'''

    def __init__(self, nresidue, name, atoms=[]):
        self.nResidue = nresidue
        self.name = name
        self.atoms = atoms

    def add_atom(self, atom):
        '''Copies an atom instance onto the current residue'''
        self.atoms.append(GromacsAtom(atom.nAtom,
                                      atom.position,
                                      atom.name,
                                      atom.velocity)
                          )

    def n_atoms(self):
        '''Return the number of atoms in the residue'''
        return len(self.atoms)

    def get_cop(self):
        '''Calculates and returns the center of position'''
        _sumPositions = np.zeros(3)
        for atom in self.atoms:
            _sumPositions += np.array(atom.position)
        return list(_sumPositions / self.n_atoms())

    def center_around(self, atomName, center=[0., 0., 0.]):
        '''Sets an specified atom in the origin (or any specified center) and
        moves the rest respectively'''
        for atom in self.atoms:
            if (atom.name == atomName):
                _selectedAtom = atom
                _translation = atom.set_position(center)
                break
        else:
            return False
        for atom in self.atoms:
            if (atom != _selectedAtom):
                atom.translate(_translation)
        return True

    def translate(self, translation):
        '''Moves all the atoms in the residue towards an specified vector'''
        for atom in self.atoms:
            atom.translate(translation)
            pass
        return True

    def rotate(self, angle, axis='Z'):
        '''Rotates the residue around an specified axis'''
        if axis is 'X':
            _rotationMatrix = np.matrix([[1, 0, 0],
                                         [0, np.cos(angle), -np.sin(angle)],
                                         [0, np.sin(angle), np.cos(angle)]
                                         ])
        elif axis is 'Y':
            _rotationMatrix = np.matrix([[np.cos(angle), 0, np.sin(angle)],
                                         [0, 1, 0],
                                         [-np.sin(angle), 0, np.cos(angle)]
                                         ])
        elif axis is 'Z':
            _rotationMatrix = np.matrix([[np.cos(angle), -np.sin(angle), 0],
                                         [np.sin(angle), np.cos(angle), 0],
                                         [0, 0, 1]
                                         ])
        else:
            return False
        for atom in self.atoms:
            _oldPosition = np.array(atom.position)
            _newPosition = np.dot(_rotationMatrix, _oldPosition)
            atom.position = _newPosition.tolist()[0]
            pass
        return True

    def __del__(self):
        self.nResidue = None
        self.name = None
        self.atoms = []


class GromacsSystem:
    '''Instance of a simulation box'''

    def __init__(self, title="", dimentions=[], nAtoms=0, residues=[]):
        self.title = title
        self.dimentions = dimentions
        self.nAtoms = nAtoms
        self.residues = residues

    def add_residue(self, residue):
        '''Copies a residue onto the current system'''
        self.residues.append(GromacsResidue(residue.nResidue,
                                            residue.name,
                                            residue.atoms)
                             )
        self.nAtoms += residue.n_atoms()


def _parse_atom_info(line):
    '''Reads a line from a .gro file and returns an atom instance with the parsed
    information'''
    if (line[44:] is '\n'):
        return GromacsAtom(natom=int(line[15:20]),
                           name=line[10:15].replace(' ', ''),
                           position=list(map(float,
                                             line[20:44].split()
                                             )
                                         )
                           )
    else:
        return GromacsAtom(natom=int(line[15:20]),
                           name=line[10:15].replace(' ', ''),
                           position=list(map(float,
                                             line[20:44].split()
                                             )
                                         ),
                           velocity=list(map(float,
                                             line[44:68].split()
                                             )
                                         )
                           )


def _parse_residue_info(line):
    '''Reads a line from a .gro file and return the number of the current residue
    and its name'''
    resName = line[5:10].replace(' ', '')
    resNumber = int(line[0:5])
    return resNumber, resName


def readGro(filename):
    '''Reads a .gro file and creates a system instance with it'''
    inputFile = open(filename, 'r')
    systemName = inputFile.readline().replace('\n', '')
    systemNAtoms = int(inputFile.readline())
    fileLines = inputFile.readlines()
    inputFile.close()
    systemSize = list(map(float, fileLines.pop().split()))
    outSystem = GromacsSystem(title=systemName, dimentions=systemSize,
                              residues=[])
    currentResidue = GromacsResidue(*_parse_residue_info(fileLines[0]))
    currentResidue.atoms = []
    for line in fileLines:
        if (_parse_residue_info(line)[0] == currentResidue.nResidue):
            currentResidue.add_atom(_parse_atom_info(line))
        else:
            outSystem.add_residue(currentResidue)
            currentResidue = GromacsResidue(*_parse_residue_info(line))
            currentResidue.atoms = []
            currentResidue.add_atom(_parse_atom_info(line))
    outSystem.add_residue(currentResidue)
    if (outSystem.nAtoms != systemNAtoms):
        print("WARN :", systemNAtoms, 'atoms were declared in the input'
              'file, but', outSystem.nAtoms, 'were found.')
    del(systemName, systemNAtoms, fileLines, systemSize, currentResidue)
    return outSystem


def string_position(position):
    string = ''
    for coord in position:
        string += str(round(coord, 3)).rjust(8)
    return string


def string_velocity(velocity):
    string = ''
    if (velocity == []):
        return string
    else:
        for coord in velocity:
            string += str(round(coord, 4)).rjust(8)
        return string


def string_size(size):
    string = ''
    for i in size:
        string += str(i) + ' '
    return string


def writeGro(filename, system):
    output = open(filename, 'w')
    output.write(system.title + '\n')
    output.write(str(system.nAtoms).rjust(5) + '\n')
    atomNumber = 1
    for i in range(len(system.residues)):
        resName = system.residues[i].name
        resNumber = str(i + 1)
        for j in range(system.residues[i].n_atoms()):
            atom = system.residues[i].atoms[j]
            output.write(resNumber.rjust(5) +
                         resName.ljust(5) +
                         atom.name.rjust(5) +
                         str(atomNumber).rjust(5) +
                         string_position(atom.position) +
                         string_velocity(atom.velocity) +
                         '\n'
                         )
            atomNumber += 1
            pass
        pass
    output.write(string_size(system.dimentions) + '\n')
    output.truncate()
    output.close()
    return True

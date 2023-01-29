from dataclasses import dataclass
import numpy as np

@dataclass()
class Node:
    nid: int
    x: float
    y: float
    z: float = 0.

@dataclass()
class Element:
    eid: int
    elem_type: str
    attached_nodes: list[int]

@dataclass()
class Boundary:
    nid: int
    first_dof: int
    last_dof: int
    value: float

    @property
    def dof_array(self):
        return np.array([i for i in range(int(self.first_dof), int(self.last_dof) + 1)])

@dataclass
class Load:
    nid: int
    dof: int
    value: float

def parse_input_file(input_file):

    print(f'\nParsing input file: {input_file}')
    
    with open(input_file) as f:
        lines = [line.strip() for line in f]

    nodes, elements, spc, load = {}, {}, {}, {}

    bNode, bBeam, bRod, bSpc, bLoad = False, False, False, False, False

    for line in lines:

        line = line.lower()

        if line.startswith('#'):
            continue

        # N O D E S
        if line.startswith('*node'):
            bNode = True
            bBeam, bRod, bSpc, bLoad = False, False, False, False
        elif bNode and not line.startswith('*'):
            lineSplit = line.split(',')
            nid = lineSplit[0]
            nodes[nid] = Node(nid, lineSplit[1], lineSplit[2])

        # E L E M E N T S
        elif line.startswith('*element') and 'beam' in line:
            bBeam = True
            bNode, bRod, bSpc, bLoad = False, False, False, False
            elem_type = 'beam'
        elif bBeam and not line.startswith('*'):
            lineSplit = line.split(',')
            eid = lineSplit[0]
            elements[eid] = Element(eid, elem_type, [lineSplit[1],lineSplit[2]])

        elif line.startswith('*element') and 'rod' in line:
            bRod = True
            bNode, bBeam, bSpc, bLoad = False, False, False, False
            elem_type = 'rod'
        elif bRod and not line.startswith('*'):
            lineSplit = line.split(',')
            eid = lineSplit[0]
            elements[eid] = Element(eid, elem_type, [lineSplit[1],lineSplit[2]])

        # B O U N D A R Y
        elif line.startswith('*boundary'):
            bSpc = True
            bNode, bBeam, bRod, bLoad = False, False, False, False
        elif bSpc and not line.startswith('*'):
            lineSplit = line.split(',')
            nid = lineSplit[0]
            if not nid in spc:
                spc[nid] = [ Boundary(nid, lineSplit[1], lineSplit[2], lineSplit[3]) ]
            else:
                spc[nid].append(Boundary(nid, lineSplit[1], lineSplit[2], lineSplit[3]))

        # L O A D
        elif line.startswith('*load'):
            bLoad = True
            bNode, bBeam, bRod, bSpc = False, False, False, False
        elif bLoad and not line.startswith('*'):
            lineSplit = line.split(',')
            nid = lineSplit[0]
            load[nid] = Load(nid, lineSplit[1], lineSplit[2])

        else: 
            bNode, bBeam, bRod, bSpc = False, False, False, False

    return nodes, elements
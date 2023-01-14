import numpy as np
import sys
from dataclasses import dataclass

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

def parse_input_file(input_file):

    print(f'Parsing input file: {input_file} ...')
    
    with open(input_file) as f:
        lines = [line.strip() for line in f]

    nodes, elements = {}, {}

    bNode, bBeam, bRod = False, False, False

    for line in lines:

        line = line.lower()

        if line.startswith('#'):
            continue

        # N O D E S
        if line.startswith('*node'):
            bNode = True
            bBeam, bRod = False, False
        elif bNode and not line.startswith('*'):
            lineSplit = line.split(',')
            nid = lineSplit[0]
            nodes[nid] = Node(nid, lineSplit[1], lineSplit[2])

        # E L E M E N T S
        elif line.startswith('*element') and 'beam' in line:
            bNode, bRod = False, False
            bBeam = True
            elem_type = 'beam'
        elif bBeam and not line.startswith('*'):
            lineSplit = line.split(',')
            eid = lineSplit[0]
            elements[eid] = Element(eid, elem_type, [lineSplit[1],lineSplit[2]])

        elif line.startswith('*element') and 'rod' in line:
            bNode, bBeam = False, False
            bRod = True
            elem_type = 'rod'
        elif bRod and not line.startswith('*'):
            lineSplit = line.split(',')
            eid = lineSplit[0]
            elements[eid] = Element(eid, elem_type, [lineSplit[1],lineSplit[2]])

        # elif line.startswith('*'):
        #     bNode, bBeam, bRod = False, False, False

        else: 
            bNode, bBeam, bRod = False, False, False

    return nodes, elements


def writeVTKPoints(nodes):

    print(f'\nWriting VTKPoints')
    
    with open('nodes.vtu','w') as f:
        f.write(f'<?xml version="1.0"?>\n')
        f.write(f'<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
        f.write(f'<UnstructuredGrid>\n')

        no_of_nodes = len(nodes)

        f.write(f'<Piece NumberOfPoints="{no_of_nodes}" NumberOfCells="{no_of_nodes}">\n')
        
        # Point Data
        f.write(f'<PointData>\n')
        f.write(f'<Array type="Int32" Name="FEM_NODE_ID" format="ascii">\n')

        for nid in sorted(nodes.keys()):
            f.write(f' {nodes[nid].nid}')
		
        f.write(f'\n</Array>\n')
        f.write(f'</PointData>\n')

        # Points
        f.write(f'<Points>\n')
        f.write(f'<DataArray type="Float64" Name="Points" NumberOfComponents="3" format="ascii">\n')
        
        for nid in sorted(nodes.keys()):
            f.write(f' {nodes[nid].x} {nodes[nid].y} {nodes[nid].z}')

        f.write(f'\n</DataArray>\n')
        f.write(f'</Points>\n')

        # Cells
        f.write(f'<Cells>\n')
        f.write(f'<DataArray type="Int32" Name="connectivity" format="ascii">\n')

        for nid in sorted(nodes.keys()):
            f.write(f' {int(nodes[nid].nid)-1}')

        f.write(f'\n</DataArray>\n')
        f.write(f'<DataArray type="Int32" Name="offsets" format="ascii">\n')

        for nid in sorted(nodes.keys()):
            f.write(f' {nodes[nid].nid}')
        
        f.write(f'\n</DataArray>\n')
        f.write(f'<DataArray type="Int32" Name="types" format="ascii">\n')

        for i in range(len(nodes)):
            f.write(f' 1')

        f.write(f'\n</DataArray>\n')
        f.write(f'</Cells>\n')
        f.write(f'</Piece>\n')
        f.write(f'</UnstructuredGrid>\n')
        f.write(f'</VTKFile>\n')

        print(f'Number of nodes: {no_of_nodes}')
        print(f'Done writing nodes.vtu')


def writeVTKLines(nodes, elements):

    print(f'\nWriting VTKLines')
    
    with open('elements.vtu','w') as f:
        f.write(f'<?xml version="1.0"?>\n')
        f.write(f'<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
        f.write(f'<UnstructuredGrid>\n')

        no_of_nodes = len(nodes)
        no_of_cells = len(elements)

        f.write(f'<Piece NumberOfPoints="{no_of_nodes}" NumberOfCells="{no_of_cells}">\n')
        
        # Points
        f.write(f'<Points>\n')
        f.write(f'<DataArray type="Float64" Name="Points" NumberOfComponents="3" format="ascii">\n')
        
        for nid in sorted(nodes.keys()):
            f.write(f' {nodes[nid].x} {nodes[nid].y} {nodes[nid].z}')

        f.write(f'\n</DataArray>\n')
        f.write(f'</Points>\n')
        
        # Cells
        f.write(f'<Cells>\n')
        f.write(f'<DataArray type="Int32" Name="connectivity" format="ascii">\n')

        for eid in sorted(elements.keys()):
            n1 = int(elements[eid].attached_nodes[0]) - 1
            n2 = int(elements[eid].attached_nodes[1]) - 1
            f.write(f' {n1} {n2}')

        f.write(f'\n</DataArray>\n')
        f.write(f'<DataArray type="Int32" Name="offsets" format="ascii">\n')

        for eid in sorted(elements.keys()):
            f.write(f' {int(elements[eid].eid)*2}')
        
        f.write(f'\n</DataArray>\n')
        f.write(f'<DataArray type="Int32" Name="types" format="ascii">\n')

        for i in range(len(elements)):
            f.write(f' 3')

        f.write(f'\n</DataArray>\n')
        f.write(f'</Cells>\n')

        f.write(f'\n<CellData>\n')
        f.write(f'<Array type="Int32" Name="FEM_ELEMENT_ID" format="ascii">\n')

        for eid in sorted(elements.keys()):
            f.write(f' {elements[eid].eid}')
        
        f.write(f'\n</Array>\n')
        f.write(f'<Array type="String" Name="Element_Type" format="ascii">\n')

        for eid in sorted(elements.keys()):
            elem_type = elements[eid].elem_type
            for i in list(b'{elem_type}'):
                f.write(f' {i}')
            f.write(f' 0')

        f.write(f'\n</Array>\n')
        f.write(f'</CellData>\n')
        f.write(f'</Piece>\n')
        f.write(f'</UnstructuredGrid>\n')
        f.write(f'</VTKFile>\n')

        print(f'Number of elements: {no_of_cells}')
        print(f'Done writing elements.vtu')


if __name__ == '__main__':

    input_file = sys.argv[1]

    nodes, elements = parse_input_file(input_file)

    writeVTKPoints(nodes)
    
    writeVTKLines(nodes, elements)

    print('\nDone.')
import numpy as np

def writeVTKPoints(nodes, output_path):

    print(f'\nWriting VTKPoints')
    
    with open(output_path+'nodes.vtu','w') as f:
        f.write(f'<?xml version="1.0"?>\n')
        f.write(f'<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
        f.write(f'<UnstructuredGrid>\n')

        no_of_nodes = len(nodes)

        f.write(f'<Piece NumberOfPoints="{no_of_nodes}" NumberOfCells="{no_of_nodes}">\n')
        
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

        # Point Data
        f.write(f'<PointData>\n')
        f.write(f'<Array type="Int32" Name="FEM_NODE_ID" format="ascii">\n')

        for nid in sorted(nodes.keys()):
            f.write(f' {nodes[nid].nid}')
		
        f.write(f'\n</Array>\n')
        
        f.write(f'</PointData>\n')
        
        f.write(f'</Piece>\n')
        f.write(f'</UnstructuredGrid>\n')
        f.write(f'</VTKFile>\n')

        print(f' Number of Nodes: {no_of_nodes}')
        print(f' File written to {output_path}nodes.vtu')

def writeVTKLines(nodes, elements, output_path):

    print(f'\nWriting VTKLines')
    
    with open(output_path+'elements.vtu','w') as f:
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

        # Cell Data
        f.write(f'<CellData>\n')
        
        f.write(f'<Array type="Int32" Name="FEM_ELEMENT_ID" format="ascii">\n')
        for eid in sorted(elements.keys()):
            f.write(f' {elements[eid].eid}')
        f.write(f'\n</Array>\n')

        f.write(f'<Array type="String" Name="Element_Type" format="ascii">\n')
        for eid in sorted(elements.keys()):
            elem_type = elements[eid].elem_type
        
            ascii_list = [ord(c) for c in elem_type]

            for i in ascii_list:
                f.write(f' {i}')
            f.write(f' 0')
        f.write(f'\n</Array>\n')

        f.write(f'</CellData>\n')
  
        f.write(f'</Piece>\n')
        f.write(f'</UnstructuredGrid>\n')
        f.write(f'</VTKFile>\n')

        print(f' Number of Nodes: {no_of_nodes}')
        print(f' Number of Cells: {no_of_cells}')
        print(f' File written to {output_path}elements.vtu')
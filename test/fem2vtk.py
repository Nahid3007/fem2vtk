import numpy as np
import sys

from writeVTK import (
    writeVTKPoints,
    writeVTKLines,
    writeVTKPointSPC
)
from parse_input import parse_input_file

if __name__ == '__main__':

    print(f'\n************************************************************************')
    print(f'*                                                                      *')
    print(f'*                             f e m 2 v t k                            *')
    print(f'*                                                                      *')
    print(f'************************************************************************')

    input_file = sys.argv[1]
    output_path = sys.argv[2]

    nodes, elements, spc, load = parse_input_file(input_file)

    # writeVTKPoints(nodes,output_path)
    
    writeVTKLines(nodes, elements, spc, load, output_path)

    # writeVTKPointSPC(nodes, spc, output_path)

    # print('dof 1')
    # dof = 1
    # dof_dir = {}
    # for nid in sorted(spc.keys()):
    #     for i in range(len(spc[nid])):
    #         if dof in spc[nid][i].dof_array:
    #             dof_dir[nid] = np.array([1.,0.,0.])
    #         elif nid in dof_dir:
    #             continue
    #         else:
    #             dof_dir[nid] = np.array([0.,0.,0.])

    # print(dof_dir)
    # for key,value in dof_dir.items():
    #     print(' '.join(map(str, value)))

    # print('dof1')
    # dof = 1
    # dof_dir = {}
    # for nid in sorted(nodes.keys()):
    #     if not nid in spc:
    #         dof_dir[nid] = np.array([0.,0.,0.])
    #     elif nid in spc:
    #         for i in range(len(spc[nid])):
    #             if dof in spc[nid][i].dof_array:
    #                 dof_dir[nid] = np.array([1.,0.,0.])
    #             elif nid in dof_dir:
    #                 continue
    #             else:
    #                 dof_dir[nid] = np.array([0.,0.,0.])        

    # print(dof_dir)

    # for nid in sorted(nodes.keys()):
    #     if not nid in load:
    #         print(nid,'0. 0. 0.')
    #     if nid in load and load[nid].dof == '1':
    #         direction = np.array([1.,0.,0.])*float(load[nid].value)
            
    #         print(nid, direction)

    print('\nDone.')
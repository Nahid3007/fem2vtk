import numpy as np
import sys

from writeVTK import (
    writeVTKPoints,
    writeVTKLines
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

    nodes, elements = parse_input_file(input_file)

    writeVTKPoints(nodes,output_path)
    
    writeVTKLines(nodes, elements, output_path)

    print('\nDone.')
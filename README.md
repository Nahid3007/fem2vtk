# Overview
A python tool to convert the `2D_Planar_Truss_Beam_FEA` FE model to a VTK model for visualizing it in ParaView.

This tool creates for the input file a `nodes.vtu` and a `elements.vtu` file which can be loaded in ParaView.

At the moment only the FE nodes and elements can be visualized. Loads and boundary conditions will be also possible to be visualized in a later version.

# Usage

The main file of this tool is `fem2vtk.py`. 

Run in terminal:

```
python fem2vtk.py [input .*txt file] [output path]
```

# Example Output in ParaView

The FE nodes and element IDs can be visualized:

![nodes_element_ids](/test/vtk_output/fe_elements_nodes_id.png "nodes and element id visualization")

The FE element types can also be visualized:

![nodes_element_ids](/test/vtk_output/fe_element_types.png "nodes and element id visualization")
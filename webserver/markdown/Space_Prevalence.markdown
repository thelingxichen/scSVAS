##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

In Oviz-SingleCell platform, we develop a readily available web interface "Space Prevalence"  for interactive and real-time visualization of clonal dynamics across multiple samples.

"Space Prevalence'' enables users to create the recurrent event visualization just in following steps:

  + With subclone tree file `clonal_edges.csv` and clonal prevelance file `clonal_prev.csv` as input, run `scSVAS space.py` to get the space tree results `space_edges.csv`.
  + Open https://sc.deepomics.org/demo-project/analyses/space\_prevalence in Google browser, and upload files `clonal_edges.csv`, `clonal_prev.csv`, and `space_edges.csv`.


"Space Prevalence" displays the clonal tree, lesion tree, and the space prevalence across subclones and lesions. If the mouse hovers over the node in lineage tree and sankey diagram, an interactive tooltip carried its vital information will appear. 

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/scSVAS_Input_Format.markdown).


# Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over an component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "Space Prevalence'' application and their tooltipping and highlighting interactions are as follows:
    + Subclone lineage tree node </br>
      The tooltip will display the name of subclone/lesion, the clone prevalence at each timepoint if available. The corresponding subclone/lesion in lineage tree, fishplot, and sankey plot will be highlighted. 
    + Lesion lineage tree node </br>
      The tooltip will display the lesion node name, distance to the root node, clonal frequency, the number of cells in the subclone. The corresponding lesion in sankey plot will be highlighted. 
    + Lesion lineage tree branch </br>
      The tooltip will display the parent node name, child node name, and the distance of branch. The corresponding branch and nodes will be highlighted in sankey plot and clonal prevalence matrix.
    + Sankey plot node </br>
      The tooltip will display the subclone/lesion node name. The corresponding subclone/lesion in lineage tree will be highlighted. 
    + Sankey plot link </br>
      The tooltip will display the subclone node name, lesion node name, and the clona prevalence across them. The corresponding branch and nodes will be highlighted in lineage tree and clonal prevalence matrix.
    + Clonal prevalence matrix tile </br>
      The tooltip will display the subclone node name, lesion node name, and the clona prevalence across them. The corresponding branch and nodes will be highlighted in lineage tree and sankey plot.

# Editor Functionalities

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings 
    + Lineage Tree

      + Show subclone name </br>
        Users can decide show clone name or not.
        
      + Type of lineage tree </br>
         Users can change the type of lineage tree.

      + Show low prevelance clone </br>

         Users can decide whether to show low prevalence clone or not.

      + Low prevalence threshold </br>

         Users can change the value of low prevalence threshold, default it 0.01.


# Version

v1.0.0 (2020-12-19)

# Developer


Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

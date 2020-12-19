##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

As previously mentioned, many studies have observed that intra-tumor heterogeneity (ITH) is one of the principal causes of cancer therapy-resistant, tumor recurrence, and deaths. Over the past decades, researchers are interested in studying the clonal dynamics from multiple timepoint. For example, the time lineage between subclones before and after therapeutic intervention. 

Herein, in scSVAS platform, we develop a readily available web interface "Time Lineage''  for interactive and real-time visualization of clonal lineage across time for scDNA-seq data.

"Time Lineage'' enables users to create the time lineage visualization just in following steps:

   + Open https://sc.deepomics.org/demo-project/analyses/time\_lineage in Google browser, and upload the customized clonal tree file `clonal_edges.csv` and clonal prevalence file `clonal_prev.csv`.
     

"Time Lineage" is composed of fishplot, lineage tree, and cellular ensemble. As previously mentioned, the lineage tree exhibits the evolutionary relationship between tumor subclones. Users can choose different tree shapes from "topdown normal", "circular normal", and "circular acute". Fishplot conceptually manifests the proportion of tumor subclones at different tumorigenesis stages along time. We use the bezier curve to fit the trend of subclones over time. Two distinct head shapes ("bullet'' and "onion'') are offered. The cellular ensemble is an abstract aesthetic presenting the tumor's cellular prevalence at a certain point in time. If the mouse hovers over the subclone in fishplot, lineage tree, and cellular ensemble, an interactive tooltip carried its vital information will appear. 

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/scSVAS_Input_Format.markdown).


# Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "Time Lineage'' application and their tooltipping and highlighting interactions are as follows:
    + Subclone in fishplot </br>
      The tooltip will display the name of subclone, the clone prevalence at each timepoint. The corresponding subclone in fishplot and lineage tree will be highlighted. 
    + Lineage tree node </br>
      The tooltip will display the subclone node name, distance to the root node, clonal frequency, the number of cells in the subclone. The corresponding subclone in fishplot and cellular ensemble will be highlighted. 
    + Lineage tree branch </br>
      The tooltip will display the parent node name, child node name, and the distance of branch. The corresponding branch and nodes will be highlighted in fishplot and cellular ensemble.
    + Cellular ensemble </br>
      The tooltip will display the name and prevalence of the clone. The corresponding clones will be highlighted in lineage tree and fishplot.

# Editor Functionalities

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings 
    + Fishplot
      + Show clone name </br>
         Users can decide show clone name or not.
      + X-axis title of fishplot </br>
         Users can change the title for x-axis, default is "Time Point''.
      + Y-axis title of fishplot </br>
         Users can change the title for y-axis, default is "Clonal Prevalence''.
      + Vertical layout of subclones </br>
         Users can select the vertical layout of subclones from "stack'', "space'', and "center''.
      + Head shape of fishplot </br>
         Users can select the shape of clone head from "bullet'' or "onion''.
      + Width of fishplot </br>
         Users can set the width of fishplot.
      + Height of fishplot </br>
         Users can set the height of fishplot.
    + Lineage Tree
      + Title of lineage tree </br>
         Users can change the title for lineage tree. default is "Clonal Lineage Tree''. 
      + Type of lineage tree </br>
         Users can change the type of lineage tree.
    + Cellular Ensemble 
      + Number of cells </br>
         Users can adjust the number of cells in cellular ensemble presentation.
      + Radius of cellular aggregation </br>
         Users can adjust the radius of cellular ensemble presentation.
  + Color Palettes </br>
    Users can customize color palettes for subclones .


# Version

v1.0.0 (2020-12-16)

# Developer


Mr. Chaohui Li ([GitHub](https://github.com/Eric0627))

# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

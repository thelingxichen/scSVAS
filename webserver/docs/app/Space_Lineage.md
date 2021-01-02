# Space Lineage
> For quick view of visualization application, please try the demo files in the "Editor" sidebar `Demo File Sets`. Description of demo files is available in [demo data](https://docsc.deepomics.org/#/data/Demo_Data).

> The uploaded input file must match the required format, please check the general accepted [input file format](https://docsc.deepomics.org/#/data/Input_Format). 

## Introduction

In scSVAS platform, we develop a readily available web interface "Space Lineage"  for interactive and real-time visualization of clonal dynamics across multiple samples.

"Space Lineage'' enables users to create the clonal dynamics visualization just in following steps:

  + Open https://sc.deepomics.org/demo-project/analyses/space_prevalence in Google browser, and upload filessubclone tree file `clonal_edges.csv`, clonal prevelance file `clonal_prev.csv`.
  + *Optional* With subclone tree file `clonal_edges.csv` and clonal prevelance file `clonal_prev.csv` as input, run `scSVAS space.py` to get the space tree results `space_edges.csv`, then upload it.
  + *Optional* Users can also upload customized lesion images.


"Space Lineage" displays the clonal dynamics across subclones and lesions. If the mouse hovers over the node in lineage tree, an interactive tooltip carried its vital information will appear. 

## Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over an component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "Space Prevalence'' application and their tooltipping and highlighting interactions are as follows:
    + Subclone lineage tree node </br>
      The tooltip will display the name of subclone/lesion, the clone prevalence at each timepoint if available. The corresponding subclone/lesion in lineage tree, fishplot will be highlighted. 
    + Lesion lineage tree node </br>
      The tooltip will display the lesion node name, distance to the root node, clonal frequency, the number of cells in the subclone. The corresponding lesion in other lineage tree will be highlighted. 
    + Lesion lineage tree branch </br>
      The tooltip will display the parent node name, child node name, and the distance of branch. The corresponding branch and nodes will be highlighted in other lineage tree.
  + Anatomy image pointer </br>
  For each lesion, we provide an image pointer. Users can right click the image pointer to active and deactive it. When the image pointer is activated, user can drag the pointer to anywhere they want in the anatomy image.

## Editor Functionalities

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
  + Antomy type </br>
  Users can select different antomy images.

## Version

v1.0.0 (2020-12-19)

## Developer


Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Acknowledgement
The anatomy images are designed by [Freepik](https://www.freepik.com/) and [macrovector / Freepik] (https://www.freepik.com/), we acknowledge for the free license. 

## Updates

### v1.0.0

   - full functionalities implemented.

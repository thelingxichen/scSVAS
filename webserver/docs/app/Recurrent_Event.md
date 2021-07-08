# Recurrent Event
> For quick view of visualization application, please try the demo files in the "Editor" sidebar `Demo File Sets`. Description of demo files is available in [demo data](https://docsc.deepomics.org/#/data/Demo_Data).

> The uploaded input file must match the required format, please check the general accepted [input file format](https://docsc.deepomics.org/#/data/Input_Format). 

## Introduction

In scSVAS platform, we also develop a readily available web interface "Recurrent Event''  for interactive and real-time visualization of CNV profiles across multiple samples for scDNA-seq data.

"Recurrent Event'' enables users to create the recurrent event visualization just in following steps:

  + With group cnv profile file of multiple samples `*_hcluster_cnv.csv` as input, run `scSVAS recurrent.py` to get the recurrent event results `*_recurrent.json`.
  + Open https://sc.deepomics.org/demo-project/analyses/recurrent_event in Google browser, and upload the recurrent event results `*_recurrent.json`.
  + *Optional* Users can also upload the predefined gene list `target_anno.tsv` to only display the CNV shift of targeted gene.


"Recurrent Event" displays the CNV stairsteps of all samples. The gene box shows the recurrent genes.  If the mouse hovers over the subclone in stairstep and gene box, an interactive tooltip carried its vital information will appear. 


## Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "Clonal Lineage'' application and their tooltipping and highlighting interactions are as follows:
    + Stairstep </br>
        The tooltipping and highlighting interactions are the same with stairstep in "Ploidy Stairstep'' application. </br>
    + Gene box </br>
        The corresponding gene box, cytoband, genomic position on stairstep will be highlited.
    + MsigDB gene sets </br>
        The tooltip will display the name of selected MsigDB gene sets. The corresponding gene box, cytoband, genomic position on stairstep will be highlighted.
    + Self-defined gene set. </br>
        The tooltip will display the name of self-defined gene set. The corresponding gene box, cytoband, genomic position on stairstep will be highlighted.
    + Packed gene box, External link on gene, External link on MsigDB pathway </br>
      The interaction are descripted in "CNV Clonal Lineage'' application.

## Editor Functionalities
The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
    Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings 
    + Maximum genes to display on gene box </br>
        User can adjust the maximum number of genes to display on gene box, if the number of genes in one box is surpass the threshold, genes will be hided.   
    + Gap between samples </br>
        User can adjust the gap between samples.
    + Width of stairstep </br>
        User can adjust the width of stairstep.
    + Height of stairstep </br>
        User can adjust the height of stairstep.
  + Gene sets selection </br>
    User can select which gene set to display.
  + Sample and subclone selection </br>
    User can select which sample and subclone to display.


## Version

v1.0.0 (2020-12-17)

## Developer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

Mr. Lirui Kang  ([GitHub](https://github.com/RKLho))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

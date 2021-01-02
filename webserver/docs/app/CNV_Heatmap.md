# CNV Heatmap
> For quick view of visualization application, please try the demo files in the "Editor" sidebar `Demo File Sets`. Description of demo files is available in [demo data](https://docsc.deepomics.org/#/data/Demo_Data).

> The uploaded input file must match the required format, please check the general accepted [input file format](https://docsc.deepomics.org/#/data/Input_Format). 

## Introduction

The web interface "CNV Heatmap'' is extension version of "CNV View'', by supporting extra functionalities including genome region zooming, local region search, and local region annotation.  

"CNV Heatmap'' enables users to create the cnv heatmap of single cell CNV profiles in following straightforward steps as follow:

+ Open https://sc.deepomics.org/demo-project/analyses/heatmap in Google browser, and upload cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv`.
+  *Optional* With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` as inputs, users can run `scSVAS` to get the cutted dendrogram of single cells, and upload it to compress the heatmap plot.
+  *Optional* Users can also upload a customized bed file to check the CNV heatmap in local region.

  

Users can get a single cell CNV landscape view of scDNA-seq data. With single cells as rows and genomic regions as columns, the cell CNV heatmap exhibits the copy number of a specific single-cell across the entire genome. The cell meta heat map will be displayed on the left if users provide single-cell meta information. In addition, there is a genome zoom slider located at the bottom of CNV heatmap. Users can drag the slider to zoom in and out on the genome region. Users can also search for a local genome region in "Editor General Settings". If the local genome region is less than 5M, an annotation layer including "Repeat track'' and "Gene track'' will be displayed. If the mouse hovers over cell CNV/meta heatmap, repeats, and genes, an interactive tooltip carried its vital information will appear. 


## Interactions


   + Download </br>
     An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
   + Tooltips and Highlights </br>
     When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are serveral major components in the "CNV Heatmap'' application and their tooltipping and highlighting interactions are as follows:
     + Cell CNV Heatmap, Cell Meta Heatmap, Cutted Dendrogram Node, Cutted Dendrogram Branch </br>
       Tooltipping and highlighting interactions are the same with "CNV View'' visualization.
     + Gene Track </br>
       Tooltip will display the transcript name and gene body interval for covered gene. Tooltip will display exon number and exon interval for covered gene exon. 
     + Repeat Track </br>
       Tooltip will display the names of repeat class, repeat element, repeat family, genome position, and strand information of a selected repeat.
   + Zoom Slider Button </br>
       Users can click this button to active genome zoom slider mode.
   + Bed Region Button </br>
       Users can click this button to active bed region mode.
   + Search Bed Button </br>
       Users can click this button to active search bed mode.
   + Genome Zoom Slider </br>
       Users can adjust and drag the slider along genome region to zoom in and out.
   + Local Region Zoom Slider </br>
       Users can adjust and drag the slider along local region to zoom in and out.
   + Pages </br>
       Users can click 'Prev' or 'Next' to switch uploaded local bed regions.
   + Dendrogram Zooming </br>
       Dendrogram zooming is the same with "CNV View'' visualization.

## Editor Functionalities

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
    Demo file sets and files Functionalities are the same with "CNV Heatmap'' visualization.
  + General Settings
    + Auto load heatmap, NA cases, Reorder cells by </br>
      Auto load heatmap, NA cases, Reorder cells by functionalities are the same with "CNV View'' visualization.
    + Mode </br>
      Users can switch from "Zoom Slider'', "Bed Region'', or "Search Bed'' modes.
    + Select categorical meta label, Layout Settings </br>
      Select categorical meta label, Layout Settings are the same with "CNV View'' visualization.
  + Search (Available in "Bed Region" and "Search Bed'' mode)
    + Search local genome region </br>
      Users can enter a local genome region to display, e.g. chr17:5,565,097-9,590,863. This functionality is only effective when search bed mode is activated.
    + Bed region </br>
      Users can select the local genome region in uploaded bed file to display. This functionality is only effective when bed region mode is activated.
  + Genome Browser (Available in "Bed Region" and "Search Bed'' mode)
    + Annotation Panel 
      + Display strand </br>
        Users can choose to display postive, negative, or both strands on gene track.
      + Show repeat track </br>
        Users can choose to display the repeat track or not.
      + Merge gene tracks </br>
        Users can choose to merge gene track to get condensed displaying.
      + Display gene name </br>
        Users can choose to display the gene name or transcript name in gene track.
      + Display all genes </br>
        Users can choose to display all genes on the gene track. 
    + Genes </br>
      This section lists all genes in current local region, users can decide to display which transcript of one gene.
  + Color palettes </br>
    Users can customize color palettes for available categorical meta labels and continuous meta labels.


## Version

v1.0.0 (2020-12-16)

## Developer

Mr. Yuhao Qing ([GitHub](https://github.com/Q-Y-H))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

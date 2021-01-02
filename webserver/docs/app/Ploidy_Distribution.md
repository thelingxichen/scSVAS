# Ploidy Distribution

## Introduction

Over the past decade, the single cell DNA CNV calling algorithms usually model the relationship between sequenced read count and copy number employing Poisson distribution with mappability, GC content, scale factor as confounding factor. 

In cancer datasets, the copy number of different regions may encounter dramatic gain or loss. For single-cell DNA cancer data,  ploidy distribution can intuitively display the tumor intra-heterogeneity.

To address this concern, in scSVAS platform, we develop a readily available web interface "Ploidy Distribution''  for interactive and real-time visualization of ploidy density plot for scDNA-seq data.

"Ploidy Distribution'' enables users to create the ploidy density plot just in one simple step as follow:

  + Open https://sc.deepomics.org/demo-project/analyses/ploidy_distribution in Google browser, and upload cnv profile file `*_cnv.csv` and predefined meta file `*_meta.csv`.
  + *Optional* With cnv profile file `*_cnv.csv` and predefined meta file `*_meta.csv` as inputs, users may also run `scSVAS` to get the subclone cluster result in `*_meta_scsvas.csv` first.

Then, you may get a matrix of the ploidy density plot of scDNA-seq data. The columns will list all categorical meta labels available in uploaded file `*_meta_scsvas.csv` by default. The first row displays the ploidy distribution of total single cells, just like the way for bulk sequencing. The second line exhibits the ploidy distribution of all subgroups for specific categorical meta labels in an aggregate form. Then, the following rows will list the ploidy distribution of all available subsets individually.
Users can decide to display or hide these meta labels and subsets in "Editor-Select categorical meta label''. 
Users can choose to set the ploidy unit as cell mean ploidy or bin ploidy in "Editor-Mode''.
If the mouse hovers over the density plot, an interactive tooltip carried its vital information will appear. 

## Input & Demo File

The uploaded file must match the *required* format, please check the general accepted [input file format](data/input_format). Several demo files descripted in [demo data](data/demo_data) are provided in the "Editor" sidebar. 


## Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are two major types of component in the "Ploidy Distribution'' application and their tooltipping and highlighting interactions are as follows:
      + Distribution plot </br>
         The tooltip will display the current ploidy value and the density of that ploidy.
      + Aggregate subgroup distribution plot </br>
         The tooltip will display the current ploidy value and the density of that ploidy on each subgroups. 

## Editor Functionalities
The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.


  + Demo File Sets, Files </br>
    Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings </br>
    + Mode </br>
      Users can select to display "cell mean ploidy" or "bin ploidy" mode.
    + Get log10-scale of count? </br>
        Users can choose whether applies log10-scale on density count.
    + Set total number of intervals (bins) </br>
        Users can set the total number of bins, the bin is the block that you use to combine values before getting the frequency.
    + Only get the plot with 10+ data? </br>
        Users can decide whether filter subgroup plot with less than 10 data points.
    + Distribution plot height </br>
        Users can adjust the height of each distribution plot.
    + Distribution plot width </br>
        Users can adjust the width of each distribution plot.
    + Maximum value of ploidy </br>
        Users can adjust the maximum value of ploidy in x-axis.

  + Select categorical meta label </br>
    User can choose which categorical meta labels to display.

  + Color Palettes </br>
    Users can customize color palettes for available categorical meta labels.

## Version

v1.0.0 (2020-12-16)

## Developer

Mr. Chaohui Li ([GitHub](https://github.com/Eric0627))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functions implemented.

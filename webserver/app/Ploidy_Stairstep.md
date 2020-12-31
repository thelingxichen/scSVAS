# Ploidy Stairstep

## Introduction
As previously mentioned, for single-cell DNA cancer data, the ploidy distribution can intuitively show tumor heterogeneity. The ploidy line plot along the chromosomes can also visually show the heterogeneity between tumor subclones by combining genomic coordinates.
By collapsing the single cells in the same tumor subclones into one observation, we can infer the pseudo-bulk ploidy of each subclone. Since cancer CNV ploidy line alters along chromosomes, we call it the "stairstep plot''.

In scSVAS platform, we develop a readily available web interface "Ploidy Stairstep''  for interactive and real-time visualization of ploidy stairstep plot for scDNA-seq data.

"Ploidy Stairstep'' enables users to create the ploidy stairstep plot just in one simple step as follow:

+ Open https://sc.deepomics.org/demo-project/analyses/ploidy_stairstep in Google browser, and upload cnv profile file `*_cnv.csv` and predefined meta file `*_meta.csv`.
+ *Optional* With cnv profile file `*_cnv.csv` and predefined meta file `*_meta.csv` as inputs, users may also run `scSVAS` to get the subclone cluster result in `*_meta_scsvas.csv` first.

Then, you may get a matrix of the ploidy stairstep plot of scDNA-seq data. The columns will list all categorical meta labels available in uploaded file `*_meta_scsvas.csv` by default. The first row displays the ploidy stairstep of pseudo-bulk profiles. The second line exhibits the ploidy stairstep of all subgroups for specific categorical meta labels in an aggregate form. Then, the following rows will list the ploidy stairstep of all available subsets individually.
Users can decide to display or hide these meta labels and subsets in "Editor-Select categorical meta label''. 
If the mouse hovers over the stairstep plot, an interactive tooltip carried its vital information will appear. 

## Input & Demo File

The uploaded file must match the *required* format, please check the general accepted [input file format](data/input_format). Several demo files descripted in [demo data](data/demo_data) are provided in the "Editor" sidebar. 


## Interactions

  + Download </br>
     An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are two major types of component in the "Ploidy Stairstep'' application and their tooltipping and highlighting interactions are as follows:
    + Stairstep plot </br>
      The tooltip will display the genome position and the average copy number.
    + Aggregate subgroup distribution plot </br>
      The tooltip will display the genome position and the average copy number for each subgroup respectively.

## Editor Functionalities

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings 
    + Maximum CN value </br>
       Users can adjust the maximum CN value of y-axis.
    + Stairstep plot height </br>
       Users can adjust the height of each stairstep plot.
    + Stairstep plot width </br>
       Users can adjust the width of each stairstep plot.
    + Stairstep plot line width </br>
       Users can adjust the line width of each stairstep plot.
  + Select categorical meta label </br>
    Users can choose which categorical meta labels to display.
  + Color Palettes </br>
    Users can customize color palettes for available categorical labels.
           
           

## Version

v1.0.0 (2020-12-16)

## Developer

Mr. Ruikang Li ([GitHub](https://github.com/RKLho))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - initial functions implemented.

### v1.1.0

   - fix bug of event confidence. 
   - allow interface switch between bed file and cnv file.


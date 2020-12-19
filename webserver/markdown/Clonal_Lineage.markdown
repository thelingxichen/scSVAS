##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

Many studies have observed that intra-tumor heterogeneity (ITH) is one of the principal causes of cancer therapy-resistant, tumor recurrence, and deaths. An accurate understanding of the subclone structure and evolutionary history benefits precise treatments for individual patients. Over the past decades tools utilize SNV, CNV information, or combine these two phenotype markers to infer the phylogeny tree. There are tools customized for different sequencing protocols, including multi-region, single-cell.

Unlike the traditional phylogenetic trees as visualized in ''Cell Phylogeny'', we focus on the clonal lineage tree, which more accurately reflects the process of tumor evolution. In a clonal lineage tree, ancestors and offspring tumor cells/subpopulations can coexist at the same time point; therefore, the internal node can be the single cell/subpopulation we observed. The tumor accumulates mutations over evolution time, and child tumor cell/subpopulation carries parental and newly-acquired aberrations. The tree linkage between parent and child node is more about asymmetric subset connections than symmetric distance. 

There are several tools to visualize the clonal lineage tree with subclones as tree nodes. For example, fishplot presents clonal dynamics over time; sphere of cells present clonal subpopulations of a sample, and annotated node-based and branch-based trees present clonal relationships and seeding patterns between samples. Nevertheless, there is no good tool to display the acquired mutations along time.


To address this concern, in scSVAS platform, we develop a readily available web interface ''Clonal Lineage''  for interactive and real-time visualization of clonal lineage and associated CNV across time for scDNA-seq data.


''Clonal Lineage'' enables users to create the clonal lineage visualization just in following steps:

+ With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` and targeted gene list as inputs, run `scSVAS` to get the build clonal lineage results `*_evo.json`.
+  Open https://sc.deepomics.org/demo-project/analyses/clonal\_lineage in Google browser, and upload the customized clonal tree file `*_evo.json`.
+ *Optional*  Users can also upload the predefined gene list `target_anno.tsv` to only display the CNV shift of targeted gene.

''CNV: Clonal Lineage" is composed of lineage tree, group CNV heatmap, cellular ensemble, lineage tree branch, stairstep, and gene box. The lineage tree exhibits the evolutionary relationship between tumor subclones. Users can choose different tree shapes from ''topdown normal", ''circular normal",  ''circular acute", and ''fishplot''. Fishplot conceptually manifests the proportion of tumor subclones at different tumorigenesis stages along time. We use the bezier curve to fit the trend of subclones over time. Two distinct head shapes (''bullet'' and ''onion'') are offered. The cellular ensemble is an abstract aesthetic presenting the tumor's cellular prevalence at a certain point in time. The group CNV heatmap display the averaged copy number profiles of subclones. The lineage tree branch displays the number of gain and loss regions for each tree branch. The stairstep and gene box depicts the detailed CNV shift from the parent node to the child node. Users can click the lineage tree branch to check the different CNV shift. If the mouse hovers over lineage tree, group CNV heatmap, cellular ensemble, lineage tree branch, stairstep, and gene box, an interactive tooltip carried its vital information will appear. 

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/scSVAS_Input_Format.markdown).

# Interactions


   + Download </br>
     An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
   + Tooltips and Highlights </br>
          When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "Clonal Lineage'' application and their tooltipping and highlighting interactions are as follows:
+ Lineage tree node </br>
       The tooltip will display the subclone node name, distance to the root node, clonal frequency, the number of cells in the subclone. The corresponding node in aggregate subclone CNV heatmap, lineage tree branch will be highlighted.
      + Lineage tree branch </br>
       The tooltip will display the parent node name, child node name, and the distance of branch. The corresponding branch will be highlighted.
      + Subclone in fishplot </br>
       The tooltip will display the name of subclone, the clone prevalence at each timepoint. The corresponding subclone in fishplot, lineage tree, and aggregate subclone CNV heatmap will be highlighted. 
      + Aggregate subclone CNV heatmap </br>
       The tooltipping and highlighting interactions are the same with aggregate subgroup CNV heatmap in "CNV View'' application.
      + Cellular ensemble </br>
       The tooltip will display the name and prevalence of the clone. The corresponding clones will be highlighted in lineage tree or fishplot.
      + Subclone branch </br>
       The corresponding branch will be highlighted in lineage tree or fishplot.
      + CNV shift Stairstep </br>
       The tooltipping and highlighting interactions are the same with stairstep in "Ploidy Stairstep'' application. 
      + Gene box </br>
       The corresponding gene box, cytoband, genomic position on stairstep will be highlighted.
      + MsigDB Pathway </br>
       The tooltip will display the name of selected MsigDB pathway. The corresponding gene box, cytoband, genomic position on stairstep will be highlighted.
      + Self-defined gene set. </br>
       The tooltip will display the name of self-defined gene set. The corresponding gene box, cytoband, genomic position on stairstep will be highlighted.
      
   + Subclone branch </br>
           Users can display the CNV shifts of a particular subclone branch by clicking it.
   + Packed gene box </br>
           Users can click packed gene box to look the whole list of genes.
   + External link on gene </br>
           Users can jump to the GeneCards webpage by clicking on the gene listed in the gene box.
   + External link on MsigDB pathway </br>
           Users can jump to the MsigDB pathway webpage by clicking on the gene set icon.

# Editor Functionalities
The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.


   + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with "CNV View'' visualization.
   + General Settings 
      + Basic 
         + Select subclone label </br>
         Users can select which subclone label to display.
         + Lineage Tree/Fishplot
            + Type of lineage tree </br>
               Users can select the type of lineage tree from "topdown normal'', "circular normal'', "circular acute'', or "fishplot''.
            + Vertical layout of subclones </br>
               Users can select the vertical layout of subclones from "stack'', "space'', and "center''.
            + Head shape of fishplot </br>
               Users can select the shape of clone head from "bullet'' or "onion''.
         + Gene Box
            + CNV shift shreshold </br>
               Users can adjust the CNV shift threshold. Only genes surpass this threshold will be displayed on gene box.
            + Maximum genes to display on gene box </br>
               Users can adjust the maximum genes to display on gene box.
            + Aggregate gene sets </br>
               Users can choose to aggregate the gene sets icon or not.
   + Layout Settings
      + Basic 
         + Height of lineage tree/fishplot/aggregate subclone CNV heatmap </br>
           Users can set the height of lineage tree/fishplot/aggregate subclone CNV heatmap.
         + Margin between aggregate subclone CNV heatmap and subclone branch </br>
           Users can adjust the margin between aggregate subclone CNV heatmap and subclone branch.
         + Margin between subclone branch and CNV shift stairstep </br>
           Users can adjust the margin between subclone branch and CNV shift stairstep.
         + Margin between CNV shift stairstep and legend </br>
           Users can adjust the margin between CNV shift stairstep and legend.

      + Aggregate subclone CNV heatmap </br>
        Aggregate subclone CNV heatmap functionalities are the same with CNV heatmap in "CNV View'' visualization.
      + Subclone branch
         + Width of subclone branch </br>
           Users can adjust the width of subclone branch.
         + Height of subclone branch </br>
           Users can adust the height of subclone branch.
      + CNV shift stairstep 
         + Maximum CN value </br>
           Users can adjust the maximum CN value in y-axis.
         + Width of stairstep </br>
           Users can adjust the width of stairstep.
         + Height of stairstep </br>
           Users can adjust the height of stairstep.
         + Width of stairstep line </br>
           Users can adjust the width of line in stairstep plot .
         + Margin between parent stairstep and child stairstep </br>
           Users can adjust the margin between parent stairstep and child stairstep.
      + Gene Box
         + Width of gene box </br>
           Users can adjust the width of gene box.
         + Column margin between gene boxes </br>
           Users can adjust the margin between column margin between gene boxes.

   + Gene sets selection </br>
         Users can select the gene set to display by clicking on the checkbox.
   + Color Palettes </br>
         Users can customize color palettes for subclones, amp/loss, and gene sets.

# Version

v1.0.0 (2020-12-16)

# Developer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

Mr. Yuhao Qing ([GitHub](https://github.com/Q-Y-H))

Mr. Ruikang Li ([GitHub](https://github.com/RKLho))

Mr. Chaohui Li ([GitHub](https://github.com/Eric0627))


# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

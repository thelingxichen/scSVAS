##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

Many studies have observed that intra-tumor heterogeneity (ITH) is one of the principal causes of cancer therapy-resistant, tumor recurrence, and deaths. An accurate understanding of the subclone structure and evolutionary history benefits precise treatments for individual patients. Over the past decades tools utilize SNV, CNV information, or combine these two phenotype markers to infer the phylogeny tree. There are tools customized for different sequencing protocols, including multi-region, single-cell.

Unlike the traditional phylogenetic trees as visualized in ''CNV Cell Phylogeny'', we focus on the clonal lineage tree, which more accurately reflects the process of tumor evolution. In a clonal lineage tree, ancestors and offspring tumor cells/subpopulations can coexist at the same time point; therefore, the internal node can be the single cell/subpopulation we observed. The tumor accumulates mutations over evolution time, and child tumor cell/subpopulation carries parental and newly-acquired aberrations. The tree linkage between parent and child node is more about asymmetric subset connections than symmetric distance. 

There are several tools to visualize the clonal lineage tree with subclones as tree nodes. For example, fishplot presents clonal dynamics over time; sphere of cells present clonal subpopulations of a sample, and annotated node-based and branch-based trees present clonal relationships and seeding patterns between samples. Nevertheless, there is no good tool to display the acquired mutations along time.


To address this concern, in scSVAS platform, we develop a readily available web interface ''CNV Clonal Lineage''  for interactive and real-time visualization of clonal lineage and associated CNV across time for scDNA-seq data.


''CNV Clonal Lineage'' enables users to create the clonal lineage visualization just in following steps:

+ With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` and targeted gene list as inputs, run `scSVAS` to get the build clonal lineage results `*_evo.json`.
+  Open https://sc.deepomics.org/demo-project/analyses/clonal\_lineage in Google browser, and upload the customized clonal tree file `*_evo.json`.
+ *Optional*  Users can also upload the predefined gene list `target_anno.tsv` to only display the CNV shift of targeted gene.

''CNV: Clonal Lineage" is composed of lineage tree, group CNV heatmap, cellular ensemble, lineage tree branch, stairstep, and gene box. The lineage tree exhibits the evolutionary relationship between tumor subclones. Users can choose different tree shapes from ''topdown normal", ''circular normal",  ''circular acute", and ''fishplot''. Fishplot conceptually manifests the proportion of tumor subclones at different tumorigenesis stages along time. We use the bezier curve to fit the trend of subclones over time. Two distinct head shapes (''bullet'' and ''onion'') are offered. The cellular ensemble is an abstract aesthetic presenting the tumor's cellular prevalence at a certain point in time. The group CNV heatmap display the averaged copy number profiles of subclones. The lineage tree branch displays the number of gain and loss regions for each tree branch. The stairstep and gene box depicts the detailed CNV shift from the parent node to the child node. Users can click the lineage tree branch to check the different CNV shift. If the mouse hovers over lineage tree, group CNV heatmap, cellular ensemble, lineage tree branch, stairstep, and gene box, an interactive tooltip carried its vital information will appear. 

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/CNV_input_format.markdown).

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

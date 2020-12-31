# Embedding Map

## Introduction
High-dimensional data could be challenging to visualize. Reducing data into two dimensions is essential for representing the inherent structure of the data. Several supervised and unsupervised embedding methods have been proposed and widely applied to multiple disciplines in the past two decades. For example, linear dimension reduction tools like Principal Component Analysis (PCA), Independent Component Analysis (ICA), Non-negative Matrix Factorization (NMF) specify distinct rubrics to conduct linear projection of data. Furthermore, to tackle non-linear data structure, t-distributed Stochastic Neighbor Embedding (t-SNE), Uniform Manifold Approximation and Projection (UMAP), and Potential of Heat-diffusion for Affinity-based Trajectory Embedding (PHATE) are developed. We also build a Matrix Factorization based Deep neural network (DeepMF), which is compatible with both linear and non-linear embedding.

In scSVAS platform, we build a readily available web interface "Embedding Map''  for interactive and real-time visualization of scDNA-seq data."

With the advance of sing-cell DNA sequencing techniques, the CNV data of tens of thousands of cells could be profiled at the same time. In terms of large-scale data, conventional 2D scatter plots may disguise essential information. "Embedding Map" defeats this overplotting obstacle utilizing hexagonal binning, which also has benefits on time and memory complexity.


"Embedding Map'' enables users to create the 2D embedding plot in two straightforward steps as follow:



 + With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` and targeted gene list as inputs, run `scSVAS` to get the 2D embedding (PCA, ICA, TSNE, UMAP, PHATE, and DeepMF) results `*_meta_scsvas.csv` and targeted gene cnv profiles `*_gene_cnv.csv`.
 + Open https://sc.deepomics.org/demo-project/analyses/embedding_map in Google browser, and upload files `*_meta_scsvas.csv` and `*_gene_cnv.csv`.
   
   

Then, you may get a matrix of 2D representations of scDNA-seq data. The column will list all embedding techniques available in uploaded file `*_meta_scsvas.csv` by default. Users can decide to display or hide these embedding methods in "Editor-General Settings''. The rows display different strategies to color the single cell data point. If the "hexagon mode'' is activated, the embedded cells colored with density will be displayed. If the optional file `*_gene_cnv.csv` is uploaded, the embedded cells colored with gene CNV profiles will be shown. Users can specify the gene for coloring in "Editor-General Settings''. Moreover, all categorical meta labels available in uploaded file `*_meta_scsvas.csv` will be used as color schemes by default. Users can decide to display or hide these meta labels in "Editor-Select categorical meta label''. If the mouse hovers over one scatter point or hexagon bin, an interactive tooltip carried its vital information will appear. 

## Input & Demo File

The uploaded file must match the *required* format, please check the general accepted [input file format](data/input_format). Several demo files descripted in [demo data](data/demo_data) are provided in the "Editor" sidebar. 



## Interactions

   + Download </br>
     An SVG file will be generated when you click the ''Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the ''Light Theme'' button.
   + Tooltips and Highlights </br>
     When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are two major types of component in the ''Embedding Map'' application and their tooltipping and highlighting interactions are as follows:
     + Hexagon bins on the 2D-Embedding hexagon plot </br>
       The tooltip will display the x and y coordinates,  the coloring value, the number of cells in the bin, and the list of cell IDs.
     + Scatter point on the 2D-Embedding scatter plot </br>
       The tooltip will display the x and y coordinates, the coloring value, and the cell ID.

## Editor Functionalities

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in ''Editor Settings''.

   + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with ''CNV View'' visualization.
   + General Settings </br>
     + Select embedding methods </br>
       User can select to display available embedding methods.
     + Hexagon Mode </br>
       User can choose ''hexagon mode'' or ''scatter mode''.
     + Width of hexagon bin </br>
       User can adjust the width of hexagon bin.
     + Hexagon bin averaging scheme </br>
       User can choose ''mean'' or ''median'' as hexagon bin averaging scheme.
     + Radius of scatter point </br>
       User can adjust the radius of scatter point.
     + Search for gene </br>
       User can search or select a gene, and color the embedding plot with its copy number.
     + Embedding plot height </br>
       User can adjust the height of each embedding plot.
     + Embedding plot width </br>
       User can adjust the width of each embedding plot.
   + Select categorical meta label </br>
      Users can choose which categorical meta label to use for coloring the embedded plot. 
   + Color Palettes </br>
      Users can customize color palettes for ''Density'' and available categorical labels.

## Reference

Freytag, S., & Lister, R. (2019). 
[schex avoids overplotting for large single-cell RNA-sequencing datasets.](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz907/5651017)
*Bioinformatics*.
(PMID: [31794001](https://www.ncbi.nlm.nih.gov/pubmed/31794001), See [Figure 1](https://academic.oup.com/view-large/figure/190380643/btz907f1.tif))

## Version

v1.0.1 (2020-12-16)

## Developer

Mr. Chaohui Li ([GitHub](https://github.com/Eric0627))

## Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.1
   - Add hexagon mode.

### v1.0.0
   - Initial functions implemented.

##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

The web interface "CNV Heatmap'' is extension version of "CNV View'', by supporting extra functionalities including genome region zooming, local region search, and local region annotation.  

"CNV Heatmap'' enables users to create the cnv heatmap of single cell CNV profiles in following straightforward steps as follow:

+ Open https://sc.deepomics.org/demo-project/analyses/heatmap in Google browser, and upload cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv`.
+  *Optional* With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` as inputs, users can run `scSVAS` to get the cutted dendrogram of single cells, and upload it to compress the heatmap plot.
+  *Optional* Users can also upload a customized bed file to check the CNV heatmap in local region.
  
  

Users can get a single cell CNV landscape view of scDNA-seq data. With single cells as rows and genomic regions as columns, the cell CNV heatmap exhibits the copy number of a specific single-cell across the entire genome. The cell meta heat map will be displayed on the left if users provide single-cell meta information. In addition, there is a genome zoom slider located at the bottom of CNV heatmap. Users can drag the slider to zoom in and out on the genome region. Users can also search for a local genome region in "Editor General Settings". If the local genome region is less than 5M, an annotation layer including "Repeat track'' and "Gene track'' will be displayed. If the mouse hovers over cell CNV/meta heatmap, repeats, and genes, an interactive tooltip carried its vital information will appear. 



# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/CNV_input_format.markdown).




# Version

v1.0.0 (2020-12-16)

# Developer

Mr. Yuhao Qing ([GitHub](https://github.com/Q-Y-H))

# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

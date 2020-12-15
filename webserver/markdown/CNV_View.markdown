##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

Over the past two decades, CNV heatmap has often been adopted to visualize the CNV profiles of a batch of samples or single cells in various sequencing protocols. e.g. bulk SNP array, whole genome/exon sequencing, single cell RNA sequencing. For single cell DNA sequencing, CNV heatmap aids the landscape view of single cell copy number in several pieces of literature. In addition, Smith *et. al.* developed a visualization tool CellScape for single cell CNV heatmap.

Nevertheless, with the stride of 10x Genomics high throughput sequencing, the scale of sequenced cells escalates exponentially, aka, thousands of cells at a time. Efficient visualization of the heatmap with a large (e.g. 1k x 5k) size is critical for scientific interpretation. Plotting using R or Python packages, or existing heatmap visualization tools like CellScape are incredibly time-consuming and memory-intensive when it reaches thousands of cells and thousands of genomic regions. 

It is essential to reduce the size of heatmap while retaining the heterogeneity among single cells. 10x CNV official visualization tool Loupe solves this issue by building a single cell dendrogram in advance, splitting single cells into less than 100 subgroups by cutting the dendrogram, and collapsing single cells inside the cluster into one row in the heatmap. Cluster zoom-in operation is achieved by clicking the node in the dendrogram.  

In the scSVAS platform, cooperating scSVAS pipeline, we build web interface ''CNV View''  for interactive and real-time visualization of CNV landscape of scDNA-seq data with zoomable dendrogram. Compared with Loupe, ''CNV View'' also visualizes the aggregate subgroup CNV heatmap and stairstep, which is commonly adopted in reputable publications.

''CNV View'' enables users to create the landscape of single cell CNV profiles in two straightforward steps as follow:

  + Open (https://sc.deepomics.org/demo-project/analyses/view) in Google browser, and upload cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv`.
  + *Optional* With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` as inputs, users can run `scSVAS` to get the cutted dendrogram of single cells, and upload it to compress the heatmap plot.

Users can get a single cell CNV landscape view of scDNA-seq data. With single cells as rows and genomic regions as columns, the cell CNV heatmap exhibits the copy number of a specific single cell across the entire genome. The cell meta heat map will be displayed on the left if users provide single cell meta information.
In addition, the aggregate subgroup CNV heat map and stairstep will also be listed in the bottom layers. The user can select the subgroups to be aggregated in the "Editor General Settings". If users offer the cut dendrogram file, a zoomable cut dendrogram will be displayed on the left.
If the mouse hovers over cell CNV/meta heatmap, cutted dendrogram, and stairstep, an interactive tooltip carried its vital information will appear. 

# Input File Format
The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the [GitHub](https://github.com/paprikachan/scSVAS/tree/master/demo_data) project. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/CNV_input_format.markdown).

# Display Interactions

There are two types of interactions: *Tooltips* and *Download*.

- **Tooltips**
  Tooltips will show necessary information of object that the mouse points to.
  + __*Meta Column*__: ID of cell, name of meta information, value of meta information.
  + __*Main Heatmap Unit*__: ID of cell, location of bin in chromosomes, and average copy number of the bin.
  + __*Meta Heatmap Unit*__: Name of group, location of bin, and average copy number of the bin.
  + __*Stairstep Point*__: Chromosome number, pointed position of chromosome and average copy number of the pointed position.
- **Download**
  One SVG file will be generated when the '**Download**' button is clicked. Two themes are supplied: the default theme with dark background and the light theme with white backgroud. To use the light theme, please click the '**Light Theme**' button.

# Sidebar Functions
The sidebar provides diverse options to fine-tune the display, such as manage files, reset color, select SV event, and so on.

- **Files**
  + __*Upload*__: upload heatmap TXT file, and manage uploaded files. Note that duplicated file name will be alerted and given a random postfix.
  + __*Choose*__: choose files uploaded previously. Note that this function is ONLY available to registered user (each account has certain storage).
  + __*File Sets*__: NOT available to this page.

-   ***General***
    -   ***Auto Load Heatmap***: Load the main heatmap on the webpage loaded. *(Default: false)*
    -   ***Display the Main Heatmap***: Show the main heatmap. *(Default: true)*
    -   ***None Cases***: The identifier for data not provided in the CNV .csv file. *(Default: N/A)*
    -   ***Reorder samples by***: Reorder the sample cells by ID in ASCII order, meta information, or the original orders in the selected CNV file. *(Default: Original orders in selected CNV file.)*
-   ***Filter***: A filter to show cells with matched meta information.
-   ***Advanced Settings***
    -   ***Layout***
        -   ***Unit Height in Heatmap***: The height of a unit in the main heatmap. An integer number is recommended for better webpage rendering. *(Default: 1)*
        -   ***Unit Width in Heatmap***: The width of a unit in the main heatmap. An Integer number is recommended for better webpage rendering. *(Default: 1)*
        -   ***Distance to the left margin***: The distance of the graph to the left margin of the background. *(Default: 20)*
        -   ***Distance to the top margin***: The distance of the graph to the top margin of the background. *(Default: 20)*
        -   ***Width of a meta column***: The width of the columns of meta information. *(Default: 20)*
        -   ***Width of legends***: The width of the legends at the left side of the graph. *(Default: 120)*

# Reference

Bulk CNV SNP array

Emmanuel, C., Chiew, Y. E., George, J., Etemadmoghadam, D., Anglesio, M. S., Sharma, R., ... & Galletta, L. (2014). 
[Genomic classification of serous ovarian cancer with adjacent borderline differentiates RAS pathway and TP53-mutant tumors and identifies NRAS as an oncogenic driver.](https://clincancerres.aacrjournals.org/content/20/24/6618)
*Clinical cancer research*, 20(24), 6618-6630.
(PMID: [25316818](https://www.ncbi.nlm.nih.gov/pubmed/25316818), See Figure 2)

Savas, P., Teo, Z. L., Lefevre, C., Flensburg, C., Caramia, F., Alsop, K., ... & Kanu, N. (2016). [The subclonal architecture of metastatic breast cancer: results from a prospective community-based rapid autopsy program “CASCADE”.](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002204)
*PLoS medicine*, 13(12), e1002204.
(PMID: [28027312](https://www.ncbi.nlm.nih.gov/pubmed/28027312), See [Figure 7](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5189956/figure/pmed.1002204.g007/))

scRNA

Patel, A. P., Tirosh, I., Trombetta, J. J., Shalek, A. K., Gillespie, S. M., Wakimoto, H., ... & Louis, D. N. (2014). 
[Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma.](https://science.sciencemag.org/content/344/6190/1396)
*Science*, 344(6190), 1396-1401.
(PMID: [24925914](https://www.ncbi.nlm.nih.gov/pubmed/24925914), See [Figure 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4123637/figure/F1/))

Tirosh, I., Izar, B., Prakadan, S. M., Wadsworth, M. H., Treacy, D., Trombetta, J. J., ... & Fallahi-Sichani, M. (2016). 
[Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq.](https://science.sciencemag.org/content/352/6282/189)
*Science*, 352(6282), 189-196.
[PMID: (27124452](https://www.ncbi.nlm.nih.gov/pubmed/27124452), See [Figure 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4944528/figure/F1/))

Puram, S. V., Tirosh, I., Parikh, A. S., Patel, A. P., Yizhak, K., Gillespie, S., ... & Deschler, D. G. (2017). 
[Single-cell transcriptomic analysis of primary and metastatic tumor ecosystems in head and neck cancer.](https://www.cell.com/cell/fulltext/S0092-8674(17)31270-9?cid=tw%26p)
*Cell*, 171(7), 1611-1624.
(PMID: [29198524](https://www.ncbi.nlm.nih.gov/pubmed/29198524), See [Figure 1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5878932/figure/F1/))





# Version

v1.0.0 (2020-12-16)

# Developer

Mr. Yuhao Qing ([GitHub](https://github.com/Q-Y-H))

Mr. Ruikang Li ([GitHub](https://github.com/RKLho))

# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

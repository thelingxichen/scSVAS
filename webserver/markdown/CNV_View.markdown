##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction

Over the past two decades, CNV heatmap has often been adopted to visualize the CNV profiles of a batch of samples or single cells in various sequencing protocols. e.g. bulk SNP array, whole genome/exon sequencing, single cell RNA sequencing. For single cell DNA sequencing, CNV heatmap aids the landscape view of single cell copy number in several pieces of literature. In addition, Smith *et. al.* developed a visualization tool CellScape for single cell CNV heatmap.

Nevertheless, with the stride of 10x Genomics high throughput sequencing, the scale of sequenced cells escalates exponentially, aka, thousands of cells at a time. Efficient visualization of the heatmap with a large (e.g. 1k x 5k) size is critical for scientific interpretation. Plotting using R or Python packages, or existing heatmap visualization tools like CellScape are incredibly time-consuming and memory-intensive when it reaches thousands of cells and thousands of genomic regions. 

It is essential to reduce the size of heatmap while retaining the heterogeneity among single cells. 10x CNV official visualization tool Loupe solves this issue by building a single cell dendrogram in advance, splitting single cells into less than 100 subgroups by cutting the dendrogram, and collapsing single cells inside the cluster into one row in the heatmap. Cluster zoom-in operation is achieved by clicking the node in the dendrogram.  

In the scSVAS platform, cooperating scSVAS pipeline, we build web interface ''CNV View''  for interactive and real-time visualization of CNV landscape of scDNA-seq data with zoomable dendrogram. Compared with Loupe, ''CNV View'' also visualizes the aggregate subgroup CNV heatmap and stairstep, which is commonly adopted in reputable publications.

''CNV View'' enables users to create the landscape of single cell CNV profiles in two straightforward steps as follow:

  + Open https://sc.deepomics.org/demo-project/analyses/view in Google browser, and upload cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv`.
  + *Optional* With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` as inputs, users can run `scSVAS` to get the cutted dendrogram of single cells, and upload it to compress the heatmap plot.

Users can get a single cell CNV landscape view of scDNA-seq data. With single cells as rows and genomic regions as columns, the cell CNV heatmap exhibits the copy number of a specific single cell across the entire genome. The cell meta heat map will be displayed on the left if users provide single cell meta information.
In addition, the aggregate subgroup CNV heat map and stairstep will also be listed in the bottom layers. The user can select the subgroups to be aggregated in the "Editor General Settings". If users offer the cut dendrogram file, a zoomable cut dendrogram will be displayed on the left.
If the mouse hovers over cell CNV/meta heatmap, cutted dendrogram, and stairstep, an interactive tooltip carried its vital information will appear. 

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/CNV_input_format.markdown).


# Interactions


  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over an component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "CNV View'' application and their tooltipping and highlighting interactions are as follows:
    - Unit Component on the Cell CNV Heatmap </br>
          The tooltip will display the genome position and copy number of a unit. The name of the corresponding leaf node in the cutted dendrogram will also be shown. Further, the genome position, the leaf node, and the range of the leaf node will be highlighted.
    - Unit Component on the Cell Meta Heatmap </br>
          The tooltip will display the cell ID and meta label of a unit.
    - Cutted Dendrogram Node </br>
          The tooltip will display the name of the current node, the number of cells in it, the parent node of it, and the distance between it and the root node. Further, the subtree and the covered cell range of the current node will be highlighted.
    - Cutted Dendrogram Branch </br>
          The tooltip will display the names of the associated parent and child nodes and their branch distance. The branch, the parent node, and the child node ill be highlighted.
    - Unit Component on the Aggregate Subgroup CNV Heatmap </br>
          The tooltip will display the genome position, the copy number, and the subgroup name.
    - Component on the Aggregate Subgroup CNV Stairstep </br>
          The tooltip will display the genome position and the average copy number of cells for all subgroups.
    - Dendrogram Zooming </br>
      When users click a node in the cutted dendrogram, the selected node will be regarded as the temporary tree root, and a new sub-cutted dendrogram will be rendered. The cell CNV heatmap and meta panel will also be updated to fit the current cell range. When you click the "Back to Root'' button, the whole CNV view will return to its initial status. You may also utilize the "left arrow'' and "right arrow'' buttons to un-do and re-do zooming operations.



# Editor Functionality

The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets </br>
    Users can select a demo file set for an instant preview. 

  + Files

    + Upload </br>
      Users can upload and manage the input files. Note that the repeated file name will be warned and given a random postfix.
    + Choose </br>
      Users can choose files uploaded previously. 
    + File sets </br>
      Users can save multiple files together as a file set, then decide to display one file set previously stored.

  + General Settings 

    - Auto load heatmap </br>
      Checkbox for user to decide whether the cell CNV heatmap will automatically be loaded. 
    - NA cases (separated by comma ,) </br>
      User can define the NA cases in CNV csv file, the default `N/A,NA` means empty space `""`, string `N/A`, and string `NA` will be considered NA cases by file parser.
    - Reorder cells by </br>
      Users can reorder cells in cell CNV/meta heatmap by meta labels in ascending or descending order. The default order is the cell ordered in uploaded CNV csv file. Please note this functionality is effective only when on cutted dendrogram JSON file supplied.
    - Aggregate subgroup </br>
      Users can select categorical meta label to display in aggregate subgroup CNV heatmap and stairstep. The average copy number value in subgroup will be displayed.

  + Select categorical meta label </br>
    Users can choose which categorical meta label to show in the heatmap. Please note this functionality is effective only when on cutted dendrogram JSON file supplied.

  + Layout Settings 

    - Basic 

      + Figure margin - left </br>
        User can adjust the left margin of the figure.

      - Figure margin - top </br>
        User can adjust the top margin of the figure.
      - Genome zoom slider - height </br>
        User can adjust the height of genome zoom slider.
      - Margin between CNV heatmap and genome zoom slider </br>
        User can adjust the margin between CNV heatmap and genome zoom slider.
      - Margin betwenn cutted dendrogram and meta heatmap </br>
        User can adjust the margin between cutted dendrogram and meta heatmap.

    - CNV Heatmap

      - Unit height of CNV heatmap, unit width of CNV heatmap (integer recommended) </br>
        User can adjust the unit height and unit width of CNV heatmap. Unit refers to the smallest rendered SVG object in heatmap. Please note that the heatmap unit height and unit width are recommend to set as integer, floating point will make heatmap transparent owing to subpixel rendering.
      - Chromosomes - height </br>
        Users can adjust the height of chromosomes.
      - Show vertical line between chromosomes </br>
        User can decide whether to show vertical line between chromosomes.
      - Desired width of CNV heatmap </br>
        Users can adjust the width of CNV heatmap, default is 1000.
      - Left highlight - width </br>
        User can adjust the width of left highlight.
      - Top highlight - height </br>
        User can adjust the height of right highlight.

    - Meta Heatmap

      - Unit width of meta heatmap </br>
        User can adjust the unit width of meta heatmap. 
      - Meta heatmap legend - width </br>
        User can adjust the width of meta heatmap legend.
      - Margin between different meta heatmap legends </br>
        User can adjust the margin between different meta heatmap legends.

    - Cutted Dendrogram

      - Dendrogram - width </br>
        User can adjust the width of cutted dendrogram.

  + Color palettes </br>
    Users can customize color palettes for available categorical meta labels and continuous meta labels.


<!--

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

-->



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

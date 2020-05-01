##### [Download](https://raw.githubusercontent.com/Nobel-Justin/Oviz-Bio-demo/master/CNV_EmbeddingMap/demo_data/10x.txt) the `official demo input file`.

Additional demo files are provided in the [GitHub](https://github.com/Nobel-Justin/Oviz-Bio-demo/tree/master/SV_Heatmap/demo_data) project.

# Introduction
Xxx. 

# Input File Format
The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the [GitHub](https://github.com/Nobel-Justin/Oviz-Bio-demo/tree/master/SV_Heatmap/demo_data) project. Please check the general accepted [input file format](xxx).

# Display Interactions
There are two types of interactions: *Tooltips* and *Download*.

- **Tooltips**
  Tooltips will show necessary information of the cell point or hexagon bin that the mouse points to.
  + __*Coordinate*__: The embedding coordinate of the cell point or hexagon bin.
  + __*Annotation Value*__: The choosen annotation (Density or other meta info) value of the cell point or hexagon bin.
  + __*Cell ID/IDs*__: The choosen cell id or a list of cell ids in the choosen hexagon bin.
  + __*Cell Number*__: The number of cells in the choosen hexagon bin
   
- **Download**
  One SVG file will be generated when the '**Download**' button is clicked. Two themes are supplied: the default theme with dark background and the light theme with white backgroud. To use the light theme, please click the '**Light Theme**' button.

# Sidebar Functions
The sidebar provides diverse options to fine-tune the display, such as manage files, reannotate color, turn off **Hexagon Mode**, and so on.

- **Files**
  + __*Upload*__: upload embedding input `.csv` file, and manage uploaded files. Note that duplicated file name will be alerted and given a random postfix.
  + __*Choose*__: choose files uploaded previously. Note that this function is ONLY available to registered user (each account has certain storage).
  + __*File Sets*__: NOT available to this page.
- **General**
  + __*Annotate cells by*__: choose the annotation schema of data, from *density* and other meta informations (*Cluster*, *Region Ploidy*).
  + __*Hexagon Mode*__: turn on or off "Hexagon Mode" (rescale cell point with hexagon bin).
  + __*Set width of hexagon*__: set the size of each hexagon (only available under Hexagon Mode).

# Reference

Freytag, S., & Lister, R. (2019). 
[schex avoids overplotting for large single-cell RNA-sequencing datasets.](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz907/5651017)
*Bioinformatics*.
(PMID: [31794001](https://www.ncbi.nlm.nih.gov/pubmed/31794001), See [Figure 1](https://academic.oup.com/view-large/figure/190380643/btz907f1.tif))

# Version

v1.0.1 (2020-02-17)

# Developer

Mr. Chaohui Li ([GitHub](https://github.com/Eric0627))

# Designer

Miss. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.1
   - Add hexagon mode.
   
### v1.0.0
   - Initial functions implemented.

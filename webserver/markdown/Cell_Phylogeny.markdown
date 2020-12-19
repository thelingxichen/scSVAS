##### Please try the demo files in the sidebar (`Demo File Sets`).

# Introduction


In scSVAS platform, we build a readily available web interface "CNV Cell Phylogeny''  for interactive and real-time visualization of scDNA-seq data.

"CNV Cell Phylogeny'' enables users to create the cell phylogeny plot in one straightforward step as follow:

 + With cnv profile file `*_cnv.csv`, predefined meta file `*_meta.csv` and targeted gene list as inputs, run `scSVAS` to get the single cells cutted dendrogram `*_cut.json`, the subclone and embedding results `*_meta_scsvas.csv`, and targeted gene cnv profiles `*_gene_cnv.csv}`.
 + Open https://sc.deepomics.org/demo-project/analyses/cell\_phylogeny in Google browser, and upload files `*_cut.json`, optional files `*_meta_scsvas.csv` and `*_gene_cnv.csv`.

Then, you may get a cutted dendrogram of single cells. Users can switch the tree between "Topdown'' and "Circular'' modes. If the optional file `*_meta.csv` and `*_gene_cnv.csv` are uploaded, the cell meta and CNV heatmap will be shown. Users can decide to display or hide these meta labels in "Editor-Select categorical meta label''. If the mouse hovers over a dendrogram or heatmap, an interactive tooltip carried its vital information will appear.

# Input File Format

The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the sidebar. Please check the general accepted [input file format](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/scSVAS_Input_Format.markdown).

# Interactions

  + Download </br>
    An SVG file will be generated when you click the "Download'' button. We offer two themes, dark and light. To switch to the light theme, please click the "Light Theme'' button.
  + Tooltips and Highlights </br>
    When your cursor hovers over a component on the visualization panel, essential information about the component will show up in the tooltip, and related components will be highlighted. There are several major types of component in the "CNV View'' application and their tooltipping and highlighting interactions are as follows:
    + Cutted Dendrogram Node, Cutted Dendrogram Branch, Dendrogram Zooming, Meta CNV Heatmap </br>
      Tooltipping and highlighting interactions are the same with "CNV View'' visualization.
    + Cell CNV Heatmap </br>
      The tooltip will display the column name of a unit (such as gene or bin region) and its corresponding leaf node in the cutted dendrogram. Further, the column name, the leaf node, and the range of the leaf node will be highlighted.
  + TopDown <=> Circular </br>
    Users can click this button to switch the cutted dendrogram between "TopDown'' and "Circular'' modes.
             
             
# Editor Functionalities
The editor offers various options to fine-tune the visualization. Users can adjust the editor width and font size in "Editor Settings''.

  + Demo File Sets, Files </br>
     Demo file sets and files Functionalities are the same with "CNV View'' visualization.
  + General Settings </br>
    + Type of cutted dendrogram </br>
       Users can choose the type of cutted dendrogram between "topdown'' and "circular''.
    + NA cases (seperated by comma ,) </br>
       User can define the NA cases in CNV csv file, the default `"N/A,NA''` means empty space `"''`, string `"N/A"`, and string `"NA"` will be considered NA cases by file parser.
  + Topdown Layout Settings </br>
    Topdown Layout Settings are the same with "Layout Settings'' in "CNV Cell Phylogeny'' visualization.
  + Circular Layout Settings </br>
    + Basic </br>
       + Figure margin - left </br>
         Users can adjust the left margin of the figure.
       + Figure margin - top </br>
         Users can adjust the top margin of the figure.  
       + Margin between circular cutted dendrogram and meta heatmap </br>
         Users can adjust the margin between circular cutted dendrogam and meta heatmap.
    + Circular Layout </br>
       + Start angle of circular cutted dendrogam </br>
         Users can adjust the start angle of circular cutted dendrogram.
       + End angle of circular cutted dendrogam </br>
         Users can adjust the end angle of circular cutted dendrogram.
       + Inner radius of circular cutted dendrogram </br>
         Users can adjust the inner radius of circular cutted dendrogram.
       + Unit width of CNV heatmap (integer recommended) </br>
         Users can adjust the unit width of CNV and meta heatmap. Unit refers to the smallest rendered SVGobject in heatmap. Please note that the heatmap unit width are recommend to set as integer, floating point will make heatmap transparent owing to subpixel rendering.
  + Color Palettes </br>
         Users can customize color palettes for available categorical meta labels and continuous meta labels.


# Version

v1.0.0 (2020-12-16)

# Developer

Mr. Yuhao Qing ([GitHub](https://github.com/Q-Y-H))

Mr. Lirui Kang  ([GitHub](https://github.com/RKLho))

# Designer

Dr. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - full functionalities implemented.

# scSVAS

scSVAS an online platform for single cell DNA visualization [sc.deepomics.org](sc.deepomics.org).
 
### Introduction 
 
The recent advance of single-cell copy number variation analysis plays an essential role in addressing intratumor heterogeneity, identifying tumor subgroups, and restoring tumor evolving trajectories at single-cell resolution. Pleasant visualization of copy number analysis results boosts productive scientific exploration, validation, and sharing. Several appealing single-cell copy number figures have been demonstrated in published articles and software. However, those pictures almost lack real-time interaction, and it's hard for researchers to prepare codes to reproduce them from scratch. Moreover, existing single-cell visualization tools are incredibly time-consuming and memory-intensive when it reaches today's large-scale single-cell throughput. 

![Overview of scSVAS online application](https://github.com/paprikachan/scSVAS/blob/master/webserver/fig/Figure1.png)
*Figure1: Overview of scSVAS*

We present an online platform scSVAS (https://sc.deepomics.org) for aesthetically-pleasing, real-time interactive, user-friendly single-cell copy number variation analysis, including copy number heatmap view, ploidy stairstep, ploidy distribution, embedding map, time lineage, space lineage, space prevalence, clonal lineage, and recurrent event (Figure1a). scSVAS is specifically designed for large-scale single cells analysis. After uploading the required upstream copy number analysis results, users may make scientific discoveries, and share interactive visualization, and download high-quality publication-ready figures. Compared with other scDNA visualization tools Loupe and E-Scape, scSVAS manifest the most comprehensive functionalities (Figure1b-c).


![Workflow of scSVAS](https://github.com/paprikachan/scSVAS/blob/master/webserver/fig/Figure2.png)
*Figure2: Workflow of scSVAS*
 
Figure 2 demonstrates the input files required for each scSVAS application. The demo files are available at “Editor” on each application page. The input format are specified in [here](https://github.com/paprikachan/scSVAS/blob/master/webserver/markdown/scSVAS_Input_Format.markdown). The auxiliary scripts are available at [`./scripts`](https://github.com/paprikachan/scSVAS/blob/master/scripts).

In short, scSVAS provides versatile utilities for managing, investigating, sharing, and publishing single-cell copy number variation profiles. All visualization are publicly hosted at https://sc.deepomics.org. Offline analysis pipeline are available at https://github.com/paprikachan/scSVAS.


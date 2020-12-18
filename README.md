# scSVAS

scSVAS (scDNA-seq Somatic Variant Analysis Suite) is:
  + a pipeline for single cell DNA somatic variant analysis.
  + an online platform for single cell DNA visualization [sc.deepomics.org](sc.deepomics.org).
 
The recent advance of single-cell copy number variation analysis plays an essential role in addressing intratumor heterogeneity, identifying tumor subgroups, and restoring tumor evolving trajectories at single-cell resolution. Pleasant visualization of copy number analysis results boosts productive scientific exploration, validation, and sharing. Several appealing single-cell copy number figures have been demonstrated in published articles and software. However, those pictures almost lack real-time interaction, and it's hard for researchers to prepare codes to reproduce them from scratch. Moreover, existing single-cell visualization tools are incredibly time-consuming and memory-intensive when it reaches today's large-scale single-cell throughput. 

![Overview of scSVAS online application](https://github.com/paprikachan/scSVAS/blob/master/webserver/fig/Figure1.png)
*Figure1: Overview of scSVAS*

We present an online platform scSVAS (https://sc.deepomics.org) for aesthetically-pleasing, real-time interactive, user-friendly single-cell copy number variation analysis, including copy number heatmap view, ploidy stairstep, ploidy distribution, embedding map, time lineage, space lineage, space prevalence, clonal lineage, and recurrent event (Figure1a). scSVAS is specifically designed for large-scale single cells analysis. After uploading the required upstream copy number analysis results, users may make scientific discoveries, and share interactive visualization, and download high-quality publication-ready figures. Compared with other scDNA visualization tools Loupe and E-Scape, scSVAS manifest the most comprehensive functionalities (Figure1b-c).


![Workflow of scSVAS](https://github.com/paprikachan/scSVAS/blob/master/webserver/fig/Figure2.png)
*Figure2: Workflow of scSVAS*
 
Figure 2 demonstrates the platform workflow. It currently has two parts, off-line and online. The off-line part is the scSVAS suite. With single-cell DNA bam files or 10x cellranger results as input, scSVAS can generate all files needed for online visualization applications. 

In short, scSVAS provides versatile utilities for managing, investigating, sharing, and publishing single-cell copy number variation profiles. All visualization are publicly hosted at https://sc.deepomics.org. Offline analysis pipeline are available at https://github.com/paprikachan/scSVAS.


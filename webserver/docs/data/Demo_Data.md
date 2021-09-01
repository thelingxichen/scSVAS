# Demo Data

## Overview

The following table lists scSVAS applications' input files and demo datasets. `<file>` and `[file]` refers to compulsory and optional input file, respectively. Aberrations: Triple-negative breast cancer (TNBC); Acute myeloid leukaemia (AML); High grade serous ovarian cancer (HGSOC); Prostate cancer (PC); Lung cancer (LC).

|scSVAS Applications| Input Files | Demo Datasets |
|--|--|--|
|CNV View| <cnv.csv>, [cut.json], [meta.csv] | TNBC_T10,T16 [1,2], 10x_COLO829[3] |
|CNV Heatmap | <cnv.csv>, [cut.json], [meta.csv], [gene_cnv.csv], [target_region.bed] | TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Cell Phylogeny | <cut.json>, [meta.csv], [gene_cnv.csv] | TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Ploidy Stairstep | <cnv.csv>, [meta.csv] | TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Ploidy Distribution | <cnv.csv>, [meta.csv] |TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Embedding Map | <meta.csv>, [gene_cnv.csv] |TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Time Lineage | <clonal_edges.csv], <clonal_prev.csv> | AML [4,5], HGSOC_P7 [5,6]|
|Space Lineage | <clonal_edges.csv>, <clonal_prev.csv>, [space_edges.csv], [image.png] | HGSOC_P1,P7 [5,6], PC_A21 [5,7] |
|Space Prevalence | <clonal_edges.csv>, <clonal_prev.csv>, <space_edges.csv> | HGSOC_P1,P7 [5,6], PC_A21 [5,7] |
|Clonal Lineage | <evo.json>, [target_anno.tsv] | TNBC_T10,T16 [1,2], 10x_COLO829[3]|
|Recurrent Event | <recurrent.json>, [recurrent.tsv], [target_anno.tsv], [sample_meta.csv] | LC |


The following table lists the source of the demo datasets. 

| Demo Datasets| Description |
|--|--|
| TNBC_T10,T16 | Raw FASTQ data obtained with SRA code SRA018951 [1], profiled by SCYN [2] to get the NV call, and processed by `scSVAS.py`. |
| 10x_COLO829 | The cellranger-dna processed data was obtained from [10x official resource](https://www.10xgenomics.com/resources/datasets}~\cite{velazquez2020single) [3], and processed by scSVAS offline pipeline. |
| AML | Raw data from Ding *et al*. [4], input files obtained from E-Scape demo dataset [5].|
| HGSOC_P1,P7 | Raw data from McPherson *et al*. [6], input files obtained from E-Scape demo dataset [5]. |
| PC_A21 | Raw data from Gundem *et al*. [7], input files obtained from E-Scape demo dataset [5].|
| LC | The lung cancer data present in "Recurrent Event" is prepared in another manuscript. |

Aberrations: Triple-negative breast cancer (TNBC); Acute myeloid leukaemia (AML); High grade serous ovarian cancer (HGSOC); Prostate cancer (PC); Lung cancer (LC). 

## Reference

[1] Navin, N., Kendall, J., Troge, J., Andrews, P., Rodgers, L., McIndoo, J., Cook, K., Stepansky, A., Levy, D., Esposito, D., Muthuswamy, L., Krasnitz, A., McCombie, W. R., Hicks, J., & Wigler, M. (2011). Tumour evolution inferred by single-cell sequencing. *Nature*, 472(7341), 90–94. https://doi.org/10.1038/nature09807

[2] Feng, X., Chen, L., Qing, Y., Li, R., Li, C., & Li, S. C. (2020). SCYN: Single cell CNV profiling method using dynamic programming. *bioRxiv*. https://doi.org/10.1101/2020.03.27.011353

[3] Velazquez-Villarreal, E. I., Maheshwari, S., Sorenson, J., Fiddes, I. T., Kumar, V., Yin, Y., ... & Craig, D. W. (2020). Single-cell sequencing of genomic DNA resolves sub-clonal heterogeneity in a melanoma cell line. *Communications biology*, 3(1), 1-8. https://www.nature.com/articles/s42003-020-1044-8

[4] Ding, L., Ley, T. J., Larson, D. E., Miller, C. A., Koboldt, D. C., Welch, J. S., Ritchey, J. K., Young, M. A., Lamprecht, T., McLellan, M. D., McMichael, J. F., Wallis, J. W., Lu, C., Shen, D., Harris, C. C., Dooling, D. J., Fulton, R. S., Fulton, L. L., Chen, K., Schmidt, H., … DiPersio, J. F. (2012). Clonal evolution in relapsed acute myeloid leukaemia revealed by whole-genome sequencing. *Nature*, 481(7382), 506–510. https://doi.org/10.1038/nature10738

[5] Smith, M. A., Nielsen, C. B., Chan, F. C., McPherson, A., Roth, A., Farahani, H., Machev, D., Steif, A., & Shah, S. P. (2017). E-scape: interactive visualization of single-cell phylogenetics and cancer evolution. *Nature methods*, 14(6), 549–550. https://doi.org/10.1038/nmeth.4303

[6] McPherson, A., Roth, A., Laks, E., Masud, T., Bashashati, A., Zhang, A. W., Ha, G., Biele, J., Yap, D., Wan, A., Prentice, L. M., Khattra, J., Smith, M. A., Nielsen, C. B., Mullaly, S. C., Kalloger, S., Karnezis, A., Shumansky, K., Siu, C., Rosner, J., … Shah, S. P. (2016). Divergent modes of clonal spread and intraperitoneal mixing in high-grade serous ovarian cancer. *Nature genetics*, 48(7), 758–767. https://doi.org/10.1038/ng.3573

[7] Gundem, G., Van Loo, P., Kremeyer, B., Alexandrov, L. B., Tubio, J., Papaemmanuil, E., Brewer, D. S., Kallio, H., Högnäs, G., Annala, M., Kivinummi, K., Goody, V., Latimer, C., O'Meara, S., Dawson, K. J., Isaacs, W., Emmert-Buck, M. R., Nykter, M., Foster, C., Kote-Jarai, Z., … Bova, G. S. (2015). The evolutionary history of lethal metastatic prostate cancer. *Nature*, 520(7547), 353–357. https://doi.org/10.1038/nature14347


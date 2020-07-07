

Oviz-SingleCell CNV analysis accepts the output of [`SCYN`](https://github.com/xikanfeng2/SCYN), [`cellranger-dna`](xxx).


### SCYN Output Format
The output of `SCYN` consits of two cnv files and one meta file. 

 - `prefix_cnv.csv`: with cell as row and bin as column. This file can be used as the input of Oviz-SingleCell CNV analysis.
 - `prefix_cnv_T.csv`: with bin as column and cell as row, it is the transpose matrix of `prefix_cnv.csv`. This file can be parse by popular R packages like [`ExpressionSet`](https://www.bioconductor.org/packages/release/bioc/vignettes/Biobase/inst/doc/ExpressionSetIntroduction.pdf) for downstream analysis.
 - `prefix_meta.csv`: with cell as row, and meta information as column. The default meta information is:
   + `c_gini`: stores the gini coeficient of each cell.
   + `c_ploidy`: stores the mean ploidy of each cell, it is calculated from `prefix_cnv.csv` (not the one SCOPE provide).
   After running [`meta.py`](https://github.com/paprikachan/scVar), user can get `prefix_meta_scvar.csv` with additional meta fields:
   + `hcluster`: the hierachy clustering result.
   + `e_PC1`: the first principle component of cells after PCA.
   + `e_PC2`: the second principle component of cells after PCA.
   + `e_TSNE1`: the first dimension of cells after T-distributed Stochastic Neighbor Embedding (t-SNE).
   + `e_TSNE2`: the second dimension of cells after T-distributed Stochastic Neighbor Embedding (t-SNE).
   + `e_UMAP1`: the first dimension of cells after Uniform Manifold Approximation and Projection (UMAP).
   + `e_UMAP2`: the second dimension of cells after Uniform Manifold Approximation and Projection (UMAP).
   
   User can manually add extra cell meta information like 'cell_type' and 'group' for downstream analysis. Prefix `c` here denotes numeric continuous value. The absence of prefix `c` denotes category meta information like 'group' or 'cluster'. Prefix `e` refers to embedding and dimension reduction.
   
   
### cellranger-dna Output Format
 

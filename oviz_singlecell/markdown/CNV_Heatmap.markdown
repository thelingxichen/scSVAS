##### [Download](https://raw.githubusercontent.com/Nobel-Justin/Oviz-Bio-demo/master/SV_Heatmap/demo_data/10x.txt) the `official demo input file`.

Additional demo files are provided in the [GitHub](https://github.com/Nobel-Justin/Oviz-Bio-demo/tree/master/SV_Heatmap/demo_data) project.

# Introduction
Xxx. 

# Input File Format
The uploaded **CSV** file must match the *required* format. Several demo files from **References** are provided in the [GitHub](https://github.com/Nobel-Justin/Oviz-Bio-demo/tree/master/SV_Heatmap/demo_data) project. Please check the general accepted [input file format](xxx).

# Display Interactions
There are two types of interactions: *Tooltips* and *Download*.

- **Tooltips**
  Tooltips will show necessary information of object that the mouse points to.
  + __*SV Point*__: Chromosome of 5' breakpoint, position of 5' breakpoint, chromosome of 3' breakpoint, position of 3' breakpoint, and variation type of SV event.
- **Download**
  One SVG file will be generated when the '**Download**' button is clicked. Two themes are supplied: the default theme with dark background and the light theme with white backgroud. To use the light theme, please click the '**Light Theme**' button.

# Sidebar Functions
The sidebar provides diverse options to fine-tune the display, such as manage files, reset color, select SV event, and so on.

- **Files**
  + __*Upload*__: upload heatmap TXT file, and manage uploaded files. Note that duplicated file name will be alerted and given a random postfix.
  + __*Choose*__: choose files uploaded previously. Note that this function is ONLY available to registered user (each account has certain storage).
  + __*File Sets*__: NOT available to this page.
- **Color Scheme**
  + __*Color for Min Value*__: reset color of min value.
  + __*Color for Max Value*__: reset color of max value.
- **SV Points**
  A table of SV events can be selected to visualize. Table headers `Gp`, `5'`, `Pos`, `3'`, `Pos`, `Type` respectively refer to the SV group id, chromosome of 5' breakpoint, position of 5' breakpoint, chromosomeof 3' breakpoint, position of 3' breakpoint, variation type of SV event. "blue" and "yellow" stands for positive and negative strand respectively. **Users can click the header to reorder the table.**



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

v1.0.0 (2020-01-03)

# Developer

Mr. Yuhao Qing ([GitHub](xxx))

Mr. Ruikang Li ([GitHub](xxx))

# Designer

Miss. Lingxi Chen ([GitHub](https://github.com/paprikachan))

## Updates

### v1.0.0

   - initial functions implemented.
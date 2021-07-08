sample=$1
export PYTHONPATH=~/Dropbox/workspace:~/Dropbox/workspace/SVAS/scripts
data_dir=~/Desktop/HXLC_sv_data
python3 svLAI.py call \
    --sample=${sample} \
    --mut_fn=${data_dir}/${sample}.svaba.precise.filtered.sv.annotated.tsv,${data_dir}/${sample}.svaba.filtered.indel.annotated.tsv \
    --sv_fn=${data_dir}/${sample}.svaba.precise.filtered.sv.vcf \
    --group_meta_fn=${data_dir}/${sample}_group_meta.csv \
    --barcode_group_fn=${data_dir}/${sample}_barcode_group.csv \
    --out_dir=/Users/chenlingxi/Dropbox/workspace/HXLC/sv_data/${sample} 
    # --tree_fn=${data_dir}/${sample}_edges.csv \

python3 ~/Dropbox/workspace/SVAS/scripts/csv_sv.py call \
    --sv_fn=/Users/chenlingxi/Dropbox/workspace/HXLC/sv_data/${sample}/${sample}.sv.txt \
    --sample=${sample}
    


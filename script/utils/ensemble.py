
import requests, sys


def get_region_by_ens(ens_id, ref):
    if ref == 'hg38':
        server = "https://rest.ensembl.org"
    else:
        server = "https://grch37.rest.ensembl.org"
    ext = "/lookup/id/{}?"

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        return None

    decoded = r.json()
    return 'chr'+decoded['seq_region_name'], decoded['start'], decoded['end'], decoded['display_name']


def get_region_by_gene(ens_id, ref):
    if ref == 'hg38':
        server = "https://rest.ensembl.org"
    else:
        server = "https://grch37.rest.ensembl.org"
    ext = "/lookup/symbol/homo_sapiens/{}?"

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        return None

    decoded = r.json()
    return 'chr'+decoded['seq_region_name'], decoded['start'], decoded['end'], decoded['id']


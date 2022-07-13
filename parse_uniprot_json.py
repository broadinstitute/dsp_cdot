import sys

if (len(sys.argv) < 2):
  print("Error: please provide gene name as an argument")
  return


gene = sys.argv[1] # TODO get it from args
# result after calling

import requests
# 9606 is human
uniprot_link = f"https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606" + \
    "&fields=xref_alphafolddb,xref_bmrb,xref_pcddb,xref_pdb,xref_pdbsum,xref_sasbdb,xref_smr"
response_json = requests.get(uniprot_link).json()

# requests.get(uniprot link) > {gene}.json

#import json
#js = None
#with open(f"{gene}.json", "r") as gj:
#  js = json.load(gj)

uniprot_target = response_json["results"][0]
seq = uniprot_target["sequence"]

structures = uniport_target["uniProtKBCrossReferences"]
s_by_db = dict(map(lambda s: (s["database"], s), structures)

if "AlphaFoldDB" in s_by_db:
  url = f"https://alphafold.ebi.ac.uk/files/AF-{s_by_db["AlphaFoldDB"]}-F1-model_v2.pdb"
  print(url)
# primaryAccession is id for API calls. do we get same info? How to get PDB??
# for an alphaFold structure, it's in the a place (alphafold.ebi.ac.uk/files

# https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606&fields=sequence,structure_3d
# https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606&fields=xref_alphafolddb,xref_bmrb,xref_pcddb,xref_pdb,xref_pdbsum,xref_sasbdb,xref_smr


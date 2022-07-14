
def get_pdb(gene):
  """Download 3D structure for PDB if available. Prefer spectroscopy to AlphaFold2
  and fall back to ColabFold if nothing is available."""

  # 1. pull entries from uniprot. TODO make a uniprot python-cli w/swagger + openapi
  print(f"Querying all UniProtKB entries & structures for {gene}")
  import requests
  fields = [
    "sequence", # sequence in case we need it for colabFold
    "xref_alphafolddb","xref_bmrb,xref_pcddb","xref_pdb", # all 3D structure DBs
    "xref_pdbsum","xref_sasbdb","xref_smr"
  ]
  # 9606 is human
  uniprot_link = f"https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606" + \
      f"&fields={','.join(fields)}"
  response_json = requests.get(uniprot_link).json()
  # TODO cache results with pickle so we can re-run in the future without having to call Uniprot every time

  # 2. get a uniprot result. fail if missing
  if len(response_json["results"]) == 0:
    print(f"ERROR: No results found in UniProt for {gene}")
    return
  uniprot_target = response_json["results"][0]
  
  # 3. extra seq and/or structure from UniProt result
  print(f"Extracting sequence and structure from gene {gene} entry {uniprot_target['primaryAccession']}")
  seq = uniprot_target["sequence"]

  structures = uniprot_target["uniProtKBCrossReferences"]
  structures_by_db = dict(map(lambda s: (s["database"], s), structures))

  # 4. Pull down PDB or get it from colabFold
  # TODO add cases for x-ray crystallography data. Look into setting up an AF2 API for structureless proteins
  url = None
  source = ""
  if "AlphaFoldDB" in structures_by_db:
    source = "AF2"
    url = f"https://alphafold.ebi.ac.uk/files/AF-{structures_by_db['AlphaFoldDB']['id']}-F1-model_v2.pdb"
    print(f"AlphaFold structure found {url}")
  else:
    print("ERROR: Source not supported/AF2 not found")
    return
  pdb_res = requests.get(url).text
  

  # 5. Write pdb to file
  import os
  output_dir = "results"
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  with open(f"{output_dir}/{gene}_{source}.pdb", "w") as f:
    f.write(pdb_res)


  # primaryAccession is id for API calls. do we get same info? How to get PDB??
  # for an alphaFold structure, it's in the a place (alphafold.ebi.ac.uk/files
  
  # https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606&fields=sequence,structure_3d
  # https://rest.uniprot.org/uniprotkb/search?query=gene:{gene}+AND+organism_id:9606&fields=xref_alphafolddb,xref_bmrb,xref_pcddb,xref_pdb,xref_pdbsum,xref_sasbdb,xref_smr


def genes_from_file(filename):
  with open(filename, "r") as f:
    contents = f.read()
    genes = list(map(lambda x: x.strip(), contents.split(',')))
    return genes

## __main__
import sys

genes = []
if len(sys.argv) < 2:
  print("Error: please provide gene name as an argument")
  exit(1)
elif sys.argv[1] != '-f':
  genes = sys.argv[1:] 
elif len(sys.argv) == 3: # parse a comma separated list
  print(f"loading genes from file {sys.argv[2]}")
  genes = genes_from_file(sys.argv[2])
else:
  print("Error malformated args")
  exit(1)


print(f"Loading pfb files for {len(genes)} genes")
for gene in genes:
  get_pdb(gene) 

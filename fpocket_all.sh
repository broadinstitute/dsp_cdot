
# Setup:
# 1. Install docker and pull down the fpocket/fpocket image
# 2. Create a data dir with open access (chmod +777 data) and store all PDBs inside

# Make output dir
mkdir -p fpocket_out

# Loop through all PDB files and run fpocket on each one
# TODO this loop never ends
FILES=$(ls data/*.pdb)
for pdb_file in $FILES
do
  echo $pdb_file # check filename
  echo ${pdb_file%.*}_out # check output filename is as expected
  docker run -v `pwd`:/WORKDIR -w /WORKDIR fpocket/fpocket fpocket -f $pdb_file # run fpocket on the file
  mv ${pdb_file%.*}_out fpocket_out # move outputs to results dir
done

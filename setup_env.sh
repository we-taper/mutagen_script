conda create -n mutagen python=3.6
source ~/miniconda3/bin/activate
conda activate mutagen
conda install -n mutagen --yes -c conda-forge mutagen
conda install -n mutagen --yes autopep8 ipython rope pylint

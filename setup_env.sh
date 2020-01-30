conda create -n mutagen python=3.6
source ~/miniconda3/bin/activate
conda activate mutagen
conda install -c conda-forge mutagen
conda install --yes autopep8 ipython rope pylint

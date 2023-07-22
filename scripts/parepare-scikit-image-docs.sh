VERSION=0.21.0
# conda install -c conda-forge latexmk -y
mkdir -p build
cd build
# if scikit-image folder not exist, clone it
[ ! -d scikit-image ] && git clone https://github.com/scikit-image/scikit-image.git --branch v$VERSION --single-branch


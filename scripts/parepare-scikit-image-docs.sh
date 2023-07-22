# conda install -c conda-forge latexmk -y
mkdir -p build
cd build
# if scikit-image folder not exist, clone it
[ ! -d scikit-image ] && git clone https://github.com/scikit-image/scikit-image.git --branch v$SCIKIT_IMAGE_VERSION --single-branch
cat ../scripts/latexpdf-fixed >> scikit-image/doc/Makefile



declare -a methods_names="iDetect";


## run from OpenBLAS lib ##
#OMP_NUM_THREADS=4 LD_PRELOAD=/opt/OpenBLAS/lib/libopenblas.so octave run_from_OpenBLAS.m


## normal execution ##
for method_name in $methods_names
do 
cd $method_name;
#OMP_NUM_THREADS=4 octave run_from_OpenBLAS.m;
OMP_NUM_THREADS=4 LD_PRELOAD=/opt/OpenBLAS/lib/libopenblas.so octave run_from_OpenBLAS.m
cd ..;
done

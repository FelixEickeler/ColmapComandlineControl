# Had this lying around maybe it helps someone. Really quick&dirty script. => felix.eickeler@tum.de

# Comandline Script for Automatic Reconstructions with Colmap

This is a small script that helped me doing mulitple reconstructions on a linux headleass machine. I will control colmap over the commandline and parse the "whole" ini-file. In the default ini there should be path added to create your own folder structure. There is log folder provided with the logs of the substeps (tail them for the current process).

## Options
Usage:
python ColmapCommandlineControl/main.py --path [path to folder] --ini [path to ini] 
(Full reconstruction. images are located in [path_to_folder]/images)

python ColmapCommandlineControl/main.py --path [path_to_folder] --step 111 --ini [path_to_ini] --sequential_matcher
(Only extraction, sequential_matching & mapping)


Following options are available:

| Option        | Argument      | Explaination  |
| ------------- |:------------- | :-----|
| --recursive      | None              | Takes multiple folder with the same structure and walks over each one for a reconstruction |
| --path           | [path_to_folder]  |   Path to the root directory. If recursive is not active it should be the root folder of the project that you want to reconstruct |
| --ini_path | [path_to_ini]      |    Path to the ini file. Please make note that there are some additional lines for the data structure! See the default.ini as an example |
 --steps        | binary string      | Binary representation of the steps you want to take: 1 is feature extraction, 2 is matching, 4 is mapping, 8 is image undistortion, 16 is dense stereo, 32 is dense fusing and 64 is a extraction of the statistic (json)  |  
 
For example a 001 will trigger the mapping process. A 101 the extraction & the mapping.
Currently only sequential and exhaustive matching is implemented. add --sequential_matcher to change to the sequential mode. Default is exhaustive.


These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Roadmap
+ more colmap features
+ saving all steps

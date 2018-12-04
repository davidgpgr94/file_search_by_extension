# Search by extension
## Introduction
> Find the files whose extension is indicated by the user.

> This script has been created by David González Pérez for the second job of the subject Informática Forense in Computer Engineer at UVa, Spain.

## Requirements
1. Python 2.7 installed into C:\Python27
2. Check that you have in the same directory the script and the file customsigs_GCK.txt. You can download it from https://www.garykessler.net/software/FileSigs_20151213a.zip

## Examples for use
### Find PDF files
> python search_by_extension.py -e pdf

> This will copy all PDF files found into ./search_by_dates_copy directory with the same relative directory structure

### Find JPG files and select which I want to copy
> python search_by_extension.py -e JPG -f

> This will show a UI where we could select the files to copy. Then, it will copy all selected files into ./search_by_dates_copy directory with the same relative directory structure

### Start searching for MP4 files from the directory specified by the -s option.
> python search_by_extension.py -e mp4 -s ../

> The start directory could be specified by absolut or relative path

### To specify the directory where we want to copy the found files, we have to use -t option.
> python search_by_extension.py -e mpg -t ../

> This will copy all the files found into directory ../ with the same relative directory structure

### To see which extensions are recognized, use the -i option
> python search_by_extension.py -i

### You can see the magic number of a recognized extension
> python search_by_extension.py -e sys -d

## All extensions supported are inside customsigs_GCK.txt. If you want change this library to other with more extensions, you should rename it (the new) with the name customsigs_GCK.txt
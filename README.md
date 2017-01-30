# fiwalkReader
Usage:  python3.x fiwalkReadyer.py -i [fiwalk output xml file] -o [output file in .xlsx format]
Simple python script to read fiwalk output xml files and extract all the filenames and MD5 hash values into an .xlsx file.


TODO:
1.  Create times for all allocated files (sort files based on times)
2.  File offset locations for all filenames (byte_runs
3.  add progressbar given some of these files get big.
4. List all files between various sizes (1-1024, 1025 - 4096, 4097 - 16384, 
increment every 4k (write function to increment size values every 4k)

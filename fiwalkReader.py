import sys
from optparse import OptionParser
from collections import defaultdict
import re
import subprocess
import os
import time
import progressbar
import xlsxwriter

try:
    import xml.etree.cElementTree as ET
except ImportError:
    print("[!] Python cElementTree module that is needed for parsing the XML output file from fiwalk!")

__author__ = 'JD Durick (labgeek@gmail.com)'
__date__ = 20161230
__version__= 0.01
__description__= "Simple python script to read fiwalk output xml files and extract all the filenames and MD5 hash values into an .xlsx file"

'''
TODO
1.  Create times for all allocated files (sort files based on times
4.  File offset locations for all filenames (byte_runs
3.  add progressbar given some of these files get big.
4. List all files between various sizes (1-1024, 1025 - 4096, 4097 - 16384, 
increment every 4k (write function to increment size values every 4k
'''

'''
Function name: usage()
Input:  nothing
Output: Writes usage information to command line
Author:  JD Durick
''' 
def usage ():
    print("########################################################################################")
    print("Author:  JD Durick")
    print("Created:  1/28/2017")
    print("Version:  0.01 Beta")
    print("Description:  Simple python script to read fiwalk output xml files and extract all")
    print("the filenames and MD5 hash values into an .xlsx file")
    print("python3.5 fiwalkReader.py [-i] <fiwalk output xml file> [-o] output file in .xlsx format")
    print("########################################################################################")

    sys.exit(0)
    
'''
Function name: writeManifest()
Input:  output file name and dictionary of filename to MD5 (key, value) pairs
Output: Creates .xlsx spreadsheet for the user
Author:  JD Durick
'''     
def writeManifest(output_file, hashDict):

    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
 
    dictLen = len(hashDict)
 
    worksheet.write(0,0, "Filename(s)")
    worksheet.write(0,1,"MD5 hash value")
    row = 1
    col = 0
    print("\nWriting data to manifest file called:  %s" % output_file)
    with progressbar.ProgressBar(max_value=dictLen+1) as progress:
        for key, value in hashDict.items():
             worksheet.write(row, col, key)
             worksheet.write(row, col+1, value)
             row += 1
             progress.update(row)
    workbook.close()
    print()


'''
Function name: parseFiwalk()
Input:  xml filename and output file name
Output: Parses Fiwalk output XML file and passes data constructs to manifestWriter()
Author:  JD Durick
''' 


def parseFiwalk(xml_file, outputFile):
    fn_tag = "{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}filename"
    fs_tag = "{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}filesize"
    hash_tag = "{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}hashdigest"
    creation_tag = "{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}crtime"
    mainDict = {}
    """
    Parse FIWALK DFXML with ElementTree
    """
    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()

    for child in root:
        #print(child.tag, child.attrib)
        for step_child in child:
            for grand_step_child in step_child:
                if(grand_step_child.tag == fn_tag):
                    fname = grand_step_child.text
                    #print(fname) 
                if(grand_step_child.tag == hash_tag):
                    if(grand_step_child.attrib['type'] == 'md5'):
                        #print("MD5 is %s" % grand_step_child.text)
                        mainDict[fname] = grand_step_child.text
                #print("%s and %s" % (grand_step_child.tag, grand_step_child.text))
                for great_grand_step_child in grand_step_child:
                    pass
    writeManifest(outputFile, mainDict) 
   
# Main
if __name__ == '__main__':
    parser = OptionParser()
    parser = OptionParser(usage="usage: %prog -f <inputfilename> -o <outputfilename>", version="%prog 0.1")
    parser.add_option("-i", "--inputfilename", dest="inputfilename", help="input file path", type="string")
    parser.add_option("-o", "--outputfilename", dest="outputfilename", help=" output file path", type="string")
    (options, args) = parser.parse_args()
    xml_file = options.inputfilename
    out_file = options.outputfilename
    
    if out_file.endswith('xlsx') & xml_file.endswith('.xml'):
        parseFiwalk(xml_file, out_file)
    else:
        usage()
        print("\nCheck the input and output file, file extensions need to be correct!\n")
        exit(0)
    
    
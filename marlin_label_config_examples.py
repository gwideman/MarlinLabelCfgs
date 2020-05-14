# for python3.5 or higher

#-----------------------------------
# Within Marlin project MarlinConfigurations, this program visits all folders
# under .../config/examples/*, processing each Configuration.h, Configuration_adv.h,
# _Bootscreen.h, and _Statusscreen.h, to insert:
#    #define STRING_CONFIG_EXAMPLES_DIR ("examples/<vendor>/<model>")
# ... or similar path leading to this file.
#
# Warning: The program modifies files in place, so be sure to back them up first if needed.
# Can be run multiple times if needed. Only modifies files which don't have
# correct #define STRING_CONFIG_EXAMPLES_DIR line.
#
# Invocation:
#-------------
# 1. Edit input_examples_dir and output_examples_dir to match your directory structure. 
#    The two paths can be the same, which causes the program to insert the new define into 
#    the existing files.
#    These directories must exist (but not necessarily the subdirs of the output directory).
#
# 2. python3 marlin_label_config_examples.py
# 
#-----------------------------------
# 2020-05-10 GMW original
#-----------------------------------
#
import sys
import os
from pathlib import Path
from distutils.dir_util import copy_tree  # for copy_tree, because shutil.copytree can't handle existing files, dirs

# Modify input_examples_dir and output_examples_dir for your installation
# No trailing slash
# Setting output_examples_dir = input_examples_dir causes the program to insert into the existing files.

input_examples_dir    = r'D:\ArduinoProjects\MarlinConfigurations\Configurations-import-2.0.x\configtest1\examples'
# output_examples_dir   = input_examples_dir
output_examples_dir   = r'D:\ArduinoProjects\MarlinConfigurations\Configurations-import-2.0.x\testout\configtest2\examples'



#-------------------------------------
files_to_mod = ['Configuration.h', 'Configuration_adv.h', '_Bootscreen.h', '_Statusscreen.h']

macro_name     = 'STRING_CONFIG_EXAMPLES_DIR'
def_macro_name = '#define ' + macro_name

filenum = 0
different_out_dir = not (output_examples_dir == input_examples_dir)

#----------------------------------------------
def process_file(subdir: str, filename: str):
#----------------------------------------------
    global filenum
    filenum += 1
    
    print(str(filenum) + '  ' + filename + ':  ' + subdir)
    
    def_line = (def_macro_name + ' ("'  + subdir.replace('\\', '/')  + '")')        
    
    #------------------------
    # Read file
    #------------------------
    lines = []
    infilepath = os.path.join(input_examples_dir, subdir, filename)    
    try:
        # UTF-8 because some files contain unicode chars
        with open(infilepath, 'rt', encoding="utf-8") as infile:
            lines = infile.readlines()
            
    except Exception as e:
        print('Failed to read file: ' + str(e) )
        raise Exception
    
    lines = [line.rstrip('\r\n') for line in lines]    
    
    #------------------------
    # Process lines
    #------------------------
    file_modified    = False
    
    # region state machine
    # -1 = before pragma once; 
    # 0 = region to place define; 
    # 1 = past region to place define    
    region      = -1      
    
    outlines = []
    for line in lines:
        outline = line
        
        if (region == -1) and (def_macro_name in line):
            outline       = None
            file_modified = True
            
        elif (region == -1) and ('pragma once' in line):
            region = 0
                
        elif (region == 0):
            if (line.strip() == ''):
                pass
            elif (def_macro_name in line):
                region = 1
                if line == def_line:   # leave it as is
                    pass
                else:
                    outline       = def_line
                    file_modified = True                
            else: # some other string
                outlines.append(def_line)
                outlines.append('')
                region = 1
                file_modified = True
                
        elif (region == 1):
            if (def_macro_name in line):
                outline       = None
                file_modified = True
            else:
                pass
    
        # end if
        if outline is not None:
            outlines.append(outline)              
    # end for

    #-------------------------
    #     Output file 
    #-------------------------
    outdir      = os.path.join(output_examples_dir, subdir)
    outfilepath = os.path.join(outdir, filename)

    if file_modified: 
        # Note: no need to create output dirs, as the initial copy_tree
        # will do that.
            
        print('  writing ' + str(outfilepath))
        try:
            # Preserve unicode chars; Avoid CR-LF on Windows.
            with open(outfilepath, "w", encoding="utf-8", newline='\n') as outfile:
                outfile.write("\n".join(outlines) ) 
                
        except Exception as e:
            print('Failed to write file: ' + str(e) )
            raise Exception
    else:
        print('  no change for ' + str(outfilepath))

#----------
def main():    
#----------
    global filenum
    global input_examples_dir
    global output_examples_dir
    filenum = 0
    
    #--------------------------------
    # Check for requirements 
    #--------------------------------
    input_examples_dir  = input_examples_dir.strip()
    input_examples_dir  = input_examples_dir.rstrip('\\/')
    output_examples_dir = output_examples_dir.strip()
    output_examples_dir = output_examples_dir.rstrip('\\/')
    
    for dir in [input_examples_dir, output_examples_dir]:        
        if not (os.path.exists(dir)):
            print('Directory not found: ' + dir)
            sys.exit(1)

    #--------------------------------
    # Copy tree if necessary.    
    #--------------------------------
    # This includes files that are not otherwise included in the 
    # insertion of the define statement.
    #
    if different_out_dir:
        print('Copying files to new directory: ' + output_examples_dir)
        try:
            copy_tree(input_examples_dir, output_examples_dir)
        except Exception as e:
            print('Failed to copy directory: ' + str(e) )
            raise Exception
    
    #-----------------------------
    # Find and process files 
    #-----------------------------
    len_input_examples_dir = len(input_examples_dir);
    len_input_examples_dir += 1
    
    for filename in files_to_mod:
        input_path = Path(input_examples_dir)
        filepathlist = input_path.rglob(filename)
        
        for filepath in filepathlist:
            fulldirpath = str(filepath.parent)
            subdir      = fulldirpath[len_input_examples_dir:]
                        
            process_file(subdir, filename) 
            
#==============            
print('--- Starting marlin_label_config_examples ---')
main()
print('--- Done ---')     
        
    





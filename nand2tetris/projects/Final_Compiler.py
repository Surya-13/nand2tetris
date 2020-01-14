####################################
##                                ##
##  NAME: B.V.S SUDHEENDRA        ##
##  ROLL NO: CS18B006             ##
##  COMPILER CODE                 ##
##  COMPLETED ON: 12-11-19        ##
##  LAST MODIFIED: 12-11-19       ##
####################################

import Compiler       # Importing my Compiler.py script
import sys            # Importing the necessary modules
arglist = sys.argv    # Storing the command line inputs into a List

# Call The Compiler.py for each file populating the .tok , .xml , .vm , .err files appropriately.

for i in range(2,len(arglist)):
    Compiler.make_file_txt(arglist[i])
    Compiler.make_file_tok(arglist[i])
    Compiler.make_file_xml(arglist[i])

sys.exit()     # Exit Successfully

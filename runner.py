import sys
from import_class import *

if __name__ == '__main__':
    # Call the class and run your code here
    #
    # You can assume that sys.argv[1] is the name
    # of the file to import and that it exists.
    #
    ic = import_class
    import_class.import_file(ic, sys.argv[1])
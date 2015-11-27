#!/usr/bin/python
"""
Test script for QuantEcon executables
=====================================
    <topic>/*.py 

This script uses a context manager to redirect stdout and stderr
to capture runtime errors for writing to the log file. It also
reports basic execution statistics on the command line (pass/fail)

Usage
-----
python _scripts_/test-py.py [WARNING: Always run from root level]

Default Logs 
------------
    <topic>/*.py => py_logs.txt
"""

import sys
import os
import glob
import subprocess
import re
import copy

from common import RedirectStdStreams, EXCLUDE

set_backend = "import matplotlib\nmatplotlib.use('Agg')\n"

def generate_temp(fl):
    """
    Modify file to supress matplotlib figures
    Preserve __future__ imports at front of file for python intertpreter
    """
    doc = open(fl).read()
    doc = set_backend+doc
    #-Adjust Future Imports-#
    if re.search(r"from __future__ import division", doc):
        doc = doc.replace("from __future__ import division", "")
        doc = "from __future__ import division\n" + doc
    return doc

def example_tests(log_path='./_scripts_/py-tests.log'):
    """
    Execute each Python Example File and check exit status.
    The stdout and stderr is also captured and added to the log file
    """
    
    test_files = glob.glob('./**/*.py')
    test_files.sort()
    filtered_test_files = copy.copy(test_files)
    for exclude in EXCLUDE:
        print("Excluding Pattern: %s"%exclude)
        for fln in test_files:
            if re.search(exclude, fln):
                print("Dropping: %s" % fln)
                filtered_test_files.remove(fln)
    passed = []
    failed = []
    #TODO: Update script so that python is run from within the folder to allow for local imports of files
    with open(log_path, 'w') as f:
        for i,fname in enumerate(filtered_test_files):
            print("Checking program %s (%s/%s) ..."%(fname,i,len(filtered_test_files)))
            #-Redirected Stream Context-#
            with RedirectStdStreams(stdout=f, stderr=f):
                print("---Executing '%s'---" % fname)
                sys.stdout.flush()
                #-Generate tmp File-#
                tmpfl = fname + "_"
                fl = open(tmpfl,'w')
                fl.write(generate_temp(fname))
                fl.close()
                #-Run Program-#
                exit_code = subprocess.call(["python",tmpfl], stderr=f)
                if exit_code == 0:
                    passed.append(fname)
                else:
                    failed.append(fname)
                #-Remove tmp file-#
                os.remove(tmpfl)
                print("---END '%s'---" % fname)
                sys.stdout.flush()
    #-Report-#
    print("Passed %i/%i: " %(len(passed), len(filtered_test_files)))
    if len(failed) == 0:
    	print("Failed Files:\n\tNone")
    else:
    	print("Failed Files:\n\t" + '\n\t'.join(failed))
    print(">> See %s for details" % log_path)
    os.chdir('../')
    return passed, failed


if __name__ == '__main__':
    print("----------------------")
    print("Running all *.py files")
    print("----------------------")
    example_tests(*sys.argv[1:])
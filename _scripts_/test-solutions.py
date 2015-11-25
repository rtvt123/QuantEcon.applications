#!/usr/bin/python
"""
Test script for QuantEcon ipynb Notebooks
==========================================
    <topic>/*.ipynb

Notes
-----
  1. This script should be run from the root level "python scripts/test-ipynb.py"

"""

import sys
import os
import glob
import subprocess
import copy

from common import RedirectStdStreams, EXCLUDE

def solutions_tests(log_path='./_scripts_/ipynb-tests.log'):
    """
    Execute each Jupyter Notebook
    """
    test_files = glob.glob('./**/*.ipynb')
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
    with open(log_path, 'w') as f:
            for i,fname in enumerate(filtered_test_files):
                print("Checking notebook %s (%s/%s) ..."%(fname,i,len(filtered_test_files)))
                with RedirectStdStreams(stdout=f, stderr=f):
                    print("---> Executing '%s' <---" % fname)
                    sys.stdout.flush()
                    #-Run Program-#
                    exit_code = subprocess.call(["runipy",fname], stdout=open(os.devnull, 'wb'), stderr=f)
                    sys.stderr.flush()
                    if exit_code == 0:
                        passed.append(fname)
                    else:
                        failed.append(fname)
                    print("---> END '%s' <---" % fname)
                    print
                    sys.stdout.flush()
    #-Report-#
    print("Passed %i/%i: " %(len(passed), len(filtered_test_files)))
    if len(failed) == 0:
    	print("Failed Notebooks:\n\tNone")
    else:
    	print("Failed Notebooks:\n\t" + '\n\t'.join(failed))
    print(">> See %s for details" % log_path)
    os.chdir('../')
    return passed, failed  


if __name__ == '__main__':
    print("-------------------------")
    print("Running all *.ipynb files")
    print("-------------------------")
    solutions_tests(*sys.argv[1:])
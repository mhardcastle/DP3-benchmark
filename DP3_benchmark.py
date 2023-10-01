#!/usr/bin/env python

import sys
import os
from tqdm import tqdm
import time

# This script is supplied with two arguments -- a working directory
# and an optional operation to carry out.
# Operations are: 'download' (download only) or 'benchmark' (the default).

def download():
    result=os.system('wget https://uhhpc.herts.ac.uk/~mjh/test.tar')
    if result!=0:
        raise RuntimeError('Download failed!')
    result=os.system('tar xvf test.tar')
    if result!=0:
        raise RuntimeError('Untar failed!')
    

if __name__=='__main__':
    print('Running toy DP3 benchmark')
    try:
        wd=sys.argv[1]
    except IndexError:
        print('A working directory must be supplied')
        raise

    os.chdir(wd)

    try:
        operation=sys.argv[2]
    except IndexError:
        operation='benchmark'

    if operation not in ['download','benchmark']:
        raise RuntimeError('Unknown operation %s specified' % operation)

    print('Running operation',operation)
    
    if operation=='download':
        download()
    elif operation=='benchmark':
        if not os.path.isdir('test.ms'):
            download()
        ts=0
        count=5
        for i in tqdm(range(count)):
            os.system('rm -r test2.ms')
            st=time.time()
            os.system('DP3 numthreads=8 msin=test.ms msout=test2.ms steps=[ave] msin.datacolumn=DATA msout.datacolumn=DATA ave.type=averager ave.freqstep=8')
            et=time.time()
            ts+=(et-st)
        print('Average execution time %f seconds' % (ts/count))
            

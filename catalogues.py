import sys
import os
from tqdm import tqdm
import time
import glob
from astropy.table import Table
import numpy as np

def download():
    result=os.system('wget https://lofar-surveys.org/public/DR2/catalogues/combined-release-v1.1-LM_opt_mass.fits')
    if result!=0:
        raise RuntimeError('Download failed!')

if __name__=='__main__':
    print('Running toy catalogue processing benchmark')
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
        times=[]
        count=5
        outfile='output.fits'
        for i in tqdm(range(count)):
            if os.path.isfile(outfile):
                os.unlink(outfile)
            st=time.time()
            t=Table.read('combined-release-v1.1-LM_opt_mass.fits')
            # compute a new column
            t['new_column']=t['L_144']/10**t['Mass_median']
            t.write(outfile)
            et=time.time()
            times.append(et-st)
        print('Average execution time %f seconds' % np.mean(times))
        print('Max execution time %f seconds' % np.max(times))
        print('Std dev of execution time %f seconds' % np.std(times))

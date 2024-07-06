import sys
import os
from tqdm import tqdm
import time
import glob
from astropy.io import fits
import numpy as np

def download():
    result=os.system('wget https://uhhpc.herts.ac.uk/~mjh/test.tar')
    if result!=0:
        raise RuntimeError('Download failed!')
    result=os.system('tar xvf test.tar')
    if result!=0:
        raise RuntimeError('Untar failed!')

if __name__=='__main__':
    print('Running toy FITS image processing benchmark')
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
        files=glob.glob('*-mosaic.fits')
        if len(files)==0:
            download()
            files=glob.glob('*-mosaic.fits')

        times=[]
        count=5
        for i in tqdm(range(count)):
            os.system('rm -r output.fits')
            st=time.time()
            for i,f in enumerate(files):
                hdu=fits.open(f)
                if not i:
                    sum=np.where(np.isnan(hdu[0].data),0,hdu[0].data)
                    count=np.where(np.isnan(hdu[0].data),0,1)
                else:
                    sum+=np.where(np.isnan(hdu[0].data),0,hdu[0].data)
                    count+=np.where(np.isnan(hdu[0].data),0,1)
            sum/=count
            hdu[0].data=sum
            hdu[0].header['OBJECT']='STACK'
            hdu.writeto('output.fits')
            et=time.time()
            times.append(et-st)
        print('Average execution time %f seconds' % np.mean(times))
        print('Max execution time %f seconds' % np.max(times))
        print('Std dev of execution time %f seconds' % np.std(times))

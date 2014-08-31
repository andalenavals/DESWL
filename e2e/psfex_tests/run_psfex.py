#! /usr/bin/env python
# Program to run single file in psfex

import argparse,os,glob,re,pyfits,random,copy
import numpy as np

parser = argparse.ArgumentParser(description='Run single file')

# Directory arguments
parser.add_argument('--cat_dir',
                    default='/astro/u/rarmst/soft/bin/',
                    help='location of sextrator executable')
parser.add_argument('--psf_dir',
                    default='/astro/u/rarmst/soft/bin/',
                    help='location of psfex executable')
parser.add_argument('--findstars_dir',
                    default='~/work/wl_trunk/src/',
                    help='location wl executables')
parser.add_argument('--out_dir',
                    default='./',
                    help='location of outputs')

# Exposure inputs
parser.add_argument('--file', default=None,
                   help='name of file')
parser.add_argument('--exp_match', default='',
                   help='regexp to search for files in exp_dir')
parser.add_argument('--exp_dir',default='./', 
                   help='directory to search for files')

# Configuration files
parser.add_argument('--config_cat',
                    default='/astro/u/rarmst/psfex_tests/default.sex',
                   help='sextractor config file')
parser.add_argument('--config_psf',
                    default='/astro/u/rarmst/psfex_tests/default.psfex',
                   help='psfex config file')
parser.add_argument('--config_findstars',
                    default='/astro/u/rarmst/psfex_tests/wl.config',
                   help='wl config file')
parser.add_argument('--param_file',
                    default='/astro/u/rarmst/psfex_tests/sex.param_psfex',
                   help='sextractor param file')
parser.add_argument('--filt_file',
                    default='/astro/u/rarmst/psfex_tests/sex.conv',
                   help='name of sextractor filter file')
parser.add_argument('--star_file',
                    default='/astro/u/rarmst/psfex_tests/sex.nnw',
                   help='name of sextractor star file')

# file options
parser.add_argument('--rm_files',default=0, type=int,
                   help='remove unpacked files after finished')
parser.add_argument('--split',default=0,
                   help='split sextractor files into two')
parser.add_argument('--run_psfex',default=0,
                   help='run psfex on files')
parser.add_argument('--use_findstars',default=0,type=int,
                   help='use findstars results in psfex')
parser.add_argument('--mag_cut',default=-1,type=float,
                   help='remove the top mags using mag_auto')
parser.add_argument('--nstars',default=10,type=int,
                   help='use median of brightest nstars for min mag')
parser.add_argument('--force',default=0,type=int,
                   help='force creation of files that exist')


args = parser.parse_args()

files=[]

# set the exp_dir to the absolute path because 
args.exp_dir=os.path.abspath(args.exp_dir)

# if a whole directory is asked for than we add all of them to the
# list
if(args.file is None):
    for filename in glob.glob('%s/%s'%(args.exp_dir,args.exp_match)):
        files.append(filename)
else:
    base=os.path.splitext(os.path.basename(args.file))[0]
    files.append(args.file)

if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)

print files

for file in files:

    m=file.split('.')
    # find out if the file is fpacked by the extension
    ext=m[-1]

    # find the base filename
    if ext=='fz':
        base_file=os.path.splitext(os.path.basename(file))[0]
    else:
        base_file=os.path.basename(file)
    print 'Processing '+base_file

    # remove the .fits extension
    m=re.search('(.*)\.fits.*',base_file)
    base_name=''
    if m:
        base_name=m.group(1)
    else:
        print "Cannot find base name for "+base_name+" skipping"
        continue

    # check to see if we need to funpack
    did_unpack=False

    if(ext=='fz'):
        funpack_file=args.out_dir+'/'+base_file

        # If an unpacked file does not exist in the output directory 
        # or if we are forcing a run, unpack it into the output directory
        if not os.path.exists(funpack_file) or args.force:
        
            did_unpack=True
            
            cmd='funpack -O %s %s' % (funpack_file,file)
            ok=os.system(cmd)
            print 'running '+cmd
            file=funpack_file
                
    else:
        # If the file is not fpacked, make a symlink into the output directory
        if not os.path.exists(args.out_dir+'/'+base_file):
            # make symlink to local directory
            os.system('ln -s %s %s'%(file,args.out_dir))
            file=args.out_dir+'/'+base_file
    print file
    hdu=0
    cat_file=args.out_dir+'/'+base_file
    cat_file=cat_file.replace('.fits','_psfcat.fits')

    # if the sextractor catalog does not exist or we are forcing recreate it
    if not os.path.exists(cat_file) or args.force:

        # extract the saturation level, this is how desdm runs sextractor
        pyfile=pyfits.open(file)
        sat=-1
        try:
            sat=pyfile[hdu].header['SATURATE']
        except:
            pass
            
        cat_cmd="{cat_dir}/sex {img_file}[0] -c {cat_config} -CATALOG_NAME {cat_file} -CATALOG_TYPE FITS_LDAC -WEIGHT_TYPE MAP_WEIGHT -WEIGHT_IMAGE {img_file}[2] -PARAMETERS_NAME {param_file} -FILTER_NAME {filter_file}  -STARNNW_NAME {star_file} -DETECT_MINAREA 3".format(cat_dir=args.cat_dir, img_file=file, cat_config=args.config_cat,cat_file=cat_file,param_file=args.param_file,filter_file=args.filt_file,star_file=args.star_file)
        
        if sat>0:
            cat_cmd+=' -SATUR_LEVEL %f'%sat
        os.system(cat_cmd)
        print 'running '+cat_cmd

    # if we want to use only the stars selected by findstars
    if args.use_findstars:
        
        star_file=args.out_dir+'/'+base_name+'_findstars.fits'    

        # run find stars
        if not os.path.exists(star_file) or args.force:
            findstars_cmd='%s/findstars %s root=%s cat_ext=_psfcat.fits stars_file=%s input_prefix=%s/'%(args.findstars_dir,args.config_findstars,base_name,star_file,args.out_dir)
            print findstars_cmd
            os.system(findstars_cmd)
            

        old_cat=cat_file
        cat_file=cat_file.replace('psfcat','psfcat_findstars')

        if not os.path.exists(cat_file.replace('psfcat','psfcat_findstars')) or args.force:
            initfile=pyfits.open(old_cat)
            
            findstars_file=pyfits.open(star_file)
            mask=findstars_file[1].data['star_flag']==1
            # create new sextractor file with only these entries
            data=initfile[2].data[mask]
        
            # Need to make different copy of these to not fail
            hdu1=copy.copy(initfile[0])
            hdu2=copy.copy(initfile[1])
            
            hdu = pyfits.BinTableHDU(data)
            hdu.name='LDAC_OBJECTS'
            list=pyfits.HDUList([hdu1,hdu2, hdu])

            list.writeto(cat_file,clobber=True)


    # If we want to cut the brighest magnitudes
    if args.mag_cut>0:
        cut_file=cat_file.replace('psfcat','psfcat_mag_%0.1f'%args.mag_cut)
        if (not os.path.exists(cut_file) or args.force):
            # get the brightest 10 mags that have flags=0 and take the median just in case some were
            # selected
            name=cat_file
            hdu=2
            
            pyfile=pyfits.open(name)
            flags_mask=pyfile[hdu].data['FLAGS']==0
            mags=pyfile[hdu].data['MAG_AUTO'][flags_mask]
            mags.sort()
            min_star=np.median(mags[0:args.nstars])
            
            mag_mask=pyfile[hdu].data['MAG_AUTO']>min_star+args.mag_cut
            
            data=pyfile[hdu].data[mag_mask]
            
            cat_file=cut_file
            
            # Need to make different copy of these to not fail
            hdu1=copy.copy(pyfile[0])
            hdu2=copy.copy(pyfile[1])
            
            hdu = pyfits.BinTableHDU(data)
            hdu.name='LDAC_OBJECTS'
            list=pyfits.HDUList([hdu1,hdu2, hdu])
            list.writeto(cat_file,clobber=True)

    
    psf_file=cat_file.replace('fits','psf')
    catout_file=cat_file.replace('fits','used.fits')
    
    if args.run_psfex and (not os.path.exists(psf_file) or args.force):
        psf_cmd=('%s/psfex %s -c %s -OUTCAT_TYPE FITS_LDAC -OUTCAT_NAME %s' % (args.psf_dir,cat_file,args.config_psf,catout_file))
        print psf_cmd
        os.system(psf_cmd)
        
    # This will split the catalog into two different samples
    # and run psfex on all of them
    if args.split>0:

        initfile=pyfits.open(cat_file)
        nob=len(initfile[2].data)
        indexes=random.sample(range(nob), nob)
        index1=indexes[:nob/2]
        index2=indexes[nob/2:]

        data1=initfile[2].data[index1]
        data2=initfile[2].data[index2]

        name1=cat_file.replace('psfcat','psfcat1')
        name2=cat_file.replace('psfcat','psfcat2')

        # Need to make different copy of these to not fail
        hduf1=copy.copy(initfile[0])
        hduf2=copy.copy(initfile[1])
        hdus1=copy.copy(initfile[0])
        hdus2=copy.copy(initfile[1])

        hdu2 = pyfits.BinTableHDU(data2)
        hdu2.name='LDAC_OBJECTS'
        list2=pyfits.HDUList([hduf1,hduf2, hdu2])
        list2.writeto(name2,clobber=True)


        hdu1 = pyfits.BinTableHDU(data1)
        hdu1.name='LDAC_OBJECTS'
        list1=pyfits.HDUList([hdus1,hdus2, hdu1])
        list1.writeto(name1,clobber=True)

        if args.run_psfex:

            psf_cmd=('%s/psfex %s -c %s' % (args.psf_dir,name1,args.config_psf))
            print psf_cmd
            os.system(psf_cmd)
                        
            psf_cmd=('%s/psfex %s -c %s ' % (args.psf_dir,name2,args.config_psf))
            print psf_cmd
            os.system(psf_cmd)
                    

    if did_unpack and args.rm_files:

        rm_cmd='rm %s'%file
        print rm_cmd
        os.system(rm_cmd)
        


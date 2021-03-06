# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Example of script to parcellate mutli-subject data
author: Bertrand Thirion, 2005-2009
"""
import os.path as op
from numpy import array
import tempfile

from nipy.labs.spatial_models.parcel_io import parcel_input, \
    write_parcellation_images, parcellation_based_analysis
from nipy.labs.spatial_models.hierarchical_parcellation import hparcel
import get_data_light

# Get the data
nb_subj = 12
subj_id = ['subj_%02d'%s for s in range(nb_subj)]
nbeta = '%04d'%29
data_dir = op.expanduser(op.join('~', '.nipy', 'tests', 'data',
                                 'group_t_images'))
mask_images = [op.join(data_dir,'mask_subj%02d.nii'%n)
               for n in range(nb_subj)]

learn_images = [op.join(data_dir,'spmT_%s_subj_%02d.nii'%(nbeta , n))
                for n in range(nb_subj)]
missing_file = array([op.exists(m)==False 
                      for m in mask_images + learn_images]).any()
learn_images = [[m] for m in learn_images]

if missing_file:
    get_data_light.get_it()

# parameter for the intersection of the mask
ths = .5

# possibly, dimension reduction can performed on the input data
# (not recommended)
fdim = 3

# number of parcels
nbparcel = 500

# write dir
swd = tempfile.mkdtemp()

# prepare the parcel structure
domain, ldata = parcel_input(mask_images, learn_images, ths, fdim)

# run the algorithm
fpa = hparcel(domain, ldata, nbparcel, verbose=1)
#fpa,  prfx0 = hparcel(domain, ldata, nbparcel, nb_perm=5, niter=5, verbose=1)


#produce some output images
write_parcellation_images(fpa, subject_id=subj_id, swd=swd)

# do some parcellation-based analysis:
# take some test images whose parcel-based signal needs to be assessed 
test_images = [op.join(data_dir,'spmT_%s_subj_%02d.nii'%(nbeta , n))
                for n in range(nb_subj)]

# compute and write the parcel-based statistics
rfx_path = op.join(swd, 'prfx_%s.nii'%nbeta)
parcellation_based_analysis(fpa, test_images, 'one_sample', rfx_path=rfx_path)
print "Wrote everything in %s" % swd

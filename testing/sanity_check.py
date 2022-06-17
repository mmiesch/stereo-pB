"""
read in a few images and plot, for a sanity check
"""

import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm

from astropy.io import fits

dir = '../data/pBcom/'

files = list(filter(os.path.isfile, glob.glob(dir + "*.fts")))
files = sorted(files)

N = len(files)

dix = (0,N-2)

#------------------------------------------------------------------------------

fig = plt.figure(figsize=[18,10])

scale = (0,1.e-9)
dscale = (-1.e-11,1.e-11)

cmap = plt.get_cmap('stereocor2')

#------------------------------------------------------------------------------
print(80*'-')

idx1 = dix[0]

print(files[idx1])

hd = fits.open(files[idx1])[0]
im1 = hd.data

ax = fig.add_subplot(2,3,1)
plt.imshow(im1, vmin=scale[0], vmax=scale[1], cmap = cmap)

#------------------------------------------------------------------------------

idx2 = idx1 + 4

print(files[idx2])

hd = fits.open(files[idx2])[0]
im2 = hd.data

ax = fig.add_subplot(2,3,2)
plt.imshow(im2, vmin=scale[0], vmax=scale[1], cmap = cmap)

#------------------------------------------------------------------------------
im = im2 - im1

print(f"{np.min(im)} {np.max(im)}")

ax = fig.add_subplot(2,3,3)
plt.imshow(im, vmin=dscale[0], vmax=dscale[1], cmap = 'bone')

#------------------------------------------------------------------------------

print(80*'-')

idx1 = dix[1]

print(files[idx1])

hd = fits.open(files[idx1])[0]
im1 = hd.data

ax = fig.add_subplot(2,3,4)
plt.imshow(im1, vmin=scale[0], vmax=scale[1], cmap = cmap)

#------------------------------------------------------------------------------

idx2 = idx1 + 1

print(files[idx2])

hd = fits.open(files[idx2])[0]
im2 = hd.data

ax = fig.add_subplot(2,3,5)
plt.imshow(im2, vmin=scale[0], vmax=scale[1], cmap = cmap)

#------------------------------------------------------------------------------\
im = im2 - im1

print(f"{np.min(im)} {np.max(im)}")

ax = fig.add_subplot(2,3,6)
plt.imshow(im, vmin=dscale[0], vmax=dscale[1], cmap = 'bone')

#------------------------------------------------------------------------------
print(80*'-')

plt.show()
"""
Compare the pBcom images with comparable tB images
"""

import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import sunpy.visualization.colormaps as cm

from astropy.io import fits
from astropy.time import Time

#------------------------------------------------------------------------------
# composite pB files

dir = '../data/pBcom/'

files = list(filter(os.path.isfile, glob.glob(dir + "*.fts")))
files = sorted(files)

N = len(files)

pidx = 0
didx = 2

#------------------------------------------------------------------------------
# tB files

dir = '../data/img/'

tbfiles = list(filter(os.path.isfile, glob.glob(dir + "*.fts")))
tbfiles = sorted(tbfiles)

#------------------------------------------------------------------------------

fig = plt.figure(figsize=[18,10])

scale = (0,2.e-9)
dscale = (-1.e-11,1.e-11)

tbscale = (1.7e3,3.e3)
tbdscale = (-9.e0,9.e0)

cmap = plt.get_cmap('stereocor2')

#------------------------------------------------------------------------------
print(80*'-')

idx1 = pidx

print(files[idx1])

hd = fits.open(files[idx1])[0]
im1 = hd.data
t1 = Time(hd.header['DATE'])

ax = fig.add_subplot(2,3,1)
plt.imshow(im1, vmin=scale[0], vmax=scale[1], cmap = cmap)
plt.title(t1.value)

#------------------------------------------------------------------------------

idx2 = idx1 + didx

print(files[idx2])

hd = fits.open(files[idx2])[0]
im2 = hd.data
t2 = Time(hd.header['DATE'])

ax = fig.add_subplot(2,3,2)
plt.imshow(im2, vmin=scale[0], vmax=scale[1], cmap = cmap)
plt.title(t2.value)

#------------------------------------------------------------------------------
im = im2 - im1

print(f"{np.min(im)} {np.max(im)}")

ax = fig.add_subplot(2,3,3)
plt.imshow(im, vmin=dscale[0], vmax=dscale[1], cmap = 'bone')

#------------------------------------------------------------------------------
# find tB images at closest times to t1 and t1

print(f"{t1.gps} {t2.gps}")

tbtimes = []

for f in tbfiles:
    hdu = fits.open(f)[0]
    tbtimes.append(Time(hdu.header['DATE']).gps)

t = np.array(tbtimes)

dt = np.abs(t - t1.gps)
idx1 = np.where(dt == np.min(dt))[0][0]
tbfile1 = tbfiles[idx1]
print(f"idx1 {idx1} {dt[idx1]} {np.min(dt)} {tbfile1}")

dt = np.abs(t - t2.gps)
idx2 = np.where(dt == np.min(dt))[0][0]
tbfile2 = tbfiles[idx2]
print(f"idx2 {idx2} {dt[idx2]} {np.min(dt)} {tbfile2}")

#------------------------------------------------------------------------------

print(80*'-')

print(tbfile1)

hd = fits.open(tbfile1)[0]
tbim1 = hd.data
tbt1 = Time(hd.header['DATE'])

print(f"{np.min(tbim1)} {np.max(tbim1)}")

ax = fig.add_subplot(2,3,4)
plt.imshow(tbim1, vmin=tbscale[0], vmax=tbscale[1], cmap = cmap)
plt.title(tbt1.value)

#------------------------------------------------------------------------------

print(tbfile2)

hd = fits.open(tbfile2)[0]
tbim2 = hd.data
tbt2 = Time(hd.header['DATE'])

ax = fig.add_subplot(2,3,5)
plt.imshow(tbim2, vmin=tbscale[0], vmax=tbscale[1], cmap = cmap)
plt.title(tbt2.value)

#------------------------------------------------------------------------------
im = np.float64(tbim2) - np.float64(tbim1)

print(f"{np.min(im)} {np.max(im)}")

ax = fig.add_subplot(2,3,6)
plt.imshow(im, vmin=tbdscale[0], vmax=tbdscale[1], cmap = 'bone')

#------------------------------------------------------------------------------
print(80*'-')

plt.show()

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
import sunpy.visualization.colormaps as cm

#------------------------------------------------------------------------------
# define files

tb_dir = 'data/img/'
pb_dir = 'data/seq/'

tb_file  = '20220601_035424_d7c2A.fts'
tb_file2 = '20220601_042424_d7c2A.fts'

pb_files = ['20220601_040835_n7c2A.fts', \
            '20220601_040905_n7c2A.fts', \
            '20220601_040935_n7c2A.fts'
]

#------------------------------------------------------------------------------
# Read total brightness file

print(80*'-')

tb_hdu = fits.open(tb_dir+tb_file)[0]

tb = tb_hdu.data

print(f"tb file polarization {tb_hdu.header['POLAR']}")
print(f"tb data type {tb.dtype}")
print(f"tb range {np.min(tb)} {np.max(tb)}")

#------------------------------------------------------------------------------
# Read polarized brightness files

print(80*'-')

pb = 0.0

firstpass = True

for file in pb_files:
    pb_hdu = fits.open(pb_dir+file)[0]
    if firstpass:
        pb = pb_hdu.data
        firstpass = False
    else:
        pb += pb_hdu.data
    print(f"pb file polarization {pb_hdu.header['POLAR']}")

pbf = 2.0 * pb.astype('float')/3.0
pb = pbf.astype('uint16')

print(f"tb data type {pb.dtype}")
print(f"tb range {np.min(pb)} {np.max(pb)}")

print(80*'-')

#------------------------------------------------------------------------------

db = np.abs(pb - tb)

print(f"db range {np.min(db)} {np.max(db)} {np.mean(db)}")

print(80*'-')

#------------------------------------------------------------------------------
# compare with difference between two nearby tb images

tb_hdu2 = fits.open(tb_dir+tb_file2)[0]

tb2 = tb_hdu2.data

tbdiff = np.abs(tb2 - tb)

print(f"tbdiff range {np.min(tbdiff)} {np.max(tbdiff)} {np.mean(tbdiff)}")

print(80*'-')

#------------------------------------------------------------------------------

#cmap = plt.get_cmap('stereocor2')
cmap = plt.get_cmap('soholasco2')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(16, 16), sharex=True,
                               sharey=True)

scale  = [0,20000]
dscale = [0,10000]

ax1.imshow(tb, cmap=cmap, vmin = scale[0], vmax = scale[1])
ax1.set_title('tB')
ax1.axis('off')
ax2.imshow(pb, cmap=cmap, vmin = scale[0], vmax = scale[1])
ax2.set_title('pB')
ax2.axis('off')
ax3.imshow(db, cmap=cmap, vmin = dscale[0], vmax = dscale[1])
ax3.set_title('difference')
ax3.axis('off')
ax4.imshow(tbdiff, cmap=cmap, vmin = dscale[0], vmax = dscale[1])
ax4.set_title('tbdiff')
ax4.axis('off')

plt.show()
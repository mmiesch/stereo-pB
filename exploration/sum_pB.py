
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
import sunpy.visualization.colormaps as cm

#------------------------------------------------------------------------------
def nonzero_stats(im):

   nzero = np.ma.masked_equal(im, 0)
   return(nzero.min(), nzero.max(), nzero.mean(), np.ma.median(nzero))

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

vmin, vmax, mean, med = nonzero_stats(tb)

tb_time = tb_hdu.header['DATE']

print(f"tb file polarization {tb_hdu.header['POLAR']}")
print(f"tb data type {tb.dtype}")
print(f"tb range {vmin} {vmax}")
print(f"tb scale {mean} {med}")

#------------------------------------------------------------------------------
# Read polarized brightness files

print(80*'-')

pb = 0.0

firstpass = True

pb_time = []

for file in pb_files:
    pb_hdu = fits.open(pb_dir+file)[0]
    if firstpass:
        pb = pb_hdu.data
        firstpass = False
    else:
        pb += pb_hdu.data
    print(f"pb file polarization {pb_hdu.header['POLAR']}")
    pb_time.append(pb_hdu.header['DATE'])
    print(f"{pb_hdu.header['DATE']}")

pbf = 2.0 * pb.astype('float')/3.0
pb = pbf.astype('uint16')

vmin, vmax, mean, med = nonzero_stats(pb)


print(f"pb data type {pb.dtype}")
print(f"pb range {vmin} {vmax}")
print(f"pb scale {mean} {med}")

print(80*'-')

#------------------------------------------------------------------------------

db = pb.astype('int64') - tb.astype('int64')

vmin, vmax, mean, med = nonzero_stats(db)

print(f"db range {vmin} {vmax}")
print(f"db scale {mean} {med}")

print(80*'-')

#------------------------------------------------------------------------------
# compare with difference between two nearby tb images

tb_hdu2 = fits.open(tb_dir+tb_file2)[0]

tb2 = tb_hdu2.data

tb2_time = tb_hdu2.header['DATE']

tbdiff = tb2.astype('int64') - tb.astype('int64')

vmin, vmax, mean, med = nonzero_stats(tbdiff)

print(f"tbdiff range {vmin} {vmax}")
print(f"tbdiff scale {mean} {med}")

db2 = pb.astype('int64') - tb2.astype('int64')

print(80*'-')

#------------------------------------------------------------------------------

cmap = plt.get_cmap('stereocor2')
cmap2 = plt.get_cmap('soholasco2')

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(ncols=3, nrows=2, figsize=(21, 14), sharex=True,
                               sharey=True)

scale  = [0,20000]
dscale = [-10000,10000]

ax1.imshow(tb, cmap=cmap, vmin = scale[0], vmax = scale[1])
ax1.set_title(f'tB {tb_time}')
ax1.axis('off')

ax2.imshow(pb, cmap=cmap, vmin = scale[0], vmax = scale[1])
ax2.set_title(f'pB {pb_time[0]} - {pb_time[2]}')
ax2.axis('off')

ax3.imshow(db, cmap=cmap2, vmin = dscale[0], vmax = dscale[1])
ax3.set_title('difference (tb time 1)')
ax3.axis('off')

ax4.imshow(tb2, cmap=cmap, vmin = scale[0], vmax = scale[1])
ax4.set_title(f'tB {tb2_time}')
ax4.axis('off')

ax5.imshow(tbdiff, cmap=cmap2, vmin = -10, vmax = 10)
#ax5.imshow(tbdiff, cmap=cmap2)
ax5.set_title('tB difference')
ax5.axis('off')

ax6.imshow(db, cmap=cmap2, vmin = dscale[0], vmax = dscale[1])
ax6.set_title('difference (tb time 2)')
ax6.axis('off')

plt.show()
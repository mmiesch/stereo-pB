pro combine_stereo_pb, file1, file2, file3, time, outfile

; the time should be passed in jd format

secchi_prep, [file1,file2,file3], h, a, /smask

header = h[1]

image = (2./3.d0)*total(a,3)

; time was passed in julian date: convert to iso
mjd=double(time)-2400000.5d
mjd_str={ mjd: floor(mjd), time: (mjd-floor(mjd))*8.64d7 }
header.date_obs = anytim2utc(/ccsds,mjd_str)

sccwritefits, outfile, image, header

end

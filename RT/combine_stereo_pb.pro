pro combine_stereo_pb, file1, file2, file3, time, outfile

; the time should be passed as a string in iso format for
; proper inclusion in the header, e.g.
; '2022-06-14T21:14:54.040'

print,"In combine_stereo_pb: "
print,file1
print,file2
print,file3

secchi_prep, [file1,file2,file3], h, a, /smask

h = h[1]

image = (2./3.d0)*total(a,3)

; time was passed in julian date: convert to iso
mjd=double(time)-2400000.5d
mjd_str={ mjd: floor(mjd), time: (mjd-floor(mjd))*8.64d7 }
h.date = anytim2utc(/ccsds,mjd_str)

help, h.date

sccwritefits, outfile, image, h

end
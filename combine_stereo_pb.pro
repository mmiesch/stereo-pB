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

;times = [h[0].date, h[1].date, h[2].date]
image = (2./3.d0)*total(a,3)

mjd = time - 2400000.5d
mjd_str={ mjd: floor(mjd), time: (mjd-floor(mjd))*8.64d7 }
;h.date = anytim2utc(/ccds,mjd_str)

;print,anytim2utc(/ccds,mjd_str)

print,"AAAAAA "
jd=systime(/julian,/utc)
help,jd
help,time
;mjd=jd-2400000.5d
mjd=double(time)-2400000.5d
mjd_str={ mjd: floor(mjd), time: (mjd-floor(mjd))*8.64d7 }
print,anytim2utc(/ccsds,mjd_str)

;print, h.date


;sccwritefits, outfile, image, h

end
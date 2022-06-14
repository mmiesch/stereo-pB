pro combine_stereo_pb, file1, file2, file3

print,"In combine_stereo_pb: "
print,file1
print,file2
print,file3

secchi_prep, [file1,file2,file3], h, a, /smask

times = [h[0].date, h[1].date, h[2].date]
image = (2./3.d0)*total(a,3)

print,h[0].date
help,h[0].date

;h = h[1]
;h.date = date
;sccwritefits, outfilename, image, h

end
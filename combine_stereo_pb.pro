pro combine_stereo_pb, file1, file2, file3

print,"In combine_stereo_pb: "
print,file1
print,file2
print,file3

secchi_prep, [file1,file2,file3], h, a, /smask

end
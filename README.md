# stereo-pB

The software in this repository is intended to process STEREO-A polarized brightness (pB) beacon images for use with the SWPC CME Analysis Tool (CAT).

In nominal operations, the CAT uses total brightness (tB) images from the STEREO-A beacon.  The capability to also use pB images leverages the full cadence of observations available from the beacon.  This can be a valuable source of information that was previously untapped, particularly during intervals when only pB observations are executed.

The contents of this repository are as follows:

---
## RT directory

This is the code that is intended for real-time operational use, including the following files:

* `watch_dir.py`: the principal process for operational execution: automated processing of files in a target directory

* `process_dir.py`: An alternaive to `watch_dir.py`, this provides the ability to manually process all the pB files in a target directory

* `stereo_process_pB.py`: This is mainly a python wrapper for the IDL program `combine_stereo_pB,.py`.  Called by `watch_dir.py` and `process_dir.py`

* `combine_stereo_pb.pro`: The IDL code that processes the pB files using the SolarSoft routine `secchi_prep.pro`, developed by STEREO-A/COR2 vendor NRL

---
## testing directory

This code is used for testing the RT functions.  It's a bit less polished.

---
## exploration directory

This code is to a large extent the first code written, indended to explore the nature of the data.
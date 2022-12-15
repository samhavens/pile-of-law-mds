# Pile of Law MDS

This code downloads The Pile of Law from the HF Hub and converts it to MDS format. It does not use HF Datasets to do the downloading, as that was doing additional processing and slowing things down.

It then converts to MDS format, which on 64 CPUs takes about 1min per GB output, so the conversion takes ~270 CPU*hours to complete.

You can use `test_load.py` to make sure that the resulting MDS file works.

Then the MDS folder, `mds-pol` by default, needs to be uploaded to S3
shell=/bin/bash

local_version := $(shell python3 -m setuptools_scm)
tmpdir := $(shell mktemp -d)

test_local:
	atol-qc-raw-shortread \
		--in test-data/AG_P8P5C_S101_L002_R1_001.fastq.gz \
		--in2 test-data/AG_P8P5C_S101_L002_R2_001.fastq.gz \
		--out test-output/r1.fq.gz \
		--out2 test-output/r2.fq.gz \
		-a test-data/bbmap_39.01_adaptors.fa \
		--stats test-output/stats.json \
		--threads 8



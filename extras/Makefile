shell=/bin/bash

local_version := $(shell python3 -m setuptools_scm)
tmpdir := $(shell mktemp -d)
branch := $(shell git rev-parse --abbrev-ref HEAD)

test_local:
	atol-qc-raw-shortread \
		--in test-data/AG_P8P5C_S101_L002_R1_001.fastq.gz \
		--in2 test-data/AG_P8P5C_S101_L002_R2_001.fastq.gz \
		--cram test-output/local/AG_P8P5C_S101_L002.cram  \
		--dataset_id "AG_P8P5C" \
		--hic_kit "arima" \
		-a test-data/bbmap_39.01_adaptors.fa test-data/bbmap_39.01_adaptors2.fa \
		--stats test-output/local/stats.json \
		--logs test-output/local/logs \
		--threads 14

full_test:
	atol-qc-raw-shortread \
		--in 350768_AusARG_BRF_HCN7WDRXY_S3_L001_R1_001.fastq.gz \
		--in2 350768_AusARG_BRF_HCN7WDRXY_S3_L001_R2_001.fastq.gz \
		--adaptors test-data/bbmap_39.01_adaptors.fa \
		--cram test-output/full/350768_AusARG_BRF_HCN7WDRXY_S3_L001.cram \
		--stats test-output/full/stats.json \
		--logs test-output/full/logs \
		--threads 14
		
changelog: CHANGELOG.md

CHANGELOG.md: .git/index
	gitchangelog > $(tmpdir)/CHANGELOG.md
	apptainer exec docker://davidanson/markdownlint-cli2:v0.13.0 \
	markdownlint-cli2 \
	--fix \
	:$(tmpdir)/CHANGELOG.md || true
	mv $(tmpdir)/CHANGELOG.md ./CHANGELOG.md
	git add CHANGELOG.md
	git commit -m 'changelog !cosmetic'
	git push origin $(branch)

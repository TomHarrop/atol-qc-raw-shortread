# atol-qc-raw-shortread

Run short read QC on Hi-C or other Illumina reads.

1. Check read pairing
2. Trim adaptors
3. Output stats

## Installation: Use the [BioContainer](https://quay.io/repository/biocontainers/atol-qc-raw-shortread?tab=tags)

*e.g.* with Apptainer/Singularity:

```bash
apptainer exec \
  docker://quay.io/biocontainers/atol-qc-raw-shortread:0.1.0 \
  atol-qc-raw-shortread  
  
```

## Usage

```bash
atol-qc-raw-shortread \
    --in data/r1.fastq.gz \
    --in2 data/r2.fastq.gz \
    --adaptors resources/adaptors.fa \
    --out results/r1.fq.gz \
    --out2 results/r2.fq.gz \
    --stats results/stats.json 
```

14 threads seems to be a good number on a fast disk. Reads are written to
`fq.gz`, which is presumably IO bound at some point.

### Full usage

```
usage: atol-qc-raw-shortread [-h] [-t THREADS] [-n] [--qtrim | --no-qtrim] [--trimq TRIMQ] --in R1 --in2 R2 [-a ADAPTORS [ADAPTORS ...]] --out R1_OUT --out2 R2_OUT --stats STATS [--logs LOGS_DIRECTORY]

options:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
  -n                    Dry run
  --qtrim, --no-qtrim   Trim right end of reads to remove bases with quality below trimq.
  --trimq TRIMQ         Regions with average quality BELOW this will be trimmed, if qtrim is enabled

Input:
  --in R1               Read 1 input
  --in2 R2              Read 2 input
  -a ADAPTORS [ADAPTORS ...], --adaptors ADAPTORS [ADAPTORS ...]
                        FASTA file(s) of adaptors. Multiple adaptor files can be used.

Output:
  --out R1_OUT          Read 1 output
  --out2 R2_OUT         Read 2 output
  --stats STATS         Stats output (json)
  --logs LOGS_DIRECTORY
                        Log output directory. Default: logs are discarded.
```

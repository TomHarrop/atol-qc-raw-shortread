# atol-qc-raw-shortread

Run short read QC on Hi-C or other Illumina reads.

1. Check read pairing
2. Trim adaptors
3. Output stats

## Installation: Use the [BioContainer](https://quay.io/repository/biocontainers/atol-qc-raw-shortread?tab=tags)

*e.g.* with Apptainer/Singularity:

```bash
apptainer exec \
  docker://quay.io/biocontainers/atol-qc-raw-shortread:0.1.6--pyhdfd78af_0 \
  atol-qc-raw-shortread  
  
```

## Usage

```bash
atol-qc-raw-shortread \
    --in data/r1.fastq.gz \
    --in2 data/r2.fastq.gz \
    --adaptors resources/adaptors.fa \
    --cram results/reads.cram \
    --stats results/stats.json 
```

The trimming is done by `bbduk.sh`, which scales well. 14 threads works well in
testing.

BBMap's included adaptor file is inside the container under BBMap's
installation directory, `/usr/local/opt`. To use that file, pass `--adaptors
/path/to/resources/adapters.fa`.

### Full usage

```
usage: atol-qc-raw-shortread [-h] [-t THREADS] [-n] [--qtrim | --no-qtrim] [--trimq TRIMQ] [--dataset_id DATASET_ID] [--hic_kit HIC_KIT] --in R1
                             --in2 R2 [-a ADAPTORS [ADAPTORS ...]] (--cram CRAM_OUT | --out R1_OUT) [--out2 R2_OUT] --stats STATS
                             [--logs LOGS_DIRECTORY]

options:
  -h, --help            show this help message and exit
  -t, --threads THREADS
  -n                    Dry run
  --qtrim, --no-qtrim   Trim right end of reads to remove bases with quality below trimq.
  --trimq TRIMQ         Regions with average quality BELOW this will be trimmed, if qtrim is enabled
  --dataset_id DATASET_ID
                        Only for CRAM output. Will be added to the @RG header line.
  --hic_kit HIC_KIT     Only for CRAM output. Will be added to the @RG header line.

Input:
  --in R1               Read 1 input
  --in2 R2              Read 2 input
  -a, --adaptors ADAPTORS [ADAPTORS ...]
                        FASTA file(s) of adaptors. Multiple adaptor files can be used. Default ['/usr/share/java/bbmap/resources/adapters.fa'].

Output:
  --cram CRAM_OUT       CRAM output. For IO efficiency, you can output CRAM or fastq, but not both. If you need both, convert the output
                        afterwards.
  --out R1_OUT          Read 1 output. For IO efficiency, you can output CRAM or fastq, but not both. If you need both, convert the output
                        afterwards.
  --out2 R2_OUT         Read 2 output
  --stats STATS         Stats output (json)
  --logs LOGS_DIRECTORY
                        Log output directory. Default: logs are discarded.
```

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib import resources
from importlib.metadata import metadata, files
from pathlib import Path
from snakemake.logging import logger
import argparse
from snakemake.api import (
    SnakemakeApi,
    ResourceSettings,
    ConfigSettings,
    ExecutionSettings,
)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--threads", type=int, default=8, dest="threads")

    parser.add_argument("-n", help="Dry run", dest="dry_run", action="store_true")

    input_group = parser.add_argument_group("Input")

    input_group.add_argument(
        "--in", required=True, type=Path, help="Read 1 input", dest="r1"
    )

    input_group.add_argument(
        "--in2", required=True, type=Path, help="Read 2 input", dest="r2"
    )

    input_group.add_argument(
        "-a",
        "--adaptors",
        type=Path,
        help="FASTA file(s) of adaptors. Multiple adaptor files can be used.",
        dest="adaptors",
    )

    output_group = parser.add_argument_group("Output")

    output_group.add_argument(
        "--out", required=True, type=Path, help="Read 1 output", dest="r1_out"
    )

    output_group.add_argument(
        "--out2", required=True, type=Path, help="Read 2 output", dest="r2_out"
    )

    output_group.add_argument(
        "--stats", required=True, type=Path, help="Stats output (json)", dest="stats"
    )

    return parser.parse_args()


def main():
    # print version info
    pkg_metadata = metadata(__package__)

    pkg_name = pkg_metadata.get("Name")
    pkg_version = pkg_metadata.get("Version")

    logger.warning(f"{pkg_name} version {pkg_version}")

    # get the snakefile
    snakefile = Path(resources.files(__package__), "Snakefile")
    if snakefile.is_file():
        logger.warning(f"Using snakefile {snakefile}")
    else:
        raise FileNotFoundError("Could not find a Snakefile")

    # get arguments
    args = parse_arguments()
    logger.warning(f"Entrypoint args:\n    {args}")

    # run the pipeline
    resource_settings = ResourceSettings(cores=args.threads)
    config_settings = ConfigSettings(config=args.__dict__)
    execution_settings = ExecutionSettings(args.__dict__)

    with SnakemakeApi() as snakemake_api:
        workflow_api = snakemake_api.workflow(
            snakefile=snakefile,
            resource_settings=resource_settings,
            config_settings=config_settings,
        )
        dag = workflow_api.dag()
        dag.execute_workflow(
            executor="dryrun" if args.dry_run else "local",
            execution_settings=execution_settings,
        )

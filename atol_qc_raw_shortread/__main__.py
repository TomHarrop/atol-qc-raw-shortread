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
    OutputSettings,
)
from snakemake.settings.enums import Quietness


def parse_arguments():
    parser = argparse.ArgumentParser()

    # options
    parser.add_argument("-t", "--threads", type=int, default=16, dest="threads")
    parser.add_argument("-n", help="Dry run", dest="dry_run", action="store_true")

    parser.add_argument(
        "--qtrim",
        help="Trim right end of reads to remove bases with quality below trimq.",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--trimq",
        type=float,
        dest="trimq",
        help="Regions with average quality BELOW this will be trimmed, if qtrim is enabled",
        default=6.0,
    )

    # inputs
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
        nargs="+",
    )

    # outputs
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
    output_group.add_argument(
        "--logs",
        required=False,
        type=Path,
        help="Log output directory. Default: logs are discarded.",
        dest="logs_directory",
    )

    return parser.parse_args()


def main():
    # print version info
    pkg_metadata = metadata(__package__)

    pkg_name = pkg_metadata.get("Name")
    pkg_version = pkg_metadata.get("Version")

    logger.warning(f"{pkg_name} version {pkg_version}")

    # get the snakefile
    snakefile = Path(resources.files(__package__), "workflow", "Snakefile")
    if snakefile.is_file():
        logger.warning(f"Using snakefile {snakefile}")
    else:
        raise FileNotFoundError("Could not find a Snakefile")

    stats_template = Path(
        resources.files(__package__), "workflow", "report", "stats.json"
    )
    if stats_template.is_file():
        logger.warning(f"Using stats_template {stats_template}")
    else:
        raise FileNotFoundError("Could not find a stats_template")

    # get arguments
    args = parse_arguments()
    logger.warning(f"Entrypoint args:\n    {args}")
    args.stats_template = stats_template

    # control output
    output_settings = OutputSettings(quiet={Quietness.RULES, Quietness.HOST})

    # other settings
    resource_settings = ResourceSettings(
        cores=args.threads,
        overwrite_resource_scopes={
            "mem": "global",
            "threads": "global",
        },
    )
    config_settings = ConfigSettings(config=args.__dict__)
    execution_settings = ExecutionSettings(args.__dict__, lock=False)

    with SnakemakeApi(output_settings) as snakemake_api:
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

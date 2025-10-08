import pandas as pd

# Configure log parsing. These fields will be grepped out of the bbduk logs and
# show up in the final CSVs.
log_fields = [
    "Containments:",
    "Duplicates Found:",
    "Duplicates:",
    "Entropy-masked:",
    "FTrimmed:",
    "Input:",
    "KTrimmed:",
    "Pairs:",
    "Reads In:",
    "Result:",
    "Singletons:",
]

if qtrim:
    log_fields.append("QTrimmed:")

log_regex = "\|".join(log_fields)


def get_stats_params(wildcards, input):
    trim_stats = pd.read_csv(input.trim_stats)
    base_count = trim_stats.loc[trim_stats["type"] == "Result", "bases"].iloc[0]
    read_count = trim_stats.loc[trim_stats["type"] == "Result", "reads"].iloc[0]

    repair_stats = pd.read_csv(input.repair_stats)
    input_bases = int(
        repair_stats.loc[repair_stats["type"] == "Input", "bases"].iloc[0]
    )

    qc_bases_removed = input_bases - base_count

    with open(input.gchist, "r") as f:
        line = ""
        while not line.startswith("#Mean"):
            logger.error(line)
            line = f.readline()

        mean_gc_content = line.split("\t")[1]

    return {
        "base_count": int(base_count),
        "read_count": int(read_count),
        "mean_gc_content": float(mean_gc_content),
        "qc_bases_removed": int(qc_bases_removed),
    }


rule output_stats:
    input:
        trim_stats=Path(logs_directory, "trim.csv"),
        repair_stats=Path(logs_directory, "repair.csv"),
        gchist=Path(logs_directory, "gchist.txt"),
        template=stats_template,
    output:
        stats,
    params:
        stats=get_stats_params,
    template_engine:
        "jinja2"


rule process_step_logs:
    input:
        Path(workingdir, "from_logs", "{step}.txt"),
    output:
        Path(logs_directory, "{step}.csv"),
    shell:
        "process_step_logs < {input} > {output} "


rule grep_logs:
    input:
        Path(logs_directory, "{step}.log"),
    output:
        temp(Path(workingdir, "from_logs", "{step}.txt")),
    shell:
        # awk -F '[[:space:]]{2,}' means separated by two or more spaces
        "grep '^\({log_regex}\)' {input} "
        "| "
        "awk -F '[[:space:]]{{2,}}' "
        "'{{print $1, $2, $3}}' "
        "OFS='\t' "
        "> {output} "

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


rule combine_step_logs:
    input:
        Path(workingdir, "from_logs", "{step}.csv"),
    output:
        Path(stats_directory, "{step}.csv"),
    shell:
        "echo 'type,reads,bases' > {output} ; "
        "cat {input} >> {output}"


rule process_step_logs:
    input:
        Path(workingdir, "from_logs", "{step}.txt"),
    output:
        temp(Path(workingdir, "from_logs", "{step}.csv")),
    shell:
        "process_step_logs < {input} > {output} "


rule grep_logs:
    input:
        Path(stats_directory, "{step}.log"),
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

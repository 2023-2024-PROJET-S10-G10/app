import rich_click as click

click.rich_click.OPTION_GROUPS = {
    "gridsub.py": [
        {
            "name": "Basic options",
            "options": ["--campaign", "--details"],
        },
        {"name": "JDL options", "options": ["--file", "--jobfile"]},
        {"name": "JSON options", "options": ["--json", "--jsonjob"]},
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


class ID(int):
    name = "ID"


class JDL_FILE(str):
    name = "JDL_FILE"


class JSON(str):
    name = "JSON"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c",
    "--campaign",
    type=ID,
    default=None,
    help="Add jobs in an existing campaign",
)
@click.option(
    "-d",
    "--details",
    default=False,
    is_flag=True,
    help="Prints all the JSON of the campaign instead of just the ID",
)
@click.option(
    "-f",
    "--file",
    type=JDL_FILE,
    default=None,
    help="JDL File containing the JSON",
)
@click.option(
    "-F",
    "--jobfile",
    type=JDL_FILE,
    default=None,
    help="JDL File containing an array of parameters",
)
@click.option("-j", "--json", type=JSON, default=None, help="JSON String")
@click.option(
    "-J",
    "--jsonjob",
    type=JSON,
    default=None,
    help="JSON String containing an array of parameters",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(campaign, details, file, jobfile, json, jsonjob):
    """
    This command allow the user to submit campaigns to CiGri.
    """

    # Checking option content

    if file is None and jobfile is None and json is None and jsonjob is None:
        raise click.MissingParameter(
            "Must provide one of the four --file, --jobfile, --json, --jsonjob option",
            param_type="option",
        )

    # Function implementation

    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

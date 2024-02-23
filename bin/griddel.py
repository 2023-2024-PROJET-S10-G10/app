import rich_click as click

click.rich_click.OPTION_GROUPS = {
    "griddel.py": [
        {
            "name": "Basic options",
            "options": ["--campaign_ids", "--job"],
        },
        {
            "name": "State management options",
            "options": ["--pause", "--resume", "--purge"]
        },
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


class IntListParamType(click.ParamType):
    name = "id1,id2,idN"

    def convert(self, value, param, ctx):
        try:
            ids = [int(x.strip()) for x in value.split(',')]
            return ids
        except ValueError:
            self.fail(f"{value} is not a valid list of integers", param, ctx)


class ID(int):
    name = "ID"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c", "--campaign_ids",
    type=IntListParamType(),
    default=None,
    help="Campaigns on which to act"
)
@click.option(
    "-p", "--pause",
    default=False,
    is_flag=True,
    help="Holds the campaign"
)
@click.option(
    "-r", "--resume",
    default=False,
    is_flag=True,
    help="Resumes the campaign (only if it is paused)"
)
@click.option(
    "--purge",
    default=False,
    is_flag=True,
    help="Purge the campaign (only if it is finished)"
)
@click.option(
    "-j", "--job",
    type=ID,
    default=None,
    help="Cancel a single job"
)
@click.option(
    "-v", "--verbose",
    default=False,
    show_default=True,
    is_flag=True,
    help="Enable verbose mode"
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(campaign_ids, pause, resume, purge, job, verbose):
    """
    This command allow the user to manage the already existing campaigns.
    """
    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

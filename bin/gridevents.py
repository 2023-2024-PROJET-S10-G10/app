import rich_click as click

click.rich_click.OPTION_GROUPS = {
    "gridevents.py": [
        {
            "name": "Basic options",
            "options": ["--campaign", "--all", "--global", "--event"],
        },
        {
            "name": "Fix option",
            "options": ["--fix", "--resubmit"]
        },
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


class ID(int):
    name = "ID"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c", "--campaign",
    type=ID,
    default=None,
    help="Show events for this campaign ID or close them (with -f)"
)
@click.option(
    "-g", "--global", "glob",
    default=False,
    is_flag=True,
    help="Show current global events (not specific to a campaign)"
)
@click.option(
    "-e", "--event",
    type=ID,
    default=None,
    help="Show only this event or close it (with -f)"
)
@click.option(
    "-f", "--fix",
    default=False,
    is_flag=True,
    help="Fix: close an event (used with -e) or all the events of a campaign (used with -c)"
)
@click.option(
    "-r", "--resubmit",
    default=False,
    is_flag=True,
    help="Resubmit each job concerned by the fixed events (needs -f)"
)
@click.option(
    "-a", "--all",
    default=False,
    is_flag=True,
    help="Show all events, even those that are closed (warning: it does not print the current global events)"
)
@click.option(
    "-v", "--verbose",
    default=False,
    show_default=True,
    is_flag=True,
    help="Enable verbose mode"
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(verbose, campaign, glob, event, fix, resubmit, all):
    """
    This command allow the user to manage the events.
    """

    # Checking option content

    if resubmit and not fix:
        raise click.BadOptionUsage("--resubmit", "Must provide --fix to resubmit a job")

    if event is not None and campaign is not None:
        raise click.BadOptionUsage(["--campaign", "--event"], "Can't provide both campaign id and event id")

    if event is None or campaign is None:
        raise click.MissingParameter("Must provide an event id or a campaign ID", param_type="option")

    if event is not None and all:
        raise click.BadOptionUsage("--all", "Can't provide --all parameter for an event")

    if campaign:
        fix = True

    if event:
        fix = True

    # Function implementation

    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

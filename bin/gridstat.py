import rich_click as click


class ID(int):
    name = "ID"


class Offset(int):
    name = "OFFSET"


class Username(str):
    name = "USERNAME"


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    "-c", "--campaign",
    type=ID,
    default=None,
    help="Only print informations for campaign ID"
)
@click.option(
    "-d", "--dump",
    default=False,
    is_flag=True,
    help="Dump the result as JSON"
)
@click.option(
    "-f", "--full",
    default=False,
    is_flag=True,
    help="Display all info of a campaign (used with -c)"
)
@click.option(
    "-o", "--offset",
    type=Offset,
    default=None,
    help="Print jobs starting at this offset (used with -f)"
)
@click.option(
    "-e", "--events",
    default=False,
    is_flag=True,
    help="Print open events on a campaign"
)
@click.option(
    "-j", "--job",
    type=ID,
    default=None,
    help="Print infos about a job"
)
@click.option(
    "-C", "--cinfos",
    default=False,
    is_flag=True,
    help="Print cluster's scheduler infos about a job (used with -j)"
)
@click.option(
    "-H", "--headerless",
    default=False,
    is_flag=True,
    help="Remove the columns title"
)
@click.option(
    "-p", "--pretty",
    default=False,
    is_flag=True,
    help="Pretty print with a dump"
)
@click.option(
    "-u", "--username",
    type=Username,
    default=None,
    help="Only print campaigns from USERNAME"
)
@click.option(
    "-O", "--stdout",
    default=False,
    is_flag=True,
    help="Get the stdout file of a job"
)
@click.option(
    "-J", "--jdl",
    default=False,
    is_flag=True,
    help="Get the JDL file (json) of the campaign"
)
@click.option(
    "-E", "--stderr",
    default=False,
    is_flag=True,
    help="Get the stderr file of a job"
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(campaign, dump, full, offset, events, job, cinfos, headerless, pretty, username, stdout, jdl, stderr):
    """
    This command allow the user to gather information about the current campaigns.
    """
    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

import rich_click as click


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-i", "--infos",
    default=False,
    is_flag=True,
    help="Show infos about each cluster"
)
@click.option(
    "-I", "--more_infos",
    default=False,
    is_flag=True,
    help="Show detailed infos about each cluster"
)
@click.option(
    "-u", "--usage",
    default=False,
    is_flag=True,
    help="Show usage infos about each cluster (implies -i)"
)
@click.option(
    "-b", "--bars",
    default=False,
    is_flag=True,
    help="Show usage infos with colored bars (implies -i -u)"
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(infos, more_infos, usage, bars):
    """
    This command allow the user to gatheir information on the different clusters.
    """
    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

import rich_click as click
import re

click.rich_click.OPTION_GROUPS = {
    "gridnotify.py": [
        {
            "name": "Basic options",
            "options": ["--list", "--mail", "--severity", "--unsubscribe"],
        },
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


class EmailParamType(click.ParamType):
    name = "address"

    def convert(self, value, param, ctx):
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value
        ):
            self.fail(f"'{value}' is not a valid email address.", param, ctx)
        return value


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-l", "--list", default=False, is_flag=True, help="List notifications"
)
@click.option(
    "-m",
    "--mail",
    type=EmailParamType(),
    default=None,
    help="Subscribe to e-mail notifications with the given e-mail address",
)
@click.option(
    "-u",
    "--unsubscribe",
    default=False,
    is_flag=True,
    help="Unsubscribe from the specified notifications",
)
@click.option(
    "-s",
    "--severity",
    type=click.Choice(["low", "medium", "high"]),
    default=None,
    help="Set the severity of notifications to low, medium or high",
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    show_default=True,
    is_flag=True,
    help="Enable verbose mode",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(list, mail, unsubscribe, severity, verbose):
    """
    This command allow the user to manage the notification.
    """

    # Checking option content

    if list and mail is not None or unsubscribe or severity is not None:
        raise click.BadOptionUsage("--list", "--list must be provide alone")

    if severity is not None and mail is None:
        raise click.BadOptionUsage(
            "--severity",
            "An email must be provided using (--mail) when using --severity",
        )

    if unsubscribe and mail is None:
        raise click.BadOptionUsage(
            "--unsubscribe",
            "An email must be provided using (--mail) when using --unsubscribe",
        )

    if unsubscribe and severity is not None:
        raise click.BadOptionUsage(
            "[--unsubscribe, --severity]",
            "Can't use both --severity and --unsubscribe",
        )

    # Function implementation

    raise RuntimeError("NYI")


if __name__ == "__main__":
    cli()

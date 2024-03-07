import rich_click as click
import json

import sys
sys.path.append('../')
from API.apiclient import ApiClient

click.rich_click.OPTION_GROUPS = {
    "griddel.py": [
        {
            "name": "Basic options",
            "options": ["--campaign_ids", "--job"],
        },
        {
            "name": "State management options",
            "options": ["--pause", "--resume", "--purge"],
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
            ids = [int(x.strip()) for x in value.split(",")]
            return ids
        except ValueError:
            self.fail(f"{value} is not a valid list of integers", param, ctx)


class ID(int):
    name = "ID"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c",
    "--campaign_ids",
    type=IntListParamType(),
    default=None,
    help="Campaigns on which to act",
)
@click.option(
    "-p", "--pause", default=False, is_flag=True, help="Holds the campaign"
)
@click.option(
    "-r",
    "--resume",
    default=False,
    is_flag=True,
    help="Resumes the campaign (only if it is paused)",
)
@click.option(
    "--purge",
    default=False,
    is_flag=True,
    help="Purge the campaign (only if it is finished)",
)
@click.option("-j", "--job", type=ID, default=None, help="Cancel a single job")
@click.option(
    "-v",
    "--verbose",
    default=False,
    show_default=True,
    is_flag=True,
    help="Enable verbose mode",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(campaign_ids, pause, resume, purge, job, verbose):
    """
    This command allow the user to manage the already existing campaigns.

    It can either edit the campaign state eitheir cancel a campaign job.
    """

    client = ApiClient(host="localhost", port=4430, baseEndpoint='/cigri-api',
                       headers={"Content-Type": "application/json",
                                "Accept": "application/json"})

    griddel(campaign_ids, pause, resume, purge, job, verbose, client)


def griddel(campaign_ids, pause, resume, purge, job, verbose, client):
    # Checking option content

    if pause and resume:
        raise click.BadOptionUsage(
            ["--pause", "--resume"], "Can't pause and resume at the same time"
        )

    if pause and purge:
        raise click.BadOptionUsage(
            ["--pause", "--purge"], "Can't pause and purge at the same time"
        )

    if resume and purge:
        raise click.BadOptionUsage(
            ["--resume", "--purge"], "Can't resume and purge at the same time"
        )

    if not campaign_ids and job is None:
        raise click.MissingParameter(
            "Must provide at least a campaign id or a job id (using --campaign_ids ID1,ID2,IDN or --job ID)",
            param_type="option",
        )

    if campaign_ids and job is not None:
        raise click.BadOptionUsage(
            ["--campaign_ids", "--job"],
            "Can't provide both campaign ids and job id",
        )

    if job is not None and (pause or resume or purge):
        raise click.BadOptionUsage(
            "--job", "Can't provide a job to cancel and a campaign state"
        )

    if campaign_ids and not (pause or resume or purge):
        raise click.BadOptionUsage(
            "--campaign_ids",
            "Must provide a state for the campaigns (--pause, --resume or --purge)",
        )

    # Function implementation

    if job is not None:
        response = client.delete(f"/jobs/{job}")
        content = json.loads(response.read())

        if response.status != 202:
            print(f"Failed to cancel job {job}: {content}.")
        else:
            if verbose:
                print(response.read())

    elif campaign_ids:
        status = ""
        if pause:
            status = "?hold=1"
        if resume:
            status = "?resume=1"
        if purge:
            status = "?purge=1"

        for campaign_id in campaign_ids:
            response = client.delete(f"/campaigns/{campaign_id}{status}")
            content = json.loads(response.read())

            if response.status != 202:
                print(f"Failed to cancel campaign {campaign_id}: {content}.")
            else:
                if verbose:
                    print(content)
    else:
        raise RuntimeError("griddel shouldn't get called without a job id or a campaign id")


if __name__ == "__main__":
    cli()

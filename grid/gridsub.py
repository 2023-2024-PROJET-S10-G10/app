import rich_click as click
import json

import sys

sys.path.append("../")
from API.apiclient import ApiClient

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
@click.option(
    "-j", "--json", "jsonCLI", type=JSON, default=None, help="JSON String"
)
@click.option(
    "-J",
    "--jsonjob",
    type=JSON,
    default=None,
    help="JSON String containing an array of parameters",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(campaign, details, file, jobfile, jsonCLI, jsonjob):
    """
    This command allow the user to submit campaigns to CiGri.
    """

    client = ApiClient(
        host="localhost",
        port=4430,
        baseEndpoint="/cigri-api",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    gridsub(campaign, details, file, jobfile, jsonCLI, jsonjob, client)


def submit_campaign(jdl, client, campaign_id=None):
    url = "/campaigns"

    if campaign_id is not None:
        url += f"/{campaign_id}/jobs"

    return client.post(url, body=jdl)


def gridsub(campaign, details, file, jobfile, jsonCLI, jsonjob, client):
    # Checking option content

    if (
        file is None
        and jobfile is None
        and jsonCLI is None
        and jsonjob is None
    ):
        raise click.MissingParameter(
            "Must provide one of the four --file, --jobfile, --json, --jsonjob option",
            param_type="option",
        )

    if (jobfile is not None or jsonjob is not None) and campaign is None:
        raise click.MissingParameter(
            "Must provide a campaign id using --campaign when using --jobfile or --jsonjob",
            param_type="option",
        )

    # Function implementation

    jsons = []
    jobs = []

    if file is not None:
        with open(file) as f:
            jsons.append(f.read())

    if jobfile is not None:
        with open(jobfile) as f:
            jobs.append(f.read())

    if jsonCLI is not None:
        jsons.append(jsonCLI)

    if jsonjob is not None:
        jobs.append(jsonjob)

    for json_ in jsons:
        response = submit_campaign(json_, client)
        body = response.read()
        if response.status == 201:
            print("Campaign successfully submitted")
            if details:
                print(json.dumps(json.loads(body.decode()), indent=2))
        else:
            try:
                error = json.loads(body)
                if error["title"] == "Admission rule error":
                    print(f"Admission rule error:\n\t{error['message']}")
                else:
                    raise RuntimeError(f"Error: {response.body}")
            except json.decoder.JSONDecodeErrors:
                raise RuntimeError(f"Error: {body}")

    for job in jobs:
        response = submit_campaign(job, client, campaign_id=campaign)
        body = response.read()

        if response.status == 201:
            print(f"Jobs successfully added to campaign {campaign}")
            if details:
                print(json.dumps(json.loads(body.decode()), indent=2))
        else:
            raise RuntimeError(
                f"Error adding jobs to the campaign ({campaign}): {body}"
            )


if __name__ == "__main__":
    cli()

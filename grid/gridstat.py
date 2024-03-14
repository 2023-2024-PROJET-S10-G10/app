import rich_click as click
import json
import time

import sys

sys.path.append("../")
from API.apiclient import ApiClient
from shared import print_events, print_job

STATES = {
    "cancelled": "C",
    "in_treatment": "R",
    "terminated": "T",
    "paused": "P",
}
STATES.default = "?"

click.rich_click.OPTION_GROUPS = {
    "gridstat.py": [
        {
            "name": "Targeting options",
            "options": ["--campaign", "--job", "--username", "--offset"],
        },
        {"name": "Output options", "options": ["--full", "--events"]},
        {
            "name": "Advanced output options",
            "options": ["--dump", "--pretty", "--headerless", "--cinfos"],
        },
        {"name": "File options", "options": ["--stdout", "--stderr", "--jdl"]},
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


class ID(int):
    name = "ID"


class Offset(int):
    name = "OFFSET"


class Username(str):
    name = "USERNAME"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-c",
    "--campaign",
    type=ID,
    default=None,
    help="Only print informations for campaign ID",
)
@click.option(
    "-d", "--dump", default=False, is_flag=True, help="Dump the result as JSON"
)
@click.option(
    "-f",
    "--full",
    default=False,
    is_flag=True,
    help="Display all info of a campaign (used with -c)",
)
@click.option(
    "-o",
    "--offset",
    type=Offset,
    default=None,
    help="Print jobs starting at this offset (used with -f)",
)
@click.option(
    "-e",
    "--events",
    default=False,
    is_flag=True,
    help="Print open events on a campaign",
)
@click.option(
    "-j", "--job", type=ID, default=None, help="Print infos about a job"
)
@click.option(
    "-C",
    "--cinfos",
    default=False,
    is_flag=True,
    help="Print cluster's scheduler infos about a job (used with -j)",
)
@click.option(
    "-H",
    "--headerless",
    default=False,
    is_flag=True,
    help="Remove the columns title",
)
@click.option(
    "-p",
    "--pretty",
    default=False,
    is_flag=True,
    help="Pretty print with a dump",
)
@click.option(
    "-u",
    "--username",
    type=Username,
    default=None,
    help="Only print campaigns from USERNAME",
)
@click.option(
    "-O",
    "--stdout",
    default=False,
    is_flag=True,
    help="Get the stdout file of a job",
)
@click.option(
    "-J",
    "--jdl",
    default=False,
    is_flag=True,
    help="Get the JDL file (json) of the campaign",
)
@click.option(
    "-E",
    "--stderr",
    default=False,
    is_flag=True,
    help="Get the stderr file of a job",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(
    campaign,
    dump,
    full,
    offset,
    events,
    job,
    cinfos,
    headerless,
    pretty,
    username,
    stdout,
    jdl,
    stderr,
):
    """
    This command allow the user to gather information about the current campaigns.
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

    gridstat(
        campaign,
        dump,
        full,
        offset,
        events,
        job,
        cinfos,
        headerless,
        pretty,
        username,
        stdout,
        jdl,
        stderr,
        client,
    )


def gridstat(
    campaign,
    dump,
    full,
    offset,
    events,
    job,
    cinfos,
    headerless,
    pretty,
    username,
    stdout,
    jdl,
    stderr,
    client,
):
    # Checking option content

    if offset is not None:
        full = True

    if cinfos and campaign is not None:
        raise click.MissingParameter(
            "Must provide a campaign ID using --campaign to use --cinfos",
            param_type="campaign ID",
        )

    if full and campaign is not None:
        raise click.MissingParameter(
            "Must provide a campaign ID using --campaign to use --full",
            param_type="campaign ID",
        )

    if events and campaign is None:
        raise click.MissingParameter(
            "Must provide a campaign ID using --campaign to use --events",
            param_type="campaign ID",
        )

    if jdl and campaign is None:
        raise click.MissingParameter(
            "Must provide a campaign ID using --campaign to use --jdl",
            param_type="campaign ID",
        )

    if stdout and events is None:
        raise click.MissingParameter(
            "Must provide an event ID using --events to use --stdout",
            param_type="event ID",
        )

    if stderr and events is None:
        raise click.MissingParameter(
            "Must provide an event ID using --events to use --stderr",
            param_type="event ID",
        )

    # Function implementation

    campaigns = []

    url = "/campaigns"
    if campaign is not None:
        url += f"/{campaign}"
    if jdl:
        url += "/jdl?pretty=true"
    if events:
        url += "/events"
    if full and dump:
        url += "/jobs"
    if dump and pretty:
        url += "?pretty=true"
    if offset is not None and dump and pretty:
        url += f"&offset={offset}"
    if offset is not None and dump and not pretty:
        url += f"?offset={offset}"

    if job is not None:
        url = f"/jobs/{job}"
    if stdout is not None:
        url += f"/{stdout}"
    if cinfos:
        url += "/cinfos?pretty=true"

    response = client.get(url)
    body = response.read()
    content = json.load(body)
    content_print = json.dumps(content, indent=2)

    if dump:
        print(body)
    elif events:
        events = content["items"]
        print_events(events)
    elif job is not None:
        if stdout:
            if response.status == 404:
                print("File not found :\n", content["message"])
            else:
                print(content["inspect"])
        elif cinfos:
            print(content_print)
        else:
            print_job(content)
    elif jdl:
        print(content_print)
    else:
        if campaign:
            campaigns = [content]
            if response.status == 404:
                print(f"Campaign {campaign} not found")
                exit
        else:
            campaigns = content["items"]

    if username:
        campaigns = [
            campaign for campaign in campaigns if campaign["user"] == username
        ]

    if not headerless and not full and not dump and campaign is None:
        print(
            "Campaign id Name                User             Submission time     S  Progress"
        )
        print(
            "----------- ------------------- ---------------- ------------------- -- --------"
        )

    campaigns = sorted(campaigns, key=lambda x: int(x["id"]))

    for campaign in campaigns:
        progress = 0
        if campaign["total_jobs"] != 0:
            progress = (
                campaign["finished_jobs"] * 100.0 / campaign["total_jobs"]
            )

        e = " "
        if campaign["has_events"]:
            e = "e"

        if campaign is not None:
            print(
                "%-11d %-19s %-16s %-19s %s %d/%d (%d%%)"
                % (
                    campaign["id"],
                    campaign["name"][:19],
                    campaign["user"][:16],
                    time.strftime(
                        "%Y-%m-%d %H-%M-%S",
                        time.localtime(campaign["submission_time"]),
                    ),
                    STATES[campaign["state"]] + e,
                    campaign["finished_jobs"],
                    campaign["total_jobs"],
                    progress,
                )
            )
        else:
            if e == "e":
                e = "(events)"
            clusters_string = ""
            for c in campaign["clusters"]:
                clusters_string += (
                    f"\t{campaign['clusters'][c]['cluster_name']}"
                )
                for k in campaign["clusters"][c]:
                    if k != "cluster_name":
                        clusters_string += (
                            f"\t{k}: {campaign['clusters'][c][k]}\n"
                        )

            response = client.get(f"/campaigns/{campaign['id']}/stats")
            stats_string = ""

            stats = content
            for k in stats:
                if k == "remaining_time":
                    remaining = round(stats[k] / 3600, 1)
                    if remaining > 10000:
                        remaining = "~"
                    stats_string += f"\t{k}: {remaining} hours"
                elif k == "jobs_throughput":
                    throughput = round(stats[k] / 3600, 1)
                    if throughput < 0.01:
                        throughput = "~"
                    stats_string += f"\t{k}: {throughput} jobs/h\n"
                elif k == "failure_rate" or k == "resubmit_rate":
                    stats_string += f"\t{k}: {(stats[k] * 100):.1f} %\n"
                else:
                    stats_string += f"\t{k}: {stats[k]}\n"

            print(
                "Campaign: {}\n  Name: {}\n  User: {}\n  Date: {}\n  State: {} {}\n  Progress: {}/{:.0f} ({:.0f}%)\n  Stats: \n{}  Clusters: \n{}".format(
                    campaign["id"],
                    campaign["name"],
                    campaign["user"],
                    time.strftime(
                        "%Y-%m-%d %H-%M-%S",
                        time.localtime(campaign["submission_time"]),
                    ),
                    campaign["state"],
                    e,
                    campaign["finished_jobs"],
                    campaign["total_jobs"],
                    progress,
                    stats_string,
                    clusters_string,
                )
            )

            if full:
                print(" Jobs:")
                items = []
                if offset:
                    offset_string = f"?offset={offset}"
                response = client.get(
                    f"/campaigns/{campaign['id']}/jobs{offset_string}"
                )
                jobs = content
                items = jobs["items"]
                c = 0
                maxIte = 10

                while (
                    jobs
                    and jobs["links"]
                    and any(link["rel"] == "next" for link in jobs["links"])
                    and c < maxIte
                ):
                    c += 1
                    url = next(
                        (
                            link["href"]
                            for link in jobs["links"]
                            if link["rel"] == "next"
                        ),
                        None,
                    )
                    if url:
                        response = client.get(url)
                        jobs = json.loads(response.text)
                        if "items" in jobs:
                            items += jobs["items"]
                    else:
                        break

                if not items:
                    print("No jobs to print")
                else:
                    for job in items:
                        print(
                            "  {}: {},{},{},{},{},{}".format(
                                job["id"],
                                job.get("cigri_job_id", "*"),
                                job.get("remote_id", "*"),
                                job["state"],
                                job.get("cluster", "*"),
                                job["name"],
                                job["parameters"],
                            )
                        )
            if (
                jobs
                and jobs["links"]
                and any(link["rel"] == "next" for link in jobs["links"])
                and "offset" in jobs
            ):
                print(
                    f"WARNING: more jobs left. Next jobs with --offset={int(jobs['offset']) + int(jobs['limit'])}"
                )


if __name__ == "__main__":
    cli()

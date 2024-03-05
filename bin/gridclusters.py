import rich_click as click
import json

import sys

sys.path.append('../')
from API.apiclient import ApiClient

click.rich_click.OPTION_GROUPS = {
    "gridclusters.py": [
        {
            "name": "Basic option",
            "options": ["--infos", "--more_infos"],
        },
        {
            "name": "Visualization customization option",
            "options": ["--usage", "--bars"],
        },
        {
            "name": "Advanced options",
            "options": ["--verbose", "--version", "--help"],
        },
    ]
}


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-i",
    "--infos",
    default=False,
    is_flag=True,
    help="Show infos about each cluster",
)
@click.option(
    "-I",
    "--more_infos",
    default=False,
    is_flag=True,
    help="Show detailed infos about each cluster",
)
@click.option(
    "-u",
    "--usage",
    default=False,
    is_flag=True,
    help="Show usage infos about each cluster (implies -i)",
)
@click.option(
    "-b",
    "--bars",
    default=False,
    is_flag=True,
    help="Show usage infos with colored bars (implies -i -u)",
)
@click.version_option("4.0.0", prog_name="CiGri")
def cli(infos, more_infos, usage, bars, client=None):
    """
    This command allow the user to gatheir information on the different clusters.
    """

    # Checking option content

    if more_infos:
        infos = True

    if usage:
        infos = True

    if bars:
        infos = True
        usage = True

    # Function implementation

    # if client is None:
    #     client = ApiClient(host="localhost", port=4430, baseEndpoint='/cigri-api',
    #                        headers={"Content-Type": "application/json",
    #                                 "Accept": "application/json"})

    # _, content = client.get("/clusters")
    content = """{"items":[{"id":"7","name":"ceciccluster","links":[{"rel":"self","href":"/clusters/7"},{"rel":"parent","href":"/clusters"}]},{"id":"2","name":"froggy","links":[{"rel":"self","href":"/clusters/2"},{"rel":"parent","href":"/clusters"}]},{"id":"5","name":"luke","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}]},{"id":"9","name":"bigfoot","links":[{"rel":"self","href":"/clusters/9"},{"rel":"parent","href":"/clusters"}]},{"id":"8","name":"dahu","links":[{"rel":"self","href":"/clusters/8"},{"rel":"parent","href":"/clusters"}]}],"total":5,"links":[{"rel":"self","href":"/clusters"},{"rel":"parent","href":"/"}]}"""
    clusters = json.loads(content)['items']

    cluster_usages = ""
    if usage:
        # _, content = client.get("/gridusage")
        content = """{"items":[{"date":1709641539,"clusters":[{"cluster_name":"dahu","cluster_id":8,"max_resources":6080,"used_resources":0,"used_by_cigri":0,"unavailable_resources":2320},{"cluster_name":"luke","cluster_id":5,"max_resources":1166,"used_resources":0,"used_by_cigri":0,"unavailable_resources":1166},{"cluster_name":"bigfoot","cluster_id":9,"max_resources":694,"used_resources":0,"used_by_cigri":0,"unavailable_resources":646}]}],"from":null,"to":null,"total":1}"""
        cluster_usages = json.loads(content)['items'][0]['clusters']

    prompt = ""
    clusters_sorted = sorted(clusters, key=lambda x: int(x['id']))

    for cluster in clusters_sorted:
        prompt += str(cluster['id']) + ": " + cluster["name"]

        if infos:
            # _, content = client.get("clusters/" + cluster['cluster_id'])
            content = """{"id":"5","name":"luke","api_url":"https://luke-api.univ-grenoble-alpes.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"luke.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"110","properties":"","stress_factor":"0.22/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}"""
            cluster_detail = json.loads(content)

            if more_infos:
                for key in cluster_detail:
                    if key != "links":
                        prompt += "\n\t" + key + ": " + str(cluster_detail[key])
            else:
                prompt += ", " + cluster_detail['ssh_host'] + " (stress:" + cluster_detail['stress_factor']
                if cluster_detail['blacklisted']:
                    prompt += ", BLACKLISTED"
                if cluster_detail['under_stress']:
                    prompt += ", UNDER_STRESS"
                prompt += ")"
            if usage:
                if int(cluster['id']) not in [cluster_usage['cluster_id'] for cluster_usage in cluster_usages]:
                    prompt += "\n\tData temporarily unavailable\n"
                else:
                    for cluster_usage in cluster_usages:
                        if not cluster_detail['blacklisted']:
                            if int(cluster['id']) == cluster_usage['cluster_id']:
                                if bars:
                                    size = 80
                                    unavailable = cluster_usage["unavailable_resources"]
                                    used = cluster_usage["used_resources"]
                                    cigri = cluster_usage["used_by_cigri"]
                                    used -= cigri
                                    max_value = cluster_usage["max_resources"]
                                    free = max_value - cigri - used - unavailable
                                    prompt += f" ({max_value} resources)\n"
                                    for _ in range(int(round(unavailable * size / max_value))):
                                        prompt += "\033[41m \033[0m"  # red

                                    for _ in range(int(round(used * size / max_value))):
                                        prompt += "\033[43m \033[0m"  # yellow

                                    for _ in range(int(round(cigri * size / max_value))):
                                        prompt += "\033[47m \033[0m"  # white

                                    for _ in range(int(round(free * size / max_value))):
                                        prompt += "\033[42m \033[0m"  # green
                                else:
                                    for key in cluster_usage:
                                        if key != "cluster_id" and key != "cluster_name":
                                            prompt += "\n\t" + key + ": " + str(cluster_usage[key]) + "\n"
                                prompt += "\n"
        prompt += "\n"
    if bars:
        prompt += "\n\033[41m \033[0m=unavailable \033[43m \033[0m=used \033[47m \033[0m=used_by_cigri \033[42m \033[0m=free\n"

    print(prompt)


if __name__ == "__main__":
    cli()

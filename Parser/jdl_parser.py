import sys
import json
import os

sys.path.append(sys.path[0].replace("/Parser", ""))

from utils.jdl import nameCluster
#from utils.jdl import jdlKeys
from SQL.queries import *

def get_json(json_file):
    with open(json_file, 'r') as f:
        json_block = json.load(f)
    return json_block
"""
def parse_params(param_string):
    params_list = []
    for param in param_string:
        params_list.append(param.split(" "))
    return params_list

def print_params_cluster(cluster):
    for key in jdlKeys:
        param(key, cluster)

def param(key, cluster):
    value = cluster.get(key)
    print(f"-->{key}:", value if value is not None else "None")
"""
def getProjectName(cluster):
    return cluster.get("project")


def print_params(json_block, id_campaign):
    """
    print("==> name:", json_block["name"])
    print("==> jobs type:", json_block["jobs_type"])
    print(f"==> clusters used number:{len(json_block['clusters'])} ({', '.join(json_block['clusters'].keys())})")
    """

    clusters = json_block["clusters"]

    for name_cluster in nameCluster:
        if name_cluster in clusters:
            id_cluster = selectCluster(name_cluster)
            cluster = clusters[name_cluster]
            """
            print_params_cluster(cluster)
            print(f"-> {name_cluster} ({id_cluster})")
            """
            addCampProp(id_campaign, id_cluster, getProjectName(cluster), json.dumps(cluster)) #json_block["clusters"][name_cluster]
        """
        else:
            print(f"-> {name_cluster}: None")
        """

def jdl_parser(json_file):

    json_block = get_json(json_file)
    #TODO: Replace environment variable by a better solution (security)
    user = os.environ.get("USER")
    addCampaign(user, json_block["name"], json_block["jobs_type"], len(json_block["params"]), json.dumps(json_block))
    
    id_campaign = selectCampaign(user, json_block["name"], json_block["jobs_type"], len(json_block["params"]), json.dumps(json_block))

    print_params(json_block, id_campaign)
    """
    print("==> jobs number:", len(json_block["params"]))

    print("==> parameters:", parse_params(json_block["params"]))
    """

    for param in json_block["params"]:
        #print("->", param)
        addParam (id_campaign, json_block["name"], param)
        id_params = selectParam(id_campaign, json_block["name"], param)
        addJob (id_campaign, id_params) 
    
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <json_jdl_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    jdl_parser(json_file)
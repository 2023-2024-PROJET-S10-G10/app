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

def getProjectName(cluster):
    return cluster.get("project")


def proc_params(json_block, id_campaign):
    clusters = json_block["clusters"]

    for name_cluster in nameCluster:
        if name_cluster in clusters:
            id_cluster = selectCluster(name_cluster)
            cluster = clusters[name_cluster]
            
            addCampProp(id_campaign, id_cluster, getProjectName(cluster), json.dumps(cluster)) #json_block["clusters"][name_cluster]

def jdl_parser(json_file):

    json_block = get_json(json_file)

    #TODO: Replace environment variable by a better solution (security)
    user = os.environ.get("USER")
    
    id_campaign = addCampaign(user, json_block["name"], json_block["jobs_type"], len(json_block["params"]), json.dumps(json_block))

    proc_params(json_block, id_campaign)

    for param in json_block["params"]:
        addParamWithoutName (id_campaign, param)   #, json_block["name"]
        id_params = selectParam(id_campaign, param)   #, json_block["name"]
        id_job = addJob (id_campaign, id_params) 
    
        id_event = addEvent (2, id_job, "CREATED", "Campaign created")

        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <json_jdl_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    jdl_parser(json_file)
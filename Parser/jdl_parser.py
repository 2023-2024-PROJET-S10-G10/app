import sys
import json
import os

sys.path.append(sys.path[0].replace("/Parser", ""))

from utils.jdl import nameCluster
#from utils.jdl import jdlKeys
from SQL.queries import *

def get_json(json_file):
    with open(json_file, 'r') as f:
        jdl = json.load(f)
    return jdl

def getProjectName(cluster):
    return cluster.get("project")

def getCampaignName(jdl):
    return jdl.get("name")

def getJobType(jdl):
    return jdl.get("jobs_type")

def getParams(jdl):
    return jdl.get("params")    #jdl["params"]

def getNbJobs(jdl):
    return len(getParams(jdl))

def getClusters(jdl):
    clusters = jdl.get("clusters")
    jdl_clusters = []
    for name_cluster in nameCluster:
        if name_cluster in clusters:
            jdl_clusters.append(name_cluster)
    return jdl_clusters

def setCampaignProperties(jdl, id_campaign):
    clusters = getClusters(jdl)
    detail_clusters = jdl.get("clusters")

    for name_cluster in clusters:
        # get the id of the cluster
        id_cluster = selectCluster(name_cluster)
        # stock cluster's elements in the 'cluster' variable
        cluster = detail_clusters[name_cluster]
        # add the campaign properties to the database
        id_camp_prop = addCampProp(id_campaign, id_cluster, getProjectName(cluster), json.dumps(cluster))

def setParams(params, id_campaign):
    for param in params:
        # add the parameter to the database and get the id
        id_params = addParamWithoutName (id_campaign, param)
        # add the job to the database and get the id
        id_job = addJob (id_campaign, id_params)
        # add the event to the database
        id_event = addEvent (2, id_job, "CREATED", "Campaign created")

def jdl_parser(option, json_jdl):
    if option == "-s":
        jdl = json_jdl
    elif option == "-f":
        jdl = get_json(json_jdl)
    else:
        print("Usage:   python parser.py -f <json_jdl_file>")
        print("         python parser.py -s <json_jdl_string>")
        sys.exit(1)
        
    # Get the user
    #TODO: Replace environment variable by a better solution (security)
    user = os.environ.get("USER")

    # Get the campaign properties
    name_campaign = getCampaignName(jdl)
    type_job = getJobType(jdl)
    params = getParams(jdl)
    nb_jobs = getNbJobs(jdl)
    
    # Add the campaign to the database and get the id
    id_campaign = addCampaign(user, name_campaign, type_job, nb_jobs, json.dumps(jdl))

    # Get the campaign properties for each informed cluster and add them to the database in
    setCampaignProperties(jdl, id_campaign)

    # Add the parameters to the database
    setParams(params, id_campaign)

        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:   python parser.py -f <json_jdl_file>")
        print("         python parser.py -s <json_jdl_string>")
        sys.exit(1)

    option = sys.argv[1]
    json_jdl = sys.argv[2]
    jdl_parser(option, json_jdl)
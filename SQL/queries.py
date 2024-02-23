from sqlalchemy import *

from datetime import datetime
import sys

sys.path.append(sys.path[0].replace("/SQL", ""))

from SQL.Config_BDD import *

def executeQuery (query):
    with engine.connect() as connect:
        connect.execute(query)
        connect.commit()

def executeQueryReturn (query):
    with engine.connect() as connect:
        res = connect.execute(query)
        connect.commit()

        result = res.scalar()
        #results_as_dict = res.mappings().all()
    print("executeQueryReturn:", result)
    return result

### CAMPAIGNS

def deleteCampaign (id):
    deleteCampaign = delete(campagnes).where(campagnes.c.id == id)
    executeQuery(deleteCampaign)

def killCampaign (id):
    killCampaign = update(campagnes).where(campagnes.c.id == id).values(state = campaign_state(1)) # should be contrained and not be updated
    executeQuery(killCampaign)

def addCampaign (grid_user, name, type, nbjobs, jdl):
    addCampaign = insert(campagnes).values(grid_user = grid_user, name = name, type = type, nb_jobs = nbjobs, jdl = jdl, state = campaign_state(2), submission_time = datetime.now())
    executeQuery(addCampaign)

def selectCampaign (grid_user, name, type, nbjobs, jdl):
    selectCampaign = select(campagnes.c.id).where(campagnes.c.name == name, campagnes.c.grid_user == grid_user, campagnes.c.type == type, campagnes.c.nb_jobs == nbjobs, campagnes.c.jdl == jdl)
    return executeQueryReturn (selectCampaign)

### CAMPAIGN_PROPERTIES

def deleteCampProp ():
    killCampProp = delete(campaign_properties).where(campaign_properties.c.id == id)
    executeQuery(killCampProp)

def addCampProp (id_campaign, id_cluster, name, value):
    addCampProp = insert(campaign_properties).values(campaign_id = id_campaign, cluster_id = id_cluster, name = name, value = value)
    executeQuery(addCampProp)

### CLUSTER
    
def selectCluster (name):
    selectCluster = select(cluster_table.c.id).where(cluster_table.c.name == name)
    return executeQueryReturn (selectCluster)

### JOBS

def deleteJob(id):
    killJob = delete(jobs).where(jobs.c.id == id)
    executeQuery(killJob)

def killJob (id):
    killJob = update(jobs).where(jobs.c.id == id).values(state = 0)
    executeQuery(killJob)

def addJob (campaign_id, param_id):
    addJob = insert(jobs).values(campaign_id = campaign_id, param_id = param_id, submission_time = datetime.now(), state = job_state(1))
    executeQuery(addJob)
    
    """
    id_param = select([parameters.c.id]).where(parameters.c.campaign_id == campaign_id).where(parameters.c.name == name)
    
    with engine.connect() as connect:
        res = connect.execute(id_param)
        connect.commit()

    addJob = insert(jobs).values(campaign_id = campaign_id, param_id = res, state=job_state(1))
    executeQuery(addJob)
    """

### PARAMETERS

def deleteParam (id):
    killParam = delete(parameters).where(parameters.c.id == id)
    executeQuery(killParam)
    
def addParam (campaign_id, name, param):
    addParam = insert(parameters).values(campaign_id = campaign_id, name = name, param = param)
    executeQuery(addParam)

def selectParam (campaign_id, name, param):
    selectParam = select(parameters.c.id).where(parameters.c.campaign_id == campaign_id, parameters.c.name == name, parameters.c.param == param)
    return executeQueryReturn (selectParam)

if __name__ == "__main__":
    killCampaign(2)
    #addJob(1, "job1", "param1")


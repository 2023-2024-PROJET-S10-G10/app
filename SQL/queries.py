import sys
from datetime import datetime

from sqlalchemy import insert, delete, update, select

from utils.sql import validation

# Appends the parent directory of the current directory to the Python module search path.
sys.path.append(sys.path[0].replace("/SQL", ""))

from SQL.Config_BDD import (
    engine,
    campagnes,
    campaign_state,
    events,
    event_class,
    event_state,
    checkbox,
    campaign_properties,
    cluster_table,
    jobs,
    job_state,
    parameters,
    bag_of_tasks,
    users_mapping,
)


def executeQuery(query):
    with engine.connect() as connect:
        connect.execute(query)
        connect.commit()


def executeQueryReturn(query):
    with engine.connect() as connect:
        res = connect.execute(query)
        connect.commit()

        result = res.scalar()
    print("executeQueryReturn:", result)
    return result


def executeQueryReturnList(query):
    with engine.connect() as connect:
        res = connect.execute(query)
        connect.commit()

        queryRes = res.all()
        result = []
        for elt in queryRes:
            keys = enumerate(res.keys())
            obj = {}
            for i, key in keys:
                obj[key] = elt[i]
            result.append(obj)
    print("executeQueryReturn:", result)
    return result


def executeQueryReturnAll(query):
    with engine.connect() as connect:
        res = connect.execute(query)
        connect.commit()
        queryRes = res.all()
        result = []
        for elt in queryRes:
            keys = enumerate(res.keys())
            obj = {}
            for i, key in keys:
                obj[key] = elt[i]
            result.append(obj)
    print("executeQueryReturn:", result)
    return result


### CAMPAIGNS


def deleteCampaign(id):
    deleteCampaign = delete(campagnes).where(campagnes.c.id == id)
    executeQuery(deleteCampaign)


def killCampaign(id):
    state = selectCampState(id)

    killCampaign = (
        update(campagnes)
        .where(campagnes.c.id == id, campagnes.c.state != campaign_state(4))
        .values(state=campaign_state(1))
    )
    executeQuery(killCampaign)


def addCampaign(grid_user, name, type, nbjobs, jdl):
    if nbjobs < 0:
        raise ValueError("The number of jobs (nbjobs) cannot be negative.")

    submission_time = datetime.now()
    addCampaign = insert(campagnes).values(
        grid_user=grid_user,
        name=name,
        type=type,
        nb_jobs=nbjobs,
        jdl=jdl,
        state=campaign_state(2),
        submission_time=submission_time,
    )
    executeQuery(addCampaign)
    return selectCampaign(grid_user, name, type, nbjobs, jdl, submission_time)


def updateStateCampaign(id, state):
    updateCampaign = (
        update(campagnes)
        .where(
            campagnes.c.id == id,
            campagnes.c.state != campaign_state(1),
            campagnes.c.state != campaign_state(4),
        )
        .values(state=campaign_state(state))
    )
    executeQuery(updateCampaign)


def selectCampaign(grid_user, name, type, nbjobs, jdl, submission_time):
    selectCampaign = select(campagnes.c.id).where(
        campagnes.c.name == name,
        campagnes.c.grid_user == grid_user,
        campagnes.c.type == type,
        campagnes.c.nb_jobs == nbjobs,
        campagnes.c.jdl == jdl,
        campagnes.c.submission_time == submission_time,
    )
    return executeQueryReturn(selectCampaign)


def showCampaign(id):
    showCampaign = select(
        campagnes.c.grid_user,
        campagnes.c.state,
        campagnes.c.type,
        campagnes.c.name,
        campagnes.c.submission_time,
        campagnes.c.completion_time,
        campagnes.c.nb_jobs,
        campagnes.c.jdl,
    ).where(campagnes.c.id == id)
    return executeQueryReturnList(showCampaign)


def selectCampaignsFromUser(username):
    selectCampaignsFromUser = select(campagnes.c.id, campagnes.c.name).where(
        campagnes.c.grid_user == username
    )
    return executeQueryReturnList(selectCampaignsFromUser)


def selectOpenCampaignsFromUser(username):
    selectOpenCampaignsFromUser = select(
        campagnes.c.id, campagnes.c.name
    ).where(
        campagnes.c.grid_user == username,
        campagnes.c.state != campaign_state.cancelled,
        campagnes.c.state != campaign_state.terminated,
    )
    return executeQueryReturnList(selectOpenCampaignsFromUser)


def selectCampJDL(id):
    selectCampJDL = select(campagnes.c.jdl).where(campagnes.c.id == id)
    return executeQueryReturn(selectCampJDL)


def selectCampState(id):
    selectCampState = select(campagnes.c.state).where(campagnes.c.id == id)
    return executeQueryReturn(selectCampState)


def selectCampName(id):
    selectCampName = select(campagnes.c.name).where(campagnes.c.id == id)
    return executeQueryReturn(selectCampName)


def selectCampGridUser(id):
    selectCampGridUser = select(campagnes.c.grid_user).where(
        campagnes.c.id == id
    )
    return executeQueryReturn(selectCampGridUser)


def selectCampType(id):
    selectCampType = select(campagnes.c.type).where(campagnes.c.id == id)
    return executeQueryReturn(selectCampType)


def selectCampNbJobs(id):
    selectCampNbJobs = select(campagnes.c.nb_jobs).where(campagnes.c.id == id)
    return executeQueryReturn(selectCampNbJobs)


### EVENTS


def addEvent(class_e, id, code, msg, notified=False):
    if id <= 0:
        raise ValueError("The id cannot be negative.")
    date_open = datetime.now()
    if class_e == 1:  # cluster
        addEvent = insert(events).values(
            class_e=event_class(class_e),
            code=code,
            state=event_state(1),
            cluster_id=id,
            date_open=date_open,
            date_update=date_open,
            notified=notified,
            message=msg,
        )
    elif class_e == 2:  # job
        id_campaign = selectCampJobs(id)
        addEvent = insert(events).values(
            class_e=event_class(class_e),
            code=code,
            campaign_id=id_campaign,
            state=event_state(1),
            job_id=id,
            date_open=date_open,
            date_update=date_open,
            notified=notified,
            message=msg,
        )
    elif class_e == 3:  # campaign
        addEvent = insert(events).values(
            class_e=event_class(class_e),
            code=code,
            campaign_id=id,
            state=event_state(1),
            date_open=date_open,
            date_update=date_open,
            notified=notified,
            message=msg,
        )
    elif class_e == 4:  # notify
        addEvent = insert(events).values(
            class_e=event_class(class_e),
            code=code,
            state=event_state(1),
            date_open=date_open,
            date_update=date_open,
            notified=notified,
            message=msg,
        )
    elif class_e == 5:  # log
        addEvent = insert(events).values(
            class_e=event_class(class_e),
            code=code,
            state=event_state(1),
            date_open=date_open,
            date_update=date_open,
            notified=notified,
            message=msg,
        )
    else:  # others
        return -1
    executeQuery(addEvent)
    return selectEvent(date_open)


def selectEvent(date_open):
    selectEvent = select(events.c.id).where(events.c.date_open == date_open)
    return executeQueryReturn(selectEvent)


def updateParentEvent(id, parent):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    date_update = datetime.now()
    updateEvent = (
        update(events)
        .where(events.c.id == id)
        .values(parent=parent, date_update=date_update)
    )
    executeQuery(updateEvent)


def updateCheckedEvent(id, checked):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    date_update = datetime.now()
    updateEvent = (
        update(events)
        .where(events.c.id == id)
        .values(checked=checkbox(checked), date_update=date_update)
    )
    executeQuery(updateEvent)


def updateNotifiedEvent(id, notified):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    date_update = datetime.now()
    updateEvent = (
        update(events)
        .where(events.c.id == id)
        .values(notified=notified, date_update=date_update)
    )
    executeQuery(updateEvent)


def selectEventState(id):
    selectEventState = select(events.c.state).where(events.c.id == id)
    return executeQueryReturn(selectEventState)


def selectEventCode(id):
    selectEventCode = select(events.c.code).where(events.c.id == id)
    return executeQueryReturn(selectEventCode)


def selectEventClass(id):
    selectEventClass = select(events.c.class_e).where(events.c.id == id)
    return executeQueryReturn(selectEventClass)


def selectEventParent(id):
    selectEventParent = select(events.c.parent).where(events.c.id == id)
    return executeQueryReturn(selectEventParent)


def selectEventMessage(id):
    selectEventMessage = select(events.c.message).where(events.c.id == id)
    return executeQueryReturn(selectEventMessage)


def selectEventChecked(id):
    selectEventChecked = select(events.c.checked).where(events.c.id == id)
    return executeQueryReturn(selectEventChecked)


def selectEventNotified(id):
    selectEventNotified = select(events.c.notified).where(events.c.id == id)
    return executeQueryReturn(selectEventNotified)


def selectEventGlobal(id):
    selectEvent = select(
        events.c.class_e,
        events.c.code,
        events.c.state,
        events.c.cluster_id,
        events.c.campaign_id,
        events.c.job_id,
        events.c.date_open,
        events.c.date_closed,
        events.c.date_update,
        events.c.parent,
        events.c.checked,
        events.c.notified,
        events.c.message,
    ).where(events.c.id == id)
    return executeQueryReturn(selectEvent)


def selectOpenEventsFromCampaign(id_campaign):
    selectEvents = select(
        events.c.id, events.c.code, events.c.checked, events.c.date_update
    ).where(
        events.c.campaign_id == id_campaign, events.c.state == event_state.open
    )
    return executeQueryReturnList(selectEvents)


def selectOpenEvents():
    selectEvents = select(
        events.c.id, events.c.code, events.c.checked, events.c.date_update
    ).where(events.c.state == event_state.open)
    return executeQueryReturnList(selectEvents)


def closeEvent(id):
    date_closed = datetime.now()
    closeEvent = (
        update(events)
        .where(events.c.id == id)
        .values(
            state=event_state(2),
            date_closed=date_closed,
            date_update=date_closed,
        )
    )
    executeQuery(closeEvent)


### CAMPAIGN_PROPERTIES


def deleteCampProp(id):
    killCampProp = delete(campaign_properties).where(
        campaign_properties.c.id == id
    )
    executeQuery(killCampProp)


def addCampProp(id_campaign, id_cluster, name, value):
    if id_campaign <= 0:
        raise ValueError("The id_campaign cannot be negative.")
    if id_cluster <= 0:
        raise ValueError("The id_cluster cannot be negative.")

    addCampProp = insert(campaign_properties).values(
        campaign_id=id_campaign, cluster_id=id_cluster, name=name, value=value
    )
    executeQuery(addCampProp)
    return selectCampProp(id_campaign, id_cluster, name, value)


def selectCampProp(id_campaign, id_cluster, name, value):
    selectCampProp = select(campaign_properties.c.id).where(
        campaign_properties.c.campaign_id == id_campaign,
        campaign_properties.c.cluster_id == id_cluster,
        campaign_properties.c.name == name,
        campaign_properties.c.value == value,
    )
    return executeQueryReturn(selectCampProp)


def selectCampPropValue(id):
    selectCampPropValue = select(campaign_properties.c.value).where(
        campaign_properties.c.id == id
    )
    return executeQueryReturn(selectCampPropValue)


### CLUSTER


def getClusters():
    getClusters = select(cluster_table.c.id, cluster_table.c.name)
    return executeQueryReturnList(getClusters)


def selectCluster(name):
    selectCluster = select(cluster_table.c.id).where(
        cluster_table.c.name == name
    )
    return executeQueryReturn(selectCluster)


def selectClusterById(id):
    selectClusterId = select(cluster_table.columns).where(
        cluster_table.c.id == int(id)
    )
    return executeQueryReturnAll(selectClusterId)


### JOBS


def deleteJob(id):
    killJob = delete(jobs).where(jobs.c.id == id)
    executeQuery(killJob)


def killJob(id):
    killJob = (
        update(jobs)
        .where(jobs.c.id == id, jobs.c.state != job_state(6))
        .values(state=job_state(9))
    )
    executeQuery(killJob)


def addJob(campaign_id, param_id):
    if campaign_id is None:
        raise ValueError("The campaign_id cannot be None.")
    if campaign_id <= 0:
        raise ValueError("The campaign_id cannot be negative.")
    if param_id is None:
        raise ValueError("The param_id cannot be None.")
    if param_id <= 0:
        raise ValueError("The param_id cannot be negative.")

    submission_time = datetime.now()
    addJob = insert(jobs).values(
        campaign_id=campaign_id,
        param_id=param_id,
        submission_time=submission_time,
        state=job_state(1),
    )
    executeQuery(addJob)
    return selectJob(campaign_id, param_id)


def updateStateJob(id, state):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    updateJob = (
        update(jobs)
        .where(
            jobs.c.id == id,
            jobs.c.state != job_state(6),
            jobs.c.state != job_state(9),
        )
        .values(state=job_state(state))
    )
    executeQuery(updateJob)


def selectJob(campaign_id, param_id):
    selectJob = select(jobs.c.id).where(
        jobs.c.campaign_id == campaign_id, jobs.c.param_id == param_id
    )
    return executeQueryReturn(selectJob)


def selectCampJobs(id):
    selectJobs = select(jobs.c.campaign_id).where(jobs.c.id == id)
    return executeQueryReturn(selectJobs)


def selectJobState(id_job):
    selectJobState = select(jobs.c.state).where(jobs.c.id == id_job)
    return executeQueryReturn(selectJobState)


def selectJobParam(id_job):
    selectJobParam = select(jobs.c.param_id).where(jobs.c.id == id_job)
    return executeQueryReturn(selectJobParam)


### PARAMETERS


def deleteParam(id):
    killParam = delete(parameters).where(parameters.c.id == id)
    executeQuery(killParam)


def addParamWithoutName(campaign_id, param):
    if campaign_id <= 0:
        raise ValueError("The campaign_id cannot be negative.")

    addParam = insert(parameters).values(campaign_id=campaign_id, param=param)
    executeQuery(addParam)
    return selectParam(campaign_id, param)


def addParam(campaign_id, name, param):
    if campaign_id <= 0:
        raise ValueError("The campaign_id cannot be negative.")

    addParam = insert(parameters).values(
        campaign_id=campaign_id, name=name, param=param
    )
    executeQuery(addParam)
    return selectParam(campaign_id, param)


def selectParam(campaign_id, param):
    selectParam = select(parameters.c.id).where(
        parameters.c.campaign_id == campaign_id, parameters.c.param == param
    )
    return executeQueryReturn(selectParam)


def selectParams(id):
    selectParams = select(parameters.c.param).where(parameters.c.id == id)
    return executeQueryReturn(selectParams)


def selectParamName(id):
    selectParamName = select(parameters.c.name).where(parameters.c.id == id)
    return executeQueryReturn(selectParamName)


def updateParamValue(id, param):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    updateParamValue = (
        update(parameters).where(parameters.c.id == id).values(param=param)
    )
    executeQuery(updateParamValue)


def updateParamName(id, name):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    updateParam = (
        update(parameters).where(parameters.c.id == id).values(name=name)
    )
    executeQuery(updateParam)


### BAG OF TASKS


def addBagOfTask(id_campaign, id_param, priority):
    if id_campaign <= 0:
        raise ValueError("The id_campaign cannot be negative.")

    # Check the validity of priority
    prio = validation(priority, 10)

    addBagOfTask = insert(bag_of_tasks).values(
        campaign_id=id_campaign, param_id=id_param, priority=prio
    )
    executeQuery(addBagOfTask)
    return selectBagOfTask(id_campaign, id_param)


def selectBagOfTask(id_campaign, id_param):
    if id_campaign <= 0:
        raise ValueError("The id_campaign cannot be negative.")
    if id_param <= 0:
        raise ValueError("The id_param cannot be negative.")

    selectBagOfTask = select(bag_of_tasks.c.id).where(
        bag_of_tasks.c.campaign_id == id_campaign,
        bag_of_tasks.c.param_id == id_param,
    )
    return executeQueryReturn(selectBagOfTask)


def updatePriorityBagOfTask(id, priority):
    if id <= 0:
        raise ValueError("The id cannot be negative.")

    # Check the validity of priority
    prio = validation(priority, 10)

    updateBagOfTask = (
        update(bag_of_tasks)
        .where(bag_of_tasks.c.id == id)
        .values(priority=prio)
    )
    executeQuery(updateBagOfTask)


def selectBagOfTaskPriority(id):
    selectBagOfTaskPriority = select(bag_of_tasks.c.priority).where(
        bag_of_tasks.c.id == id
    )
    return executeQueryReturn(selectBagOfTaskPriority)


def selectBagOfTaskCampaign(id):
    selectBagOfTaskCampaign = select(bag_of_tasks.c.campaign_id).where(
        bag_of_tasks.c.id == id
    )
    return executeQueryReturn(selectBagOfTaskCampaign)


def selectBagOfTaskParam(id):
    selectBagOfTaskParam = select(bag_of_tasks.c.param_id).where(
        bag_of_tasks.c.id == id
    )
    return executeQueryReturn(selectBagOfTaskParam)


## USER MAPPING


def addUsersMapping(grid_login, cluster_login, cluster_id):
    addUsersMapping = insert(users_mapping).values(
        grid_login=grid_login,
        cluster_login=cluster_login,
        cluster_id=cluster_id,
    )
    executeQuery(addUsersMapping)
    return selectUsersMapping(grid_login, cluster_login, cluster_id)


def selectUsersMapping(grid_login, cluster_login, cluster_id):
    selectUsersMapping = select(users_mapping.c.id).where(
        users_mapping.c.grid_login == grid_login,
        users_mapping.c.cluster_login == cluster_login,
        users_mapping.c.cluster_id == cluster_id,
    )
    return executeQueryReturn(selectUsersMapping)


## AUTHENTICATION

## JOBS TO LAUNCH

##  QUEUE COUNTS

## ADMISSION RULES

##  USER NOTIFICATION

##  USER PRIORITY

## GRID USER

##  TASKS AFFINITY

## TAPS

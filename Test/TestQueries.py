from TestManager import TestManager
import sys

# Appends the parent directory of the current directory to the Python module search path.
sys.path.append(sys.path[0].replace("/Test", ""))

from SQL.queries import *

id_cluster = 2  #dahu

class QueriesClusterUT(TestManager):
    ## CLUSTER
    def TestCluster(self):
        ### Get back the id of the cluster
        id_cluster_dahu = selectCluster("dahu")
        id_cluster_luke = selectCluster("luke")
        id_cluster_tatooine = selectCluster("tatooine")

        self.assertEqual(id_cluster_dahu, 2)
        self.assertEqual(id_cluster_luke, 1)
        self.assertEqual(id_cluster_tatooine, None)

## CAMPAIGNS
class CreateCampaign(TestManager):
    # Create a campaign with user, name, type, nb jobs and jdl
    def CreateCampaign(self):
        ### Create
        id_campaign = addCampaign("user", "name", "type", 2, "jdl")

        jdl = selectCampJDL(id_campaign)
        self.assertEqual(jdl, "jdl")

        name = selectCampGridUser(id_campaign)
        self.assertEqual(name, "user")

        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.in_treatment)

        nbjobs = selectCampNbJobs(id_campaign)
        self.assertEqual(nbjobs, 2)

        type = selectCampType(id_campaign)
        self.assertEqual(type, "type")

    # Create a campaign without user
    def CreateCampaignWithoutUser(self):
        try:
            ### Create
            id_campaign = addCampaign(null, "name CCWU", "type CCWU", 3, "jdl CCWU")
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

    # Create a campaign without name
    def CreateCampaignWithoutName(self):
        try:
            ### Create
            id_campaign = addCampaign("user CCWN", null, "type CCWN", 4, "jdl CCWN")
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a campaign without jdl
    def CreateCampaignWithoutJdl(self):
        ### Create
        id_campaign = addCampaign("user CCWJ", "name CCWJ", "type CCWJ", 5, None)
        
        jdl = selectCampJDL(id_campaign)
        self.assertEqual(jdl, None)
    
    # Create a campaign with zero job
    def CreateCampaignWithZeroJob(self):
        ### Create
        id_campaign = addCampaign("user CCWZJ", "name CCWZJ", "type CCWZJ", 0, "jdl CCWZJ")
        
        nbjobs = selectCampNbJobs(id_campaign)
        self.assertEqual(nbjobs, 0)
    
    # Create a campaign with a unvalided number of job
    def CreateCampaignWithUnvalidedNbJob(self):
        try:
            ### Create
            id_campaign = addCampaign("user CCWUNJ", "name CCWUNJ", "type CCWUNJ", -1, "jdl CCWUNJ")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
    # Create a campaign without type
    def CreateCampaignWithoutType(self):
        try:
            ### Create
            id_campaign = addCampaign("user CCWT", "name CCWT", None, 6, "jdl CCWT")
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

class SelectCampaignJdl(TestManager):
    # Return a jdl
    def SelectJdl(self):
        ### Create
        id_campaign = addCampaign("user SJ", "name SJ", "type SJ", 7, "jdl SJ")

        jdl = selectCampJDL(id_campaign)
        self.assertEqual(jdl, "jdl SJ")

    # Return an uninformed jdl
    def SelectUninformedJdl(self):
        jdl = selectCampJDL(0)
        self.assertEqual(jdl, None)

class SelectCampaignState(TestManager):
    # Return a state
    def SelectState(self):
        ### Create
        id_campaign = addCampaign("user SS", "name SS", "type SS", 8, "jdl SS")

        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.in_treatment)

class UpdateCampaignState(TestManager):
    ### Update the state
    def UpdateCampaign(self):
        ### Create
        id_campaign = addCampaign("user UC", "name UC", "type UC", 9, "jdl UC")
        
        updateStateCampaign (id_campaign, 3)
        
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.paused)
    
    ### Update the state with a unvalided state
    def UpdateCampaignWithUnvalidedState(self):
        ### Create
        id_campaign = addCampaign("user UCWUS", "name UCWUS", "type UCWUS", 10, "jdl UCWUS")

        state_before = selectCampState(id_campaign)
        try:
            updateStateCampaign (id_campaign, 66)
            self.assertTrue(False)
        except Exception as e:
            state_after = selectCampState(id_campaign)
            self.assertEqual(state_before, state_after)

    ### Update the state of a campaign already terminated
    def UpdateCampaignAlreadyTerminated(self):
        ### Create
        id_campaign = addCampaign("user UCAT", "name UCAT", "type UCAT", 10, "jdl UCAT")
        updateStateCampaign (id_campaign, 4)

        state_before = selectCampState(id_campaign)
        self.assertEqual(state_before, campaign_state.terminated)
        
        try:
            updateStateCampaign (id_campaign, 3)
            self.assertTrue(False)
        except Exception as e:
            state_after = selectCampState(id_campaign)
            self.assertEqual(state_before, state_after)

    ### Cancel a campaign already terminated
    def CancelCampaignAlreadyTerminated(self):
        ### Create
        id_campaign = addCampaign("user CCAT", "name CCAT", "type CCAT", 10, "jdl CCAT")
        updateStateCampaign (id_campaign, 4)

        state_before = selectCampState(id_campaign)
        self.assertEqual(state_before, campaign_state.terminated)
        
        try:
            updateStateCampaign (id_campaign, 1)
            self.assertTrue(False)
        except Exception as e:
            state_after = selectCampState(id_campaign)
            self.assertEqual(state_before, state_after)

class CancelCampaign(TestManager):
    ### Cancel a campaign
    def CancelCampaign(self):
        ### Create
        id_campaign = addCampaign("user CC", "name CC", "type CC", 11, "jdl CC")

        killCampaign(id_campaign)
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.cancelled)
    
    ### Cancel a cancelled campaign
    def CancelCancelledCampaign(self):
        ### Create
        id_campaign = addCampaign("user CCC", "name CCC", "type CCC", 12, "jdl CCC")
        killCampaign(id_campaign)
        state = selectCampState(id_campaign)
        
        self.assertEqual(state, campaign_state.cancelled)

        killCampaign(id_campaign)
        new_state = selectCampState(id_campaign)

        self.assertEqual(state, new_state)
        self.assertEqual(new_state, campaign_state.cancelled)

    ### Cancel a non existed campaign
    def CancelNonExistedCampaign(self):
        killCampaign(0)
        state = selectCampState(0)
        self.assertEqual(state, None)

class SelectCampaign(TestManager):

    def showCampaign(self):
        id_camp = addCampaign("user", "name", "type", 5, "jdl")

        campaign = showCampaign(id_camp)

        self.assertEqual(campaign[0][0], "user")
        self.assertEqual(campaign[0][1], campaign_state.in_treatment)
        self.assertEqual(campaign[0][2], "type")
        self.assertEqual(campaign[0][3], "name")
        self.assertEqual(campaign[0][5], None)
        self.assertEqual(campaign[0][6], 5)
        self.assertEqual(campaign[0][7], "jdl")

    def selectCampaignsFromUser(self):
        id_camp1 = addCampaign("user1", "name", "type", 5, "jdl")
        id_camp2 = addCampaign("user1", "name", "type", 5, "jdl")
        id_camp3 = addCampaign("user1", "name", "type", 5, "jdl")

        campaigns = selectCampaignsFromUser("user1")

        self.assertEqual(campaigns[0][0], id_camp1)
        self.assertEqual(campaigns[1][0], id_camp2)
        self.assertEqual(campaigns[2][0], id_camp3)

    def selectOpenCampaignsFromUser(self):
        id_camp1 = addCampaign("user2", "name", "type", 5, "jdl")
        id_camp2 = addCampaign("user2", "name", "type", 5, "jdl")
        id_camp3 = addCampaign("user2", "name", "type", 5, "jdl")
        killCampaign(id_camp2)

        campaigns = selectOpenCampaignsFromUser("user2")

        self.assertTrue(len(campaigns) == 2)

## PARAMETERS
class CreateParameter(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")

    # Create a parameter
    def CreateParameter(self):
        id_param = addParam(CreateParameter.id_campaign, "name CP", "value CP")
        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CP")
        self.assertEqual(name, "name CP")
    
    # Create a parameter without name
    def CreateParameterWithoutName1(self):
        id_param = addParam(CreateParameter.id_campaign, "", "value CPWN1")

        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CPWN1")
        self.assertNotEqual(name, None)
        self.assertEqual(name, "")

    def CreateParameterWithoutName2(self):
        id_param = addParamWithoutName(CreateParameter.id_campaign, "value CPWN2")

        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CPWN2")
        self.assertEqual(name, None)
    
    # Create a parameter without the parameter's value
    def CreateParameterWithoutValue(self):
        id_param = addParam(CreateParameter.id_campaign, "name CPWV", "")
        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "")
        self.assertNotEqual(name, None)
        self.assertEqual(name, "name CPWV")

### Select parameter name
class SelectParameterName(TestManager):
    # Return an existed name
    def SelectParameterName(self):
        id_param = addParam(CreateParameter.id_campaign, "name SPN", "value SPN")

        name = selectParamName(id_param)
        self.assertEqual(name, "name SPN")
    
    # Return an uniformed name
    def SelectUniformedParameterName(self):
        name = selectParamName(0)
        self.assertEqual(name, None)

### Update name
class UpdateParameterName(TestManager):
    def UpdateParameterName(self):
        id_param = addParam(CreateParameter.id_campaign, "name UPN", "value UPN")

        updateParamName(id_param, "new_name UPN")
        name = selectParamName(id_param)
        self.assertEqual(name, "new_name UPN")

### Update value
class UpdateParameterValue(TestManager):
    def UpdateParameterValue(self):
        id_param = addParam(CreateParameter.id_campaign, "name UPV", "value UPV")

        updateParamValue(id_param, "new_value UPV")
        params = selectParams(id_param)
        self.assertEqual(params, "new_value UPV")

### Delete parameter
class DeleteParameter(TestManager):
    # Delete an existed parameter
    def DeleteParameter(self):
        id_param = addParam(CreateParameter.id_campaign, "name DP", "value DP")

        deleteParam(id_param)
        params = selectParams(id_param)
        self.assertEqual(params, None)
    
    # Delete a non existed parameter
    def DeleteNonExistedParameter(self):
        deleteParam(0)
        params = selectParams(0)
        self.assertEqual(params, None)

## JOBS
class CreateJob(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")

    # Create a job with a campaign and a parameter
    def CreateJob(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name CJ", "value CJ")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)

        self.assertNotEqual(id_job, None)
        id_campaign_job = selectCampJobs(id_job)
        self.assertEqual(CreateJob.id_campaign, id_campaign_job)
        state = selectJobState(id_job)
        self.assertEqual(state, job_state.to_launch)
        id_param_job = selectJobParam(id_job)
        self.assertEqual(id_param_job, id_param)

    # Create a job without campaign
    def CreateJobWithoutCampaign(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name CJWC", "value CJWC")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)

        try:
            id_job = addJob(None, id_param)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
    # Create a job with an unvalided id campaign
    def CreateJobWithUnvalableCampaign(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name CJWUC", "value CJWUC")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        try:
            id_job = addJob(0, id_param)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    # Create a job without id parameter
    def CreateJobWithoutParameter(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name CJWP", "value CJWP")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        try:
            id_job = addJob(CreateJob.id_campaign, None)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
    # Create a job with an unvalided id parameter
    def CreateJobWithUnvalableParameter(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name CJWUP", "value CJWUP")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        try:
            id_job = addJob(CreateJob.id_campaign, 0)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
### UpdateState
class UpdateJobState(TestManager):
    # Update the state
    def UpdateJob(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name UJ", "value UJ")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        updateStateJob(id_job, 3)
        state = selectJobState(id_job)
        self.assertEqual(state, job_state.submitted)
    
    # Update with a unvalided state
    def UpdateJobWithUnvalidedState(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name UJWUS", "value UJWUS")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        state_before = selectJobState(id_job)
        try:
            updateStateJob(id_job, 66)
            self.assertTrue(False)
        except Exception as e:
            state_after = selectJobState(id_job)

            self.assertEqual(state_before, state_after)

### Delete
class DeleteJob(TestManager):
    # Delete a job
    def DeleteJob(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name DJ", "value DJ")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        killJob(id_job)

        state = selectJobState(id_job)

        self.assertEqual(state, job_state.cancelled)
    
    # Delete a non existed job
    def DeleteNonExistedJob(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name DNEJ", "value DNEJ")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        killJob(0)

        state = selectJobState(0)

        self.assertEqual(state, None)
    
    # Update a terminated job
    def UpdateJobTerminated(self):
        # Create a parameter
        id_param = addParam(CreateJob.id_campaign, "name", "value")

        ### Create a job
        id_job = addJob(CreateJob.id_campaign, id_param)
        
        updateStateJob(id_job, 6)
        state_before = selectJobState(id_job)
        self.assertEqual(state_before, job_state.terminated)
        
        try:
            updateStateJob(id_job, 4)
            self.assertTrue(False)
        except Exception as e:
            state_after = selectJobState(id_job)

            self.assertEqual(state_before, state_after)

## CAMPAIGN_PROPERTIES
class QueriesCampaignPropertiesUT(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")

    ### Create a campaign property
    id_camp_prop = addCampProp(id_campaign, id_cluster, "project", "json")

class CreateCampProp(TestManager):
    # Create a campaign property
    def CreateCampProp(self):
        ### Create a campaign property
        id_camp_prop = addCampProp(QueriesCampaignPropertiesUT.id_campaign, id_cluster, "project", "json")
        
        value = selectCampPropValue(id_camp_prop)

        self.assertEqual(value, "json")
        self.assertNotEqual(id_camp_prop, None)

    # Create a campaign property without value
    def CreateCampPropWithoutValue(self):
        try:
            id_camp_prop = addCampProp(QueriesCampaignPropertiesUT.id_campaign, id_cluster, "project", None)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a campaign property without id cluster
    def CreateCampPropWithoutCluster(self):
        try:
            id_camp_prop = addCampProp(QueriesCampaignPropertiesUT.id_campaign, None, "project", "json")
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a campaign property with an unvalided id cluster
    def CreateCampPropWithUnvalidedCluster(self):
        try:
            id_camp_prop = addCampProp(QueriesCampaignPropertiesUT.id_campaign, -1, "project", "json")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
    # Create a campaign property without name
    def CreateCampPropWithoutName(self):
        try:
            id_camp_prop = addCampProp(QueriesCampaignPropertiesUT.id_campaign, id_cluster, "", "json")
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

    # Create a campaign property without campaign
    def CreateCampPropWithoutCampaign(self):
        try:
            id_camp_prop = addCampProp(0, id_cluster, "project", "json")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

### Delete a campaign property
class DeleteCampProp(TestManager):
    # Delete a campaign property
    def DeleteCampProp(self):
        deleteCampProp(QueriesCampaignPropertiesUT.id_camp_prop)
        value = selectCampPropValue(QueriesCampaignPropertiesUT.id_camp_prop)
        self.assertEqual(value, None)
    
    # Delete a non existed campaign property
    def DeleteNonExistedCampProp(self):
        deleteCampProp(0)
        value = selectCampPropValue(0)
        self.assertEqual(value, None)

## EVENTS
class QueriesEventsUT(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")
    # Create a parameter
    id_param = addParam(id_campaign, "name", "value")
    # Create a job
    id_job = addJob(id_campaign, id_param)

    ### Create event for a campaign
    def CreateEventsForCampaign(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)
        GetEvents.id_campaign_e = id_event_campaign

        state_campaign = selectEventState(id_event_campaign)
        code_campaign = selectEventCode(id_event_campaign)
        class_campaign = selectEventClass(id_event_campaign)
        parent_campaign = selectEventParent(id_event_campaign)
        msg_campaign = selectEventMessage(id_event_campaign)
        checked_campaign = selectEventChecked(id_event_campaign)
        notified_campaign = selectEventNotified(id_event_campaign)

        self.assertNotEqual(id_event_campaign, None)
        self.assertEqual(state_campaign, event_state.open)
        self.assertEqual(code_campaign, "code campagne")
        self.assertEqual(class_campaign, event_class.campaign)
        self.assertEqual(parent_campaign, None)
        self.assertEqual(msg_campaign, "message campagne")
        self.assertEqual(checked_campaign, None)
        self.assertEqual(notified_campaign, False)

    ### Create event for a job
    def CreateEventsForJob(self):
        id_event_job = addEvent(2, QueriesEventsUT.id_job, "code job", "message job", False)
        GetEvents.id_job_e = id_event_job

        state_job = selectEventState(id_event_job)
        code_job = selectEventCode(id_event_job)
        class_job = selectEventClass(id_event_job)
        parent_job = selectEventParent(id_event_job)
        msg_job = selectEventMessage(id_event_job)
        checked_job = selectEventChecked(id_event_job)
        notified_job = selectEventNotified(id_event_job)

        self.assertEqual(state_job, event_state.open)
        self.assertEqual(code_job, "code job")
        self.assertEqual(class_job, event_class.job)
        self.assertEqual(parent_job, None)
        self.assertEqual(msg_job, "message job")
        self.assertEqual(checked_job, None)
        self.assertEqual(notified_job, False)
        self.assertNotEqual(id_event_job, None)

### Get events

class GetEvents(TestManager):
    # ids of events
    id_campaign_e = 0
    id_job_e = 0

    ### get open events related to a campaign
    def GetEventsFromCampaign(self):
        events = selectOpenEventsFromCampaign(QueriesEventsUT.id_campaign)

        self.assertEqual(events[0][0], GetEvents.id_campaign_e)
        self.assertEqual(events[0][1], "code campagne")
        self.assertEqual(events[0][2], None)
        self.assertEqual(events[1][0], GetEvents.id_job_e)
        self.assertEqual(events[1][1], "code job")
        self.assertEqual(events[1][2], None)

    def GetOpenEvents(self):
        events = selectOpenEvents()

        self.assertTrue(len(events)>3)

### UpdateParent
class UpdateEventParent(TestManager):
    # Update the parent
    def UpdateEventParent(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)
        id_event_job = addEvent(2, QueriesEventsUT.id_job, "code job", "message job", False)

        updateParentEvent(id_event_job, id_event_campaign)
        parent_job = selectEventParent(id_event_job)
        self.assertEqual(parent_job, id_event_campaign)

### UpdateChecked
class UpdateEventChecked(TestManager):
    # Update the checked
    def UpdateEventChecked(self):
        id_event_job = addEvent(2, QueriesEventsUT.id_job, "code job", "message job", False)

        updateCheckedEvent(id_event_job, 1)
        checked_job = selectEventChecked(id_event_job)
        self.assertEqual(checked_job, checkbox.yes)

### UpdateNotified
class UpdateEventNotified(TestManager):
    # Update the notified
    def UpdateEventNotified(self):
        id_event_job = addEvent(2, QueriesEventsUT.id_job, "code job", "message job", False)

        updateNotifiedEvent(id_event_job, 1)
        notified_job = selectEventNotified(id_event_job)
        self.assertEqual(notified_job, True)

class DeleteJobEvent(TestManager):
    ### Delete job event
    def CloseJobEvents(self):
        id_event_job = addEvent(2, QueriesEventsUT.id_job, "code job", "message job", False)

        closeEvent(id_event_job)
        state_job = selectEventState(id_event_job)
        self.assertEqual(state_job, event_state.closed)
    
    ### Delete campaign event
    def CloseCampaignEvent(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)

        closeEvent(id_event_campaign)
        state_campaign = selectEventState(id_event_campaign)
        self.assertEqual(state_campaign, event_state.closed)
    
    ### Delete non existed event
    def CloseNonExistedEvent(self):
        closeEvent(0)
        state = selectEventState(0)
        self.assertEqual(state, None)

    ## USER MAPPING

        ### Create

        ### Delete

    ## AUTHENTICATION

        ### Create

        ### Delete

## BAG OF TASK
class QueriesBagOfTaskUT(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")
    # Create a parameter1
    id_param1 = addParam(id_campaign, "name1", "value1")
    # Create a parameter2
    id_param2 = addParam(id_campaign, "name2", "value2")
    # Create a parameter3
    id_param3 = addParam(id_campaign, "name3", "value3")
    # Create a parameter4
    id_param4 = addParam(id_campaign, "name4", "value4")
    # Create a parameter5
    id_param5 = addParam(id_campaign, "name5", "value5")
    # Create a parameter6
    id_param6 = addParam(id_campaign, "name6", "value6")
    # Create a parameter7
    id_param7 = addParam(id_campaign, "name7", "value7")

class CreateBagOfTask(TestManager):
    # Create a bag of task
    def CreateBagOfTask(self):
        id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, QueriesBagOfTaskUT.id_param1, 8)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 8)

    # Create a bag of task without priority
    def CreateBagOfTaskWithoutPriority(self):
        id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, QueriesBagOfTaskUT.id_param2, None)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 10)

    # Create a bag of task with a unvalided priority
    def CreateBagOfTaskWithUnvalidedPriority(self):
        id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, QueriesBagOfTaskUT.id_param3, -1)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 10)
    
    # Create a bag of task without id campaign
    def CreateBagOfTaskWithoutCampaign(self):
        try:
            id_bag_of_task = addBagOfTask(None, QueriesBagOfTaskUT.id_param4, 10)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a bag of task without id param
    def CreateBagOfTaskWithoutParam(self):
        try:
            id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, None, 10)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a bag of task with an unexisted campaign
    def CreateBagOfTaskWithUnexistedCampaign(self):
        try:
            id_bag_of_task = addBagOfTask(0, QueriesBagOfTaskUT.id_param5, 10)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
    # Create a bag of task with an unexisted param
    def CreateBagOfTaskWithUnexistedParam(self):
        try:
            id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, 0, 10)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)
    
        
### Update Priority
class UpdateBagOfTaskPriority(TestManager):
    # Update the priority
    def UpdateBagOfTaskPriority(self):
        id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, QueriesBagOfTaskUT.id_param6, 10)
        updatePriorityBagOfTask(id_bag_of_task, 5)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 5)

    # Update with a unvalided priority
    def UpdateBagOfTaskWithUnvalidedPriority(self):
        id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, QueriesBagOfTaskUT.id_param7, 10)
        priority_before = selectBagOfTaskPriority(id_bag_of_task)
        try:
            updatePriorityBagOfTask(id_bag_of_task, -1)
        except ValueError as e:
            priority_after = selectBagOfTaskPriority(id_bag_of_task)
            self.assertEqual(priority_before, priority_after)

class QueriesUTClean(TestManager):
    # Delete campaign
    deleteCampaign(QueriesBagOfTaskUT.id_campaign)
    # Delete parameter1
    deleteParam(QueriesBagOfTaskUT.id_param1)
    # Delete parameter2
    deleteParam(QueriesBagOfTaskUT.id_param2)
    # Delete parameter3
    deleteParam(QueriesBagOfTaskUT.id_param3)
    # Delete parameter4
    deleteParam(QueriesBagOfTaskUT.id_param4)
    # Delete parameter5
    deleteParam(QueriesBagOfTaskUT.id_param5)
    # Delete parameter6
    deleteParam(QueriesBagOfTaskUT.id_param6)
    # Delete parameter7
    deleteParam(QueriesBagOfTaskUT.id_param7)

    ## JOBS TO LAUNCH
        
        ### Create

        ### Delete

    ## QUEUE COUNTS
        
        ### Create

        ### Delete

    ## ADMISSION RULES
        
        ### Create

        ### Delete

    ## USER NOTIFICATION
            
        ### Create

        ### Delete

    ## USER PRIORITY
            
        ### Create

        ### Delete

    ## GRID USER
            
        ### Create

        ### Delete

    ## TASKS AFFINITY
            
        ### Create

        ### Delete

    ## TAPS
        
        ### Create

        ### Delete
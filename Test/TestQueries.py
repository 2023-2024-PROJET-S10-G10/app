from TestManager import TestManager
import sys

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
        except Exception as e:
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
        except Exception as e:
            state_after = selectCampState(id_campaign)
            self.assertEqual(state_before, state_after)

class DeleteCampaign(TestManager):
    ### Cancel a campaign
    def DeleteCampaign(self):
        ### Create
        id_campaign = addCampaign("user DC", "name DC", "type DC", 11, "jdl DC")

        killCampaign(id_campaign)
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.cancelled)
    
    ### Cancel a cancelled campaign
    def DeleteCancelledCampaign(self):
        ### Create
        id_campaign = addCampaign("user DCC", "name DCC", "type DCC", 12, "jdl DCC")
        killCampaign(id_campaign)
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.cancelled)

    ### Cancel a non existed campaign
    def DeleteNonExistedCampaign(self):
        killCampaign(0)
        state = selectCampState(0)
        self.assertEqual(state, None)


## PARAMETERS
class QueriesParametersUT(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")

class CreateParameter(TestManager):
    # Create a parameter
    def CreateParameter(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name CP", "value CP")
        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CP")
        self.assertEqual(name, "name CP")
    
    # Create a parameter without name
    def CreateParameterWithoutName1(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "", "value CPWN1")

        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CPWN1")
        self.assertNotEqual(name, None)
        self.assertEqual(name, "")

    def CreateParameterWithoutName2(self):
        id_param = addParamWithoutName(QueriesParametersUT.id_campaign, "value CPWN2")

        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value CPWN2")
        self.assertEqual(name, None)
    
    # Create a parameter without the parameter's value
    def CreateParameterWithoutValue(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name CPWV", "")
        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "")
        self.assertNotEqual(name, None)
        self.assertEqual(name, "name CPWV")

### Select parameter name
class SelectParameterName(TestManager):
    # Return an existed name
    def SelectParameterName(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name SPN", "value SPN")

        name = selectParamName(id_param)
        self.assertEqual(name, "name SPN")
    
    # Return an uniformed name
    def SelectUniformedParameterName(self):
        name = selectParamName(0)
        self.assertEqual(name, None)

### Update name
class UpdateParameterName(TestManager):
    def UpdateParameterName(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name UPN", "value UPN")

        updateParamName(id_param, "new_name UPN")
        name = selectParamName(id_param)
        self.assertEqual(name, "new_name UPN")

### Update value
class UpdateParameterValue(TestManager):
    def UpdateParameterValue(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name UPV", "value UPV")

        updateParamValue(id_param, "new_value UPV")
        params = selectParams(id_param)
        self.assertEqual(params, "new_value UPV")

### Delete parameter
class DeleteParameter(TestManager):
    # Delete an existed parameter
    def DeleteParameter(self):
        id_param = addParam(QueriesParametersUT.id_campaign, "name DP", "value DP")

        deleteParam(id_param)
        params = selectParams(id_param)
        self.assertEqual(params, None)
    
    # Delete a non existed parameter
    def DeleteNonExistedParameter(self):
        deleteParam(0)
        params = selectParams(0)
        self.assertEqual(params, None)

## JOBS
class QueriesJobsUT(TestManager):
    # Create a campaign
    id_campaign = addCampaign("user", "name", 1, 1, "jdl")
    # Create a parameter
    id_param = addParam(id_campaign, "name", "value")

    ### Create a job
    id_job = addJob(id_campaign, id_param)

class CreateJob(TestManager):
    # Create a job with a campaign and a parameter
    def CreateJob(self):
        id_campaign_job = selectCampJobs(QueriesJobsUT.id_job)
        self.assertEqual(QueriesJobsUT.id_campaign, id_campaign_job)
        state = selectJobState(QueriesJobsUT.id_job)
        self.assertEqual(state, job_state.to_launch)
        id_param_job = selectJobParam(QueriesJobsUT.id_job)
        self.assertEqual(id_param_job, QueriesJobsUT.id_param)

    # Create a job without campaign
    def CreateJobWithoutCampaign(self):
        try:
            id_job = addJob(None, QueriesJobsUT.id_param)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a job with an unvalided id campaign
    def CreateJobWithUnvalableCampaign(self):
        try:
            id_job = addJob(0, QueriesJobsUT.id_param)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

    # Create a job without id parameter
    def CreateJobWithoutParameter(self):
        try:
            id_job = addJob(QueriesJobsUT.id_campaign, None)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    # Create a job with an unvalided id parameter
    def CreateJobWithUnvalableParameter(self):
        try:
            id_job = addJob(QueriesJobsUT.id_campaign, 0)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
### UpdateState
class UpdateJobState(TestManager):
    # Update the state
    def UpdateJob(self):
        updateStateJob(QueriesJobsUT.id_job, 3)
        state = selectJobState(QueriesJobsUT.id_job)
        self.assertEqual(state, job_state.submitted)
    
    # Update with a unvalided state
    def UpdateJobWithUnvalidedState(self):
        state_before = selectJobState(QueriesJobsUT.id_job)
        try:
            updateStateJob(QueriesJobsUT.id_job, 66)
        except Exception as e:
            state_after = selectJobState(QueriesJobsUT.id_job)

            self.assertEqual(state_before, state_after)

### Delete
class DeleteJob(TestManager):
    # Delete a job
    def DeleteJob(self):
        killJob(QueriesJobsUT.id_job)

        state = selectJobState(QueriesJobsUT.id_job)

        self.assertEqual(state, job_state.event)
    
    # Delete a non existed job
    def DeleteNonExistedJob(self):
        killJob(0)

        state = selectJobState(0)

        self.assertEqual(state, None)

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
        except Exception as e:
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
        except Exception as e:
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
        
        state_campaign = selectEventState(id_event_campaign)
        code_campaign = selectEventCode(id_event_campaign)
        class_campaign = selectEventClass(id_event_campaign)
        parent_campaign = selectEventParent(id_event_campaign)
        msg_campaign = selectEventMessage(id_event_campaign)
        checked_campaign = selectEventChecked(id_event_campaign)
        notified_campaign = selectEventNotified(id_event_campaign)

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

### UpdateState
class UpdateEventState(TestManager):
    # Update the state
    def UpdateEventState(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)

        updateStateEvent(id_event_campaign, 2)
        state_campaign = selectEventState(id_event_campaign)
        self.assertEqual(state_campaign, event_state.closed)

    # Update with a unvalided state
    def UpdateEventWithUnvalidedState(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)

        state_before = selectEventState(id_event_campaign)
        try:
            updateStateEvent(id_event_campaign, 66)
        except Exception as e:
            state_after = selectEventState(id_event_campaign)
            self.assertEqual(state_before, state_after)
    
### UpdateClass
class UpdateEventClass(TestManager):
    # Update the class
    def UpdateEventClass(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)

        updateClassEvent(id_event_campaign, 4)
        class_campaign = selectEventClass(id_event_campaign)
        self.assertEqual(class_campaign, event_class.notify)

    # Update with a unvalided class
    def UpdateEventWithUnvalidedClass(self):
        id_event_campaign = addEvent(3, QueriesEventsUT.id_campaign, "code campagne", "message campagne", False)

        class_before = selectEventClass(id_event_campaign)
        try:
            updateClassEvent(id_event_campaign, 66)
        except Exception as e:
            class_after = selectEventClass(id_event_campaign)
            self.assertEqual(class_before, class_after)

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
        except Exception as e:
            self.assertTrue(True)
    
    # Create a bag of task with an unexisted param
    def CreateBagOfTaskWithUnexistedParam(self):
        try:
            id_bag_of_task = addBagOfTask(QueriesBagOfTaskUT.id_campaign, 0, 10)
            self.assertTrue(False)
        except Exception as e:
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
        except Exception as e:
            priority_after = selectBagOfTaskPriority(id_bag_of_task)
            self.assertEqual(priority_before, priority_after)

class QueriesBagOfTaskClear(TestManager):
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
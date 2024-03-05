from TestManager import TestManager
import sys

sys.path.append(sys.path[0].replace("/Test", ""))

from SQL.queries import *

id_cluster = 2  #dahu

class QueriesUT(TestManager):
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
    def TestCampaign(self):
        ### Create
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")

        jdl = selectCampJDL(id_campaign)
        self.assertEqual(jdl, "jdl")

        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.in_treatment)

        ### Update
        updateStateCampaign (id_campaign, 3)
        
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.paused)

        ### Delete
        killCampaign(id_campaign)
        state = selectCampState(id_campaign)
        self.assertEqual(state, campaign_state.cancelled)
        #TODO: assert

    ## PARAMETERS
    def TestParameters(self):
        # Create a campaign
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")

        ### Create a parameter
        id_param = addParam(id_campaign, "name", "value")
        params = selectParams(id_param)
        name = selectParamName(id_param)

        self.assertEqual(params, "value")
        self.assertEqual(name, "name")

        ### Update name
        updateParamName(id_param, "new_name")
        name = selectParamName(id_param)
        self.assertEqual(name, "new_name")

        ### Update value
        updateParam(id_param, "new_value")
        params = selectParams(id_param)
        self.assertEqual(params, "new_value")

        ### Delete parameter
        deleteParam(id_param)
        params = selectParams(id_param)
        self.assertEqual(params, None)

        # Delete campaign
        killCampaign(id_campaign)

    ## JOBS
    def TestJobs(self):
        # Create a campaign
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")
        # Create a parameter
        id_param = addParam(id_campaign, "name", "value")

        ### Create a job
        id_job = addJob(id_campaign, id_param)
        id_campaign_job = selectCampJobs(id_job)
        self.assertEqual(id_campaign, id_campaign_job)
        state = selectJobState(id_job)
        self.assertEqual(state, job_state.to_launch)

        ### UpdateState
        updateStateJob(id_job, 2)
        state = selectJobState(id_job)
        self.assertEqual(state, job_state.launching)

        ### Delete
        killJob(id_job)
        state = selectJobState(id_job)
        self.assertEqual(state, job_state.event)

        # Delete parameter
        deleteParam(id_param)
        # Delete campaign
        killCampaign(id_campaign)

    ## CAMPAIGN_PROPERTIES
    def TestCampProp(self):
        # Create a campaign
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")

        ### Create a campaign property
        id_camp_prop = addCampProp(id_campaign, id_cluster, "project", "json")
        value = selectCampPropValue(id_camp_prop)
        self.assertEqual(value, "json")

        ### Delete
        deleteCampProp(id_camp_prop)
        value = selectCampPropValue(id_camp_prop)
        self.assertEqual(value, None)

        # Delete campaign
        killCampaign(id_campaign)

    ## EVENTS
    def TestEvents(self):
        # Create a campaign
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")
        # Create a parameter
        id_param = addParam(id_campaign, "name", "value")
        # Create a job
        id_job = addJob(id_campaign, id_param)

        ### Create event for a campaign
        id_event_campaign = addEvent(3, id_campaign, "code campagne", "message campagne", False)
        state_campaign = selectEventState(id_event_campaign)
        self.assertEqual(state_campaign, event_state.open)
        code_campaign = selectEventCode(id_event_campaign)
        self.assertEqual(code_campaign, "code campagne")
        class_campaign = selectEventClass(id_event_campaign)
        self.assertEqual(class_campaign, event_class.campaign)
        parent_campaign = selectEventParent(id_event_campaign)
        self.assertEqual(parent_campaign, None)
        msg_campaign = selectEventMessage(id_event_campaign)
        self.assertEqual(msg_campaign, "message campagne")
        checked_campaign = selectEventChecked(id_event_campaign)
        self.assertEqual(checked_campaign, None)
        notified_campaign = selectEventNotified(id_event_campaign)
        self.assertEqual(notified_campaign, False)

        ### Create event for a job
        id_event_job = addEvent(2, id_job, "code job", "message job", False)
        state_job = selectEventState(id_event_job)
        self.assertEqual(state_job, event_state.open)
        code_job = selectEventCode(id_event_job)
        self.assertEqual(code_job, "code job")
        class_job = selectEventClass(id_event_job)
        self.assertEqual(class_job, event_class.job)
        parent_job = selectEventParent(id_event_job)
        self.assertEqual(parent_job, None)
        msg_job = selectEventMessage(id_event_job)
        self.assertEqual(msg_job, "message job")
        checked_job = selectEventChecked(id_event_job)
        self.assertEqual(checked_job, None)
        notified_job = selectEventNotified(id_event_job)
        self.assertEqual(notified_job, False)

        ### UpdateState
        updateStateEvent(id_event_campaign, 2)
        state_campaign = selectEventState(id_event_campaign)
        self.assertEqual(state_campaign, event_state.closed)

        ### UpdateClass
        updateClassEvent(id_event_campaign, 4)
        class_campaign = selectEventClass(id_event_campaign)
        self.assertEqual(class_campaign, event_class.notify)

        ### UpdateParent
        updateParentEvent(id_event_job, id_event_campaign)
        parent_job = selectEventParent(id_event_job)
        self.assertEqual(parent_job, id_event_campaign)

        ### UpdateChecked
        updateCheckedEvent(id_event_job, 1)
        checked_job = selectEventChecked(id_event_job)
        self.assertEqual(checked_job, checkbox.yes)

        ### UpdateNotified
        updateNotifiedEvent(id_event_job, 1)
        notified_job = selectEventNotified(id_event_job)
        self.assertEqual(notified_job, True)

        ### Delete
        closeEvent(id_event_campaign)
        closeEvent(id_event_job)

    ## USER MAPPING

        ### Create

        ### Delete

    ## AUTHENTICATION

        ### Create

        ### Delete

    ## BAG OF TASK
    def TestBagOfTask(self):
        # Create a campaign
        id_campaign = addCampaign("user", "name", 1, 1, "jdl")
        # Create a parameter
        id_param = addParam(id_campaign, "name", "value")
        ### Create
        id_bag_of_task = addBagOfTask(id_campaign, id_param, 10)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 10)
        
        ### Update Priority
        updatePriorityBagOfTask(id_bag_of_task, 5)
        priority = selectBagOfTaskPriority(id_bag_of_task)
        self.assertEqual(priority, 5)

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
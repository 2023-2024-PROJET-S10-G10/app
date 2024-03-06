from TestManager import TestManager
import sys

sys.path.append(sys.path[0].replace("/Test", ""))

from Parser.jdl_parser import *
from JdlFiles.jdl_string import *

prefix = "JdlFiles/"

## NO CLUSTER USED + JDL FILE
class NoClusterJdlUT(TestManager):
    
    def test_getCampaignName(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        campaign_name = getCampaignName(jdl)
        self.assertEqual(campaign_name, "test_no_cluster")
    
    def test_getJobType(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getJobType(jdl), "normal")
    
    def test_getParams(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getParams(jdl), ["test-prefect true", "titi true", "tata false", "toto false", "tata true", "titi false", "toto true"])

    def test_getProjectName(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        detail_clusters = jdl.get("clusters")
        detail_clusters_luke = detail_clusters.get("luke")
        detail_clusters_dahu = detail_clusters.get("dahu")

        try:
            name_project_luke = getProjectName(detail_clusters_luke)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
        
        try:
            name_project_dahu = getProjectName(detail_clusters_dahu)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)
    
    def test_getNbJobs(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getNbJobs(jdl), 7)
    
    def test_getClusters(self):
        # import jdl
        jdl_file = prefix + "testNoCluster.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getClusters(jdl), [])


## ONE CLUSTER USED + ONE PARAMETER + JDL FILE
#class OneParameterJdlUT(TestManager):
class OneClusterJdlUT(TestManager):

    def test_getCampaignName(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        campaign_name = getCampaignName(jdl)
        self.assertEqual(campaign_name, "test_one_param_one_cluster")
    
    def test_getJobType(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getJobType(jdl), "desktop_computing")
    
    def test_getParams(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        params = getParams(jdl)

        self.assertEqual(params, ["toto false"])
    
    def test_getProjectName(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        detail_clusters = jdl.get("clusters")
        detail_clusters_luke = detail_clusters.get("luke")
        
        name_project_luke = getProjectName(detail_clusters_luke)

        self.assertEqual(name_project_luke, "prefect_or_not")
    
    def test_getNbJobs(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getNbJobs(jdl), 1)

    def test_getClusters(self):
        jdl_file = prefix + "test1.jdl"
        jdl = get_json(jdl_file)

        self.assertEqual(getClusters(jdl), ["luke"])

## ONE CLUSTER USED + JSON FILE
class OneClusterJdlUT(TestManager):

    def test_getCampaignName(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        campaign_name = getCampaignName(jdl)
        self.assertEqual(campaign_name, "test_one_param_one_cluster")
    
    def test_getJobType(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getJobType(jdl), "desktop_computing")
    
    def test_getParams(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getParams(jdl), ["toto false"])
    
    def test_getProjectName(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        detail_clusters = jdl.get("clusters")
        detail_clusters_luke = detail_clusters.get("luke")
        
        name_project_luke = getProjectName(detail_clusters_luke)

        self.assertEqual(name_project_luke, "prefect_or_not")
    
    def test_getNbJobs(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getNbJobs(jdl), 1)

    def test_getClusters(self):
        jdl_file = prefix + "test1.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getClusters(jdl), ["luke"])


## SEVERAL CLUSTER USED + SEVERAL PARAMETERS + JSON FILE
#class SeveralParameterJdlUT(TestManager):
class SeveralClusterJdlUT(TestManager):

    def test_getCampaignName(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        campaign_name = getCampaignName(jdl)
        self.assertEqual(campaign_name, "test_several_params_several_clusters")

    def test_getJobType(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getJobType(jdl), "normal")
    
    def test_getParams(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getParams(jdl), ["test-prefect true", "titi true", "tata false", "toto false", "tata true", "titi false", "toto true"])
    
    def test_getProjectName(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        detail_clusters = jdl.get("clusters")
        detail_clusters_luke = detail_clusters.get("luke")
        detail_clusters_dahu = detail_clusters.get("dahu")
        
        name_project_luke = getProjectName(detail_clusters_luke)
        name_project_dahu = getProjectName(detail_clusters_dahu)

        self.assertEqual(name_project_luke, "prefect_or_not")
        self.assertEqual(name_project_dahu, "prefect")

    def test_getNbJobs(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getNbJobs(jdl), 7)
    
    def test_getClusters(self):
        jdl_file = prefix + "test2.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getClusters(jdl), ["dahu", "luke"])


## NO PARAMETER + JSON FILE
class NoParameterJdlUT(TestManager):

    def test_getCampaignName(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        campaign_name = getCampaignName(jdl)
        self.assertEqual(campaign_name, "test_no_param")
    
    def test_getJobType(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getJobType(jdl), "normal")
    
    def test_getParams(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getParams(jdl), [])
    
    def test_getProjectName(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        detail_clusters = jdl.get("clusters")
        detail_clusters_luke = detail_clusters.get("luke")
        detail_clusters_dahu = detail_clusters.get("dahu")
        
        name_project_luke = getProjectName(detail_clusters_luke)
        name_project_dahu = getProjectName(detail_clusters_dahu)

        self.assertEqual(name_project_luke, "prefect_or_not")
        self.assertEqual(name_project_dahu, "prefect")
    
    def test_getNbJobs(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getNbJobs(jdl), 0)
    
    def test_getClusters(self):
        jdl_file = prefix + "testNoParam.json"
        jdl = get_json(jdl_file)

        self.assertEqual(getClusters(jdl), ["dahu", "luke"])




from bin.gridclusters import gridclusters
from TestManager import TestManager
from API.apiclient import ApiClientStub
import sys

client1 = ApiClientStub()
client1.mock("get", "/gridusage",
             body=b"""{"items":[{"date":1709652356,"clusters":[{"cluster_name":"dahu","cluster_id":8,"max_resources":6080,"used_resources":0,"used_by_cigri":0,"unavailable_resources":2320},{"cluster_name":"bigfoot","cluster_id":9,"max_resources":694,"used_resources":0,"used_by_cigri":0,"unavailable_resources":646},{"cluster_name":"luke","cluster_id":5,"max_resources":1166,"used_resources":0,"used_by_cigri":0,"unavailable_resources":598}]}],"from":null,"to":null,"total":1}""")
client1.mock("get", "/clusters",
             body=b"""{"items":[{"id":"7","name":"ceciccluster","links":[{"rel":"self","href":"/clusters/7"},{"rel":"parent","href":"/clusters"}]},{"id":"2","name":"froggy","links":[{"rel":"self","href":"/clusters/2"},{"rel":"parent","href":"/clusters"}]},{"id":"9","name":"bigfoot","links":[{"rel":"self","href":"/clusters/9"},{"rel":"parent","href":"/clusters"}]},{"id":"5","name":"luke","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}]},{"id":"8","name":"dahu","links":[{"rel":"self","href":"/clusters/8"},{"rel":"parent","href":"/clusters"}]}],"total":5,"links":[{"rel":"self","href":"/clusters"},{"rel":"parent","href":"/"}]}""")
client1.mock("get", "/clusters/2",
             body=b"""{"id":"2","name":"froggy","api_url":"https://froggy1.ujf-grenoble.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"froggy.ujf-grenoble.fr","batch":"oar2_5","resource_unit":"core","power":"150","properties":"","stress_factor":"0/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/2"},{"rel":"parent","href":"/clusters"}],"blacklisted":true,"under_stress":false}""")
client1.mock("get", "/clusters/5",
             body=b"""{"id":"5","name":"luke","api_url":"https://luke-api.univ-grenoble-alpes.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"luke.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"110","properties":"","stress_factor":"0.31/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")
client1.mock("get", "/clusters/7",
             body=b"""{"id":"7","name":"ceciccluster","api_url":"https://ceciccluster.ujf-grenoble.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"ceciccluster.ujf-grenoble.fr","batch":"oar2_5","resource_unit":"core","power":"12","properties":"","stress_factor":"0/0.8","api_chunk_size":"0","enabled":"t","links":[{"rel":"self","href":"/clusters/7"},{"rel":"parent","href":"/clusters"}],"blacklisted":true,"under_stress":false}""")
client1.mock("get", "/clusters/8",
             body=b"""{"id":"8","name":"dahu","api_url":"https://f-dahu.u-ga.fr:6669/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"f-dahu.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"200","properties":null,"stress_factor":"0.08/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/8"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")
client1.mock("get", "/clusters/9",
             body=b"""{"id":"9","name":"bigfoot","api_url":"https://bigfoot.u-ga.fr:6669/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"bigfoot.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"150","properties":null,"stress_factor":"0.01/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/9"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")

client2 = ApiClientStub()
client2.mock("get", "/gridusage",
             body=b"""{"items":[{"date":1709710038,"clusters":[{"cluster_name":"dahu","cluster_id":8,"max_resources":6080,"used_resources":4693,"used_by_cigri":95,"unavailable_resources":664},{"cluster_name":"bigfoot","cluster_id":9,"max_resources":694,"used_resources":448,"used_by_cigri":0,"unavailable_resources":70},{"cluster_name":"luke","cluster_id":5,"max_resources":1166,"used_resources":137,"used_by_cigri":0,"unavailable_resources":466}]}],"from":null,"to":null,"total":1}""")
client2.mock("get", "/clusters",
             body=b"""{"items":[{"id":"7","name":"ceciccluster","links":[{"rel":"self","href":"/clusters/7"},{"rel":"parent","href":"/clusters"}]},{"id":"2","name":"froggy","links":[{"rel":"self","href":"/clusters/2"},{"rel":"parent","href":"/clusters"}]},{"id":"5","name":"luke","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}]},{"id":"9","name":"bigfoot","links":[{"rel":"self","href":"/clusters/9"},{"rel":"parent","href":"/clusters"}]},{"id":"8","name":"dahu","links":[{"rel":"self","href":"/clusters/8"},{"rel":"parent","href":"/clusters"}]}],"total":5,"links":[{"rel":"self","href":"/clusters"},{"rel":"parent","href":"/"}]}""")
client2.mock("get", "/clusters/2",
             body=b"""{"id":"2","name":"froggy","api_url":"https://froggy1.ujf-grenoble.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"froggy.ujf-grenoble.fr","batch":"oar2_5","resource_unit":"core","power":"150","properties":"","stress_factor":"0/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/2"},{"rel":"parent","href":"/clusters"}],"blacklisted":true,"under_stress":false}""")
client2.mock("get", "/clusters/5",
             body=b"""{"id":"5","name":"luke","api_url":"https://luke-api.univ-grenoble-alpes.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"luke.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"110","properties":"","stress_factor":"0.01/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/5"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")
client2.mock("get", "/clusters/7",
             body=b"""{"id":"7","name":"ceciccluster","api_url":"https://ceciccluster.ujf-grenoble.fr/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"ceciccluster.ujf-grenoble.fr","batch":"oar2_5","resource_unit":"core","power":"12","properties":"","stress_factor":"0/0.8","api_chunk_size":"0","enabled":"t","links":[{"rel":"self","href":"/clusters/7"},{"rel":"parent","href":"/clusters"}],"blacklisted":true,"under_stress":false}""")
client2.mock("get", "/clusters/8",
             body=b"""{"id":"8","name":"dahu","api_url":"https://f-dahu.u-ga.fr:6669/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"f-dahu.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"200","properties":null,"stress_factor":"0.7/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/8"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")
client2.mock("get", "/clusters/9",
             body=b"""{"id":"9","name":"bigfoot","api_url":"https://bigfoot.u-ga.fr:6669/oarapi-cigri/","api_auth_type":"cert","api_auth_header":"X_REMOTE_IDENT","ssh_host":"bigfoot.u-ga.fr","batch":"oar2_5","resource_unit":"core","power":"150","properties":null,"stress_factor":"0.02/0.8","api_chunk_size":"100","enabled":"t","links":[{"rel":"self","href":"/clusters/9"},{"rel":"parent","href":"/clusters"}],"blacklisted":false,"under_stress":false}""")


def gridclustersCaller(infos, more_infos, usage, bars, client):
    print("================================================================================")
    print("$ gridcluster ", end="")
    if infos:
        print("-i ", end="")
    if more_infos:
        print("-I ", end="")
    if usage:
        print("-u ", end="")
    if bars:
        print("-b ", end="")
    print("\n")

    gridclusters(infos, more_infos, usage, bars, client)


original_stdout = sys.stdout
sys.stdout = open("Logs/gridclustersCaller.log", "w")


class appendUT(TestManager):

    def defaultClient1(self):
        gridclustersCaller(False, False, False, False, client=client1)

    def infosClient1(self):
        gridclustersCaller(True, False, False, False, client=client1)

    def more_infosClient1(self):
        self.assertEqual(
            gridclustersCaller(False, True, False, False, client=client1),
            gridclustersCaller(True, True, False, False, client=client1)
        )

    def barsClient1(self):
        gridclustersCaller(False, False, False, True, client=client1)

    def defaultClient2(self):
        gridclustersCaller(False, False, False, False, client=client2)

    def infosClient2(self):
        gridclustersCaller(True, False, False, False, client=client2)

    def more_infosClient2(self):
        self.assertEqual(
            gridclustersCaller(False, True, False, False, client=client2),
            gridclustersCaller(True, True, False, False, client=client2)
        )

    def barsClient2(self):
        gridclustersCaller(False, False, False, True, client=client2)

    def close(self):
        sys.stdout.close()
        sys.stdout = original_stdout

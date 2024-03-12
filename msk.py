from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
from tabulate import tabulate


def check_msk():
    print("<<<<<<<<<<<<<<< MSK >>>>>>>>>>>>>>>")
    # List Managed service Kafka and get latest version
    msk = boto3.client('kafka')
    msk_versions = msk.list_kafka_versions()
    msk_latest_version = msk_versions["KafkaVersions"][-1]["Version"]
    print("Latest Managed Service Kafka version is: " + msk_latest_version)

    # Loop through MSK clusters and list ClusterName and CurrentVersion
    msk_clusters = msk.list_clusters_v2()
    if len(msk_clusters["ClusterInfoList"]) == 0:
        print("No MSK clusters found in account skipping....")
    else:
        cluster_list = []
        for cluster in msk_clusters["ClusterInfoList"]:
            clusters = (cluster["ClusterName"]), (cluster["Provisioned"]["CurrentBrokerSoftwareInfo"]["KafkaVersion"])
            cluster_list.append(clusters)
        print(tabulate(cluster_list, headers=["MSK-Cluster-Name", "Kafka-Version"], tablefmt="fancy_grid"), end="\n")

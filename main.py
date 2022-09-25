from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
# import yaml
from tabulate import tabulate
# import requests

# Getting current AWS account id from assumed in profile
account_id = boto3.client('sts').get_caller_identity().get('Account')
def accounts():
    if  account_id == "":
        account_name = "DEVELOPMENT"
    elif account_id == "":
        account_name = "STAGING"

    print("Using account id:", account_id, account_name)
    # Will only work if account is member of an org don't have perms TODO
    # Account_name = boto3.client('organizations').describe_account(AccountId=account_id).get('Account').get('Name') TODO

# To check version against latest
def check(list1, val):
    x=[val for i in list1 if val in i]
    print(["All up to date :)" if x else "Upgrades are needed!"])

def eks():
    print("<<<<<<<<<<<<<<< EKS >>>>>>>>>>>>>>>")
    ## List Elastic search versions and get latest version
    # eks = boto3.client('eks')
    # response = requests.get('https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss')
    # response.text
    # print(response)
    # latest = $(curl -s https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss | grep "<title>Kubernetes version" | sed -n '1p')
    # eks_latest_version = $(echo $latest| sed 's/[^0-9.]*//g')
    # print("Latest eks version is: " + eks_latest_version)

    # Loop through EKS Clusters and list name and version
    eks_cluster_names = eks.list_clusters()
    if len(eks_cluster_names["clusters"]) == 0:
        print("No EKS clusters found found in account skipping....")
    else:
        cluster_name_list = []
        for name in eks_cluster_names["clusters"]:
            cluster_name_list.append(name)
        version_list = []
        for name in cluster_name_list:
            describe_cluster = eks.describe_cluster(name=name)
            versions = (describe_cluster["cluster"]["name"]),(describe_cluster["cluster"]["version"])
            version_list.append(versions)
    print(tabulate(version_list, headers=["EKS-Cluster-Name","Version"], tablefmt="fancy_grid"), end="\n")
    #check(version_list, es_latest_version)

def kafka():
    print("<<<<<<<<<<<<<<< MSK >>>>>>>>>>>>>>>")
    ## List Managed service Kafka and get latest version
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
            clusters = (cluster["ClusterName"]),(cluster["Provisioned"]["CurrentBrokerSoftwareInfo"]["KafkaVersion"])
            cluster_list.append(clusters)
        print(tabulate(cluster_list, headers=["MSK-Cluster-Name","Kafka-Version"], tablefmt="fancy_grid"), end="\n")
        check(cluster_list, msk_latest_version)

def es():
    print("<<<<<<<<<<<<<<< ElasticSearch >>>>>>>>>>>>>>>")
    ## List Elastic search versions and get latest version
    es = boto3.client('opensearch')
    es_verisons = es.list_versions()
    es_latest_version = es_verisons["Versions"][0]
    print("Latest Elastic Search version is: " + es_latest_version)

    # Loop through ES Domain and list DomainName and EngineVersion
    es_domain_names = es.list_domain_names()
    if len(es_domain_names["DomainNames"]) == 0:
        print("No Elastic Search domains found in account skipping....")
    else:
        domain_name_list = []
        for name in es_domain_names["DomainNames"]:
            names = (name["DomainName"])
            domain_name_list.append(names)
        version_list = []
        for name in domain_name_list:
            describe_domain = es.describe_domain(DomainName=name)
            versions = (describe_domain["DomainStatus"]["DomainName"]),(describe_domain["DomainStatus"]["EngineVersion"])
            version_list.append(versions)
        print(tabulate(version_list, headers=["ES-Domain-Name","Version"], tablefmt="fancy_grid"), end="\n")
        check(version_list, es_latest_version)

def rds():
    print("<<<<<<<<<<<<<<< RDS >>>>>>>>>>>>>>>")
    ## List RDS versions and get latest version
    rds = boto3.client('rds')
    rds_verisons = rds.describe_db_engine_versions()

    aurora_mysql_latest_version = JSONPath('$.DBEngineVersions[?(@.Engine=="aurora-mysql")].EngineVersion').parse(rds_verisons)[0]
    print("Latest Aurora MYSQL version is: " + aurora_mysql_latest_version)

    aurora_mysql_latest_version = JSONPath('$.DBEngineVersions[?(@.Engine=="aurora-postgresql")].EngineVersion').parse(rds_verisons)[-1]
    print("Latest Aurora Postgresql version is: " + aurora_mysql_latest_version)

    # Loop through dbs and list DBClusterIdentifier Engine and EngineVersion
    rds_clusters = rds.describe_db_clusters()
    if len(rds_clusters["DBClusters"]) == 0:
        print("No RDS clusters found in account skipping....")
    else:
        db_list = []
        for db in rds_clusters["DBClusters"]:
            dbs = (db["DBClusterIdentifier"]),(db["Engine"]),(db["EngineVersion"])
            db_list.append(dbs)
        print(tabulate(db_list, headers=["RDS-Name","Engine", "Version"], tablefmt="fancy_grid"), end="\n")
        check(db_list,aurora_mysql_latest_version)

for services in account_id:
    # print("Using account id:", account_id)
    accounts()
    eks()
    kafka()
    es()
    rds()
    break
else:
    print("No valid aws account configured...")
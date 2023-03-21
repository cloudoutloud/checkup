from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
from tabulate import tabulate
# import requests

def eks():
    print("<<<<<<<<<<<<<<< EKS >>>>>>>>>>>>>>>")
    ## List Elastic search versions and get latest version
    eks = boto3.client('eks')
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
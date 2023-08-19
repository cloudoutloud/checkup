from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
from tabulate import tabulate
import requests
import subprocess
from itertools import islice, cycle

def check_eks():
    print("<<<<<<<<<<<<<<< EKS >>>>>>>>>>>>>>>")
    eks = boto3.client('eks')
    response = requests.get('https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss')
    response.text
    latest = "curl -s https://docs.aws.amazon.com/eks/latest/userguide/doc-history.rss | grep '<title>Kubernetes version [0-9]' | sed -n '1p'"
    output = subprocess.check_output(latest, shell=True, universal_newlines=True)
    sed_command = "sed 's/[^0-9.]*//g'"
    eks_latest_version = subprocess.check_output(sed_command, input=output, shell=True, universal_newlines=True)
    print("Latest eks version is: " + eks_latest_version)

    eks_cluster_names = eks.list_clusters()
    if len(eks_cluster_names["clusters"]) == 0:
        print("No EKS clusters found found in account skipping....")
    else:
        # Get cluster names in account
        cluster_name_list = []
        for name in eks_cluster_names["clusters"]:
            cluster_name_list.append(name)

        # Get EKS version for each cluster
        version_list = []
        for name in cluster_name_list:
            describe_cluster = eks.describe_cluster(name=name)
            versions = (describe_cluster["cluster"]["name"]),(describe_cluster["cluster"]["version"])
            version_list.append(versions)
        print(tabulate(version_list, headers=["EKS-Cluster-Name","EKS-Version"], tablefmt="fancy_grid"), end="\n")

        # Get addons for each cluster
        addons_list = []
        for name in cluster_name_list:
            list_addons = eks.list_addons(clusterName=name)
            addons = (list_addons["addons"])
            addons_list.append(addons)
            addons_tuple = tuple(map(tuple, addons_list))
        a = list(zip(cluster_name_list, addons_tuple,))
        print(tabulate(a, headers=["EKS-Cluster-Name","Addons-Installed"], tablefmt="fancy_grid"), end="\n")

        # Split addons_tuple into a list so can use in for loop below
        tuple_to_split = addons_tuple
        addons_string_list = [item for sublist in tuple_to_split for item in sublist]

        # Get addons version for each addon
        addons_version_list = []
        for addon in addons_string_list:
            describe_addons = eks.describe_addon(clusterName=name,addonName=addon)
            addons_version = (describe_addons["addon"]["addonVersion"])
            addons_version_list.append(addons_version)

        # Combined the three list and pair the corresponding elements
        combined_list = []
        for index, (item2, item3) in enumerate(zip(addons_string_list, addons_version_list)):
            item1 = cluster_name_list[index % len(cluster_name_list)]
            combined_list.append((item1, item2, item3))
        print(tabulate(combined_list, headers=["EKS-Cluster-Name", "Addon", "Addon-version"], tablefmt="fancy_grid"), end="\n")
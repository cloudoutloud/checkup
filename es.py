from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
from tabulate import tabulate


def check_es():
    print("<<<<<<<<<<<<<<< ElasticSearch >>>>>>>>>>>>>>>")
    # List Elastic search versions and get latest version
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
            versions = (describe_domain["DomainStatus"]["DomainName"]), (describe_domain["DomainStatus"]["EngineVersion"])
            version_list.append(versions)
        print(tabulate(version_list, headers=["ES-Domain-Name", "Version"], tablefmt="fancy_grid"), end="\n")

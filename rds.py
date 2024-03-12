from traceback import print_tb
import boto3
import boto3.session
import json
from jsonpath import JSONPath
from tabulate import tabulate


def check_rds():
    print("<<<<<<<<<<<<<<< RDS >>>>>>>>>>>>>>>")
    # List RDS versions and get latest version
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
            dbs = (db["DBClusterIdentifier"]), (db["Engine"]), (db["EngineVersion"])
            db_list.append(dbs)
        print(tabulate(db_list, headers=["RDS-Name", "Engine", "Version"], tablefmt="fancy_grid"), end="\n")

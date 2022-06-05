import boto3
import boto3.session
import json
from jsonpath import JSONPath

# If using default profile uncomment line 10,11
my_profile_name = ""
my_session = boto3.session.Session(profile_name = my_profile_name)

# Getting AWS account id from assumed profile
account_id = boto3.client('sts').get_caller_identity().get('Account')
print("Using account id: " + account_id)

## List EKS and get latest version TODO
# eks = boto3.client('eks')
# eks_versions = eks.describe_addon_versions()
# with open('data.json', 'w')as f:
#     json.dump(eks_versions, f)

## List Managed service Kafka and get latest version
msk = boto3.client('kafka')
msk_versions = msk.list_kafka_versions()
# print(json.dumps(msk_versions, indent = 1))
latest_version = msk_versions["KafkaVersions"][-1]["Version"]
print("Latest Managed Service Kafka version is: " + latest_version)

## List Elastic search versions and get latest version
es = boto3.client('opensearch')
es_verisons = es.list_versions()
# print(json.dumps(es_verisons, indent = 1))
es_latest_version = es_verisons["Versions"][0]
print("Latest Elastic Search version is: " + es_latest_version)

## List RDS versions and get latest version
rds = boto3.client('rds')
rds_verisons = rds.describe_db_engine_versions()
# print(json.dumps(rds_verisons, indent = 1))
aurora_mysql_latest_version = JSONPath('$.DBEngineVersions[?(@.Engine=="aurora-mysql")].EngineVersion').parse(rds_verisons)[0]
print("Latest Aurora MYSQL version is: " + aurora_mysql_latest_version)
aurora_mysql_latest_version = JSONPath('$.DBEngineVersions[?(@.Engine=="aurora-postgresql")].EngineVersion').parse(rds_verisons)[-1]
print("Latest Aurora Postgresql version is: " + aurora_mysql_latest_version)


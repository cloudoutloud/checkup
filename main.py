import boto3
from msk import kafka
from es import es
from rds import rds
from eks import eks

# Getting current AWS account id from assumed in profile
account_id = boto3.client('sts').get_caller_identity().get('Account')

# def accounts():
#     if  account_id == "":
#         account_name = "DEVELOPMENT"
#     elif account_id == "":
#         account_name = "STAGING"

#     print("Using account id:", account_id, account_name)

for services in account_id:
    # accounts()
    eks()
    kafka()
    es()
    rds()
    break
else:
    print("No valid aws account configured...")
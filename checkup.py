import boto3
import click
from msk import check_msk
from es import check_es
from rds import check_rds
from eks import check_eks

# Getting current AWS account id from assumed in profile
account_id = boto3.client('sts').get_caller_identity().get('Account')


@click.command()
@click.option('--eks', is_flag=True, help='Elastic Kubernetes Service')
@click.option('--msk', is_flag=True, help='Managed Service Kafka')
@click.option('--es',  is_flag=True, help='OpenSearch Service')
@click.option('--rds', is_flag=True, help='Relational Database Service')
@click.option('--all', is_flag=True, help='Loop through all supported AWS services')
def checkup(eks, msk, es, rds, all):
    if eks:
        check_eks()
    if msk:
        check_msk()
    if es:
        check_es()
    if rds:
        check_rds()
    if all:
        check_eks()
        check_msk()
        check_es()
        check_rds()


if __name__ == '__main__':
    checkup()

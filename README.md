## Checkup :wrench:

A script to check all given AWS managed service versions in a given account.
Print results in table and cross check current version is up to date.

Script will authenticate using your local AWS profile

To use run `python3 checkup.py --help` for full options.

List of AWS managed services supported
- EKS (Elastic Kubernetes Service)
- RDS (Relational Database Service)
- MSK (Managed Streaming for Apache Kafka)
- OpenSearch (AWS elasticsearch offering)
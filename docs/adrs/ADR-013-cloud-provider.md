# ADR-013: AWS

**Status:** Accepted  
**Date:** 2026-04-04  
**Decides:** Cloud provider and production infrastructure

## Decision

AWS is the cloud provider for all production infrastructure.

## Service Mapping

| Platform Need | AWS Service |
|--------------|------------|
| PostgreSQL (canonical OLTP) | RDS for PostgreSQL (or Aurora PostgreSQL) |
| ClickHouse (analytical warehouse) | ClickHouse Cloud on AWS |
| Object storage (raw evidence) | S3 |
| Container orchestration | ECS (Fargate) |
| Secrets management | Secrets Manager |
| DNS / CDN | Route 53 / CloudFront |
| Monitoring | CloudWatch |

## Rationale

- Largest cloud ecosystem — broadest set of managed services, integrations, and tooling
- Largest talent pool — most engineers have AWS experience
- Highest upgrade potential — if the platform grows to need additional services (SQS, Lambda, Redshift, SageMaker), they're native to the ecosystem
- ClickHouse Cloud is available on AWS with low-latency connectivity to RDS and S3

## Implications

- All infrastructure code uses AWS-specific services (not multi-cloud abstractions)
- Local development uses Docker Compose with MinIO (S3-compatible) so code works identically
- boto3 is the Python SDK for all AWS service interactions
- IAM roles and policies manage service permissions

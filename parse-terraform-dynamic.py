#!/usr/bin/env python3
import json
import re
from datetime import datetime

with open('main.tf', 'r') as f:
    tf_content = f.read()

resources = {}
pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s+\{([^}]+)\}'
matches = re.findall(pattern, tf_content, re.DOTALL)

for res_type, res_name, res_body in matches:
    if res_type not in resources:
        resources[res_type] = []
    resources[res_type].append({'name': res_name, 'body': res_body.strip()})

components = []

# KMS
for kms in resources.get('aws_kms_key', []):
    components.append({"type": "cryptographic-asset", "name": kms['name'], "properties": [{"name": "type", "value": "aws_kms_key"}]})

# RDS
for rds in resources.get('aws_db_instance', []):
    components.append({"type": "application", "name": rds['name'], "properties": [{"name": "type", "value": "aws_db_instance"}]})

# Secrets
for secret in resources.get('aws_secretsmanager_secret', []):
    components.append({"type": "platform", "name": secret['name'], "properties": [{"name": "type", "value": "aws_secretsmanager_secret"}]})

# ECR
for ecr in resources.get('aws_ecr_repository', []):
    components.append({"type": "platform", "name": ecr['name'], "properties": [{"name": "type", "value": "aws_ecr_repository"}]})

# CloudWatch
for logs in resources.get('aws_cloudwatch_log_group', []):
    components.append({"type": "platform", "name": logs['name'], "properties": [{"name": "type", "value": "aws_cloudwatch_log_group"}]})

# ALB HTTPS
for listener in resources.get('aws_lb_listener', []):
    if 'HTTPS' in listener['body']:
        components.append({"type": "cryptographic-asset", "name": listener['name'], "properties": [{"name": "type", "value": "aws_lb_listener"}, {"name": "protocol", "value": "HTTPS"}]})

# S3
for s3 in resources.get('aws_s3_bucket', []):
    components.append({"type": "platform", "name": s3['name'], "properties": [{"name": "type", "value": "aws_s3_bucket"}]})

# DynamoDB
for ddb in resources.get('aws_dynamodb_table', []):
    components.append({"type": "platform", "name": ddb['name'], "properties": [{"name": "type", "value": "aws_dynamodb_table"}]})

# SNS
for sns in resources.get('aws_sns_topic', []):
    components.append({"type": "platform", "name": sns['name'], "properties": [{"name": "type", "value": "aws_sns_topic"}]})

cbom = {
    "$schema": "http://cyclonedx.org/schema/bom-1.4.schema.json",
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "serialNumber": "urn:uuid:pqc-web-infra-iac",
    "version": 1,
    "metadata": {
        "timestamp": datetime.now().isoformat() + "+00:00",
        "component": {"type": "application"}
    },
    "components": components
}

import os
os.makedirs('results', exist_ok=True)
with open('results/iac-cbom-dynamic.json', 'w') as f:
    json.dump(cbom, f, indent=2)

print(f"✅ Total components: {len(components)}")
for c in components:
    print(f"  - {c['name']} ({c['type']})")

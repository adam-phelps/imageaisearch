import os
import boto3
from dataclasses import dataclass
from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_rds as rds,
    core
)

#@dataclass
#class IaisInfraStackDbProps(core.StackProps):
   # main_sg = ec2.Vpc

class IaisInfraStackDb(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, main_vpc: object, main_sg: object, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_engine = rds.DatabaseInstanceEngine.maria_db(
            version=rds.MariaDbEngineVersion.VER_10_4_8
        )

        db_instance = rds.DatabaseInstance(self, f"iais-prod-db",
            engine=db_engine,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
            vpc=main_vpc,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.ISOLATED
            }
        )

        db_sg = ec2.SecurityGroup(self, f"iais-sg-db-{str}",
            vpc=main_vpc,
            allow_all_outbound=True,
            description="For DB access.")
        
        db_sg.add_ingress_rule(
            peer=main_sg,
            connection=ec2.Port.tcp(3306)
        )

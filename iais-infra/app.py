#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    core
)

from iais_infra.iais_infra_stack import IaisInfraStack
from iais_infra.iais_infra_mon_stack import IaisInfraMonitorStack


app = core.App()
IaisInfraStack(app, "iais-infra")
#IaisInfraMonitorStack(app, "iais-infra-mon")

app.synth()

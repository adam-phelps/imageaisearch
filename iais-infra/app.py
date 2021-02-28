#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    core
)

from iais_infra.iais_infra_stack import IaisInfraStack
from iais_infra.iais_infra_stack_bootstrap import IaisInfraStackBootstrap
from iais_infra.iais_infra_mon_stack import IaisInfraMonitorStack
from iais_infra.iais_infra_stack_db import IaisInfraStackDb


App = core.App()
BootstrapStack = IaisInfraStackBootstrap = IaisInfraStackBootstrap(
    App,
    "iais-bootstrap")

CoreStack = IaisInfraStack(
    App,
    "iais-infra",
    pub_hosted_zone=BootstrapStack.pub_hosted_zone
    )

'''DbStack = IaisInfraStackDb(
    App, 
    "iais-infra-rds-db",
    main_vpc=CoreStack.vpc,
    main_sg=CoreStack.sg)'''

#IaisInfraMonitorStack(App, "iais-infra-mon")

App.synth()

import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_route53 as r53,
    aws_route53_targets as r53t,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as targets,
    aws_synthetics as synthetics,
    core
)


class IaisInfraMonitorStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Must manually update the https:// url in this file before launching stack.
        canary = synthetics.Canary(self, "HTTPS-Canary",
            schedule=synthetics.Schedule.rate(core.Duration.minutes(10)),
            canary_name="iais-https",
            test=synthetics.Test.custom(
                code=synthetics.Code.from_asset(os.path.join(os.path.dirname(os.path.abspath(__file__)),"canary")),
                handler="index.handler"
            ),
            runtime=synthetics.Runtime.SYNTHETICS_NODEJS_2_2
            )
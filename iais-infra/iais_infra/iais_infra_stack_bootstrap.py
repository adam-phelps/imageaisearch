import os
import boto3
from aws_cdk import (
    aws_route53 as r53,
    core
)


class IaisInfraStackBootstrap(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        pub_hosted_zone = r53.PublicHostedZone(self, f"iais-pubHostedZone",
            zone_name="imageaisearch.com",
            comment="Managed in Google Domains. Redirecting Google domain servers here")

        self.pub_hosted_zone = pub_hosted_zone

                
import os
import boto3
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


class IaisInfraStack(core.Stack):

    
    def __init__(self, scope: core.Construct, id: str, pub_hosted_zone: object, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        sts = boto3.client("sts")
        deploy_account_id = sts.get_caller_identity()["Account"]
        deploy_region = sts.meta.region_name

        #TODO ADD an ASG
        vpc = ec2.Vpc(self, "iais-public",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                name="public",
                subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(
                name="private",
                subnet_type=ec2.SubnetType.ISOLATED),
                ])

        sg = ec2.SecurityGroup(self, f"iais-sg-{str}",
            vpc=vpc,
            allow_all_outbound=True,
            description="For HTTPS access.")

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443)
        )

        self.sg = sg
        self.vpc = vpc

        instance_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        role = iam.Role(self, "iais-web-server-roles",
                        assumed_by = iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AmazonEC2RoleforSSM"
        ))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonRekognitionFullAccess"
        ))


        instance = ec2.Instance(self, "iais-web-server-instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=instance_ami,
            vpc = vpc,
            role = role,
            security_group=sg)

        instance_target = targets.InstanceIdTarget(
            instance_id=instance.instance_id,
            port=443
        )

        lb = elbv2.NetworkLoadBalancer(self, f"iais-lb-{str}",
            vpc=vpc,
            internet_facing=True)

        lb_tg = elbv2.NetworkTargetGroup(self,
            vpc=vpc,
            id=f"iais-tg-{str}",
            port=443,
            targets=[instance_target])
        
        lb_listener = lb.add_listener(f"iais-listener-{str}",
            port=443,
            default_target_groups=[lb_tg])

        r53.ARecord(self, "AliasRecord",
            zone=pub_hosted_zone,
            target=r53.RecordTarget.from_alias(r53t.LoadBalancerTarget(lb)))

        r53.ARecord(self, "AliasRecordWww",
            zone=pub_hosted_zone,
            record_name="www.imageaisearch.com",
            target=r53.RecordTarget.from_alias(r53t.LoadBalancerTarget(lb)))
                
        secrets_man_policy = iam.Policy(self, "iais", 
            roles=[role],
            policy_name="iais-web-server-secrets-manager",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "secretsmanager:GetResourcePolicy",
                        "secretsmanager:GetSecretValue",
                        "secretsmanager:DescribeSecret",
                        "secretsmanager:ListSecretVersionIds"
                    ],
                    resources=[
                        f"arn:aws:secretsmanager:{deploy_region}:{deploy_account_id}:secret:DJANGO_SECRET_KEY-mHAOZX"
                    ]
                )
            ])

        secrets_man_policy.attach_to_role(role)

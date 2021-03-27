from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2


class MyLambdashStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPCを作る
        # そのまま作るとNat Gateway+Elastic IPというモリモリ構成なので
        # オプションでNATを作らないでおく
        self.lambdash_vpc = ec2.Vpc(
            self,
            id="lambdash_vpc",
            nat_gateways=0,
            subnet_configuration=ec2.Vpc.DEFAULT_SUBNETS_NO_NAT,
        )

        # Security Gruopを作る
        # idに日本語をつけると少々バグるので英語で
        self.lambdash_scgr = ec2.SecurityGroup(
            self,
            id="lambdash_security_group",
            vpc=self.lambdash_vpc,
            description="labmdash_security_group",
        )

        ### ingress rule
        # HTTP access
        self.lambdash_scgr.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            description="HTTP",
            connection=ec2.Port.tcp(80),
        )

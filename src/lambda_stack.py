from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from src.my_lambdash_stack import MyLambdashStack


class LambdaStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, stack=MyLambdashStack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        docker_image = aws_lambda.EcrImageCode.from_asset_image(
            directory="src/server"
        )

        # lambdaの実行ロール
        # S3にライブラリーなどを置くのでS3アクセスがいる
        # 雑にFullAccessを付与
        lambda_role = iam.Role(
            self,
            "s3_full_access_from_lambda",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("s3.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    "s3_full_access",
                    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
                ),
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    "lambda_full_access",
                    "arn:aws:iam::aws:policy/AWSLambda_FullAccess",
                ),
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    "lambda_basic_execution",
                    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                ),
            ],
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                resources=["arn:aws:s3:::lambdash-storage" + "/*"],
            )
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "ec2:DescribeNetworkInterfaces",
                    "ec2:CreateNetworkInterface",
                    "ec2:DeleteNetworkInterface",
                    "ec2:DescribeInstances",
                    "ec2:AttachNetworkInterface",
                ],
                resources=["*"],
            )
        )

        lambda_func = aws_lambda.Function(
            self,
            "my_lambdash_function",
            code=docker_image,
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            vpc=stack.lambdash_vpc,
            security_groups=[stack.lambdash_scgr],
            vpc_subnets=stack.lambdash_vpc.public_subnets[0],
            role=lambda_role,
        )

        apigateway.LambdaRestApi(
            self,
            "Lambdash-Endpoint",
            handler=lambda_func,
        )

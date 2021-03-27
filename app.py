#!/usr/bin/env python3

from aws_cdk import core as cdk

from src.my_lambdash_stack import MyLambdashStack
from src.lambda_stack import LambdaStack

app = cdk.App()
stack = MyLambdashStack(app, "MyLambdashStack")
lambdash = LambdaStack(app, "LambdaStack", stack)

app.synth()

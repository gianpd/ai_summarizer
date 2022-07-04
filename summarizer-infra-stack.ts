import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";

import * as path from "path";


export class SummarizerInfraStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const dockerfile = path.join(__dirname, "../../");

    // create AWS lambda function and push image to ECR
    const apiLambda = new lambda.DockerImageFunction(this, "LambdaFunction", {
      code: lambda.DockerImageCode.fromImageAsset(dockerfile),
      timeout: Duration.minutes(1),
      memorySize: 1024,
      environment: {HF_TOKEN: process.env.HF_TOKEN ?? "",},
    });

    // give to apigateway permission to invoke the lambda
    new lambda.CfnPermission(this, "ApiGatewayPermission", {
      functionName: apiLambda.functionArn,
      action: "lambda:InvokeFunction",
      principal: "apigateway.amazonaws.com",
    });


    const summarizerApi = new apiGateway.RestApi(this, "RestApi", {
      restApiName: "Summarizer API",
    })

    summarizerApi.root.addProxy({
      defaultIntegration: new apiGateway.LambdaIntegration(apiLambda)
    })
   }
}
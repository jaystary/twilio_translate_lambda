# SMS Translation through Google Cloud Translate and Twilio

A (dockerized) Lambda that consumes a POST through an API Gateway and Lambda. 

Within the Lambda one can chain a series of Requests into different APIs and then return a response.

In this case we call the Google Translate API and forward the response via Twilio API to a mobile phone via SMS

```
POST Lambda endpoint

Body:

{"to":"+12345678",
"input": "Hello World",
"src": "de",
"dest": "es"}



```

In order for this to work you need:
- An AWS account + programmatic access
Configured locally through aws configure (requires AWS CLI)

- A service account scoped on the Google Translate API
Deployed through creds.json which contains the GC creds

- A Twilio Account + programmatic access
As API Keys in Code/through secrets manager

This repo utizilizes CDK for IaC on AWS for:
- API Gateway
- Lambda with custom container

One could enable Streamlit as a UI if needed by uncommeting the relevant parts.


## What is AWS CDK

[AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) allows to define infrastructre as code. This project uses Python as language.

In order to use this repo, an AWS Account is required, [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed and configured as well as [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) installed.


### A few prerequisits on AWS CDK
AWS CDK has few important commands:
- **cdk deploy** (Deploys infrastructure)
- **cdk destroy** (Destroy deployed infrastructure)
- **cdk diff** (Similiar to a git diff shows differences between deployed and current stacks)
- **cdk ls** (Lists all the stacks/infrastructure in an app)
- **cdk synth** (Synthesizes and prints Cloudformation template)

Under the hood, CDK translates stacks into Cloudformation templates, and these cloudformation templates get created within AWS.

### Deploying the repo via CDK

The actual code of the Lambda resids in model/deployment/app.py

From the root:

Bootstrap CDK onto AWS if this is the first time you deploy CDK into your AWS account_
```
cdk bootstrap aws://YOUR AWS ACCOUNT #/eu-central-1
```

Configure your AWS account in cdk.json.
```
pip install -r requirements.txt
```

```
cdk deploy #Creates the stack/infrastructure
```

```
cdk destroy #Destroys the stack/infrastructure
```

If you change code either in the infrastructure or in the Lambda (including dependencies) just trigger cdk deploy again

To test code, just create a random script file in model/deployment and run your code with the same references as from your lambda.
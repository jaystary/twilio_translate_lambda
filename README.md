# SMS Q&A & Translation through Google Cloud Translate and Twilio

![Architecture](https://user-images.githubusercontent.com/34389140/101979520-fa116080-3c5d-11eb-8c2d-4b25e604c0d5.png)

Proof of concept for a Hackathon. The idea was to build a simple Q&A/Translate pipeline for low resource languages accessible through SMS.

For the quick implementation we used Google Translate / Twilio API. For future applications those API requests can be replaced by self-trained models and chained accordingly.

POST Lambda endpoint

Body:

```
{{"to":"+9949077424",
"input": "Where can i find Yams",
"src": "en",
"dest": "ig",
"qa": {
    "Where can i find Yams": "You can find Yams in the next store"
}
}}

```
The qa dict mocks the Question&Answer model. The response is the translated answer to the question.

In order for this to work it is required to have:
- An AWS account + programmatic access
Configured locally through aws configure (requires AWS CLI)

- A service account scoped on the Google Translate API
Deployed through creds.json which contains the GC creds

- A Twilio Account + programmatic access
As API Keys in Code/through secrets manager

This repo utizilizes CDK for IaC on AWS for:
- API Gateway
- Lambda with custom container

Optional:
- Streamlit as a UI

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

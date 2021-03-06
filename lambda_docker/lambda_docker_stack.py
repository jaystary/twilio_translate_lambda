from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigatewayv2 as api_gw,
    aws_apigatewayv2_integrations as integrations,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_iam as iam,
    aws_logs as logs,
    core
)
from aws_cdk.aws_logs import LogGroup, RetentionDays
import os

MOUNT_POINT = "/mnt/data"
LOG_RETENTION = RetentionDays.ONE_MONTH

"""Infrastructure"""
class LambdaDockerStack(core.Stack):   
    def __init__(self, scope: core.Construct, construct_id: str, name: str,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        """VPC - used in project"""
        vpc = ec2.Vpc(self, f'{name}-VPC', max_azs=2)
        
               
        """Model folder that contains Lambda code"""
        model_folder = os.path.dirname(os.path.realpath(__file__)) + "/../model"
        lambda_handler = _lambda.DockerImageFunction(self, f'{name}-Lambda',
                    code=_lambda.DockerImageCode.from_image_asset(model_folder), 
                    memory_size=128, 
                    timeout=core.Duration.minutes(1), 
                    vpc=vpc)
        
 
        """Custom Log groups for Lambda"""
        lambda_lgs = logs.LogGroup(
            self,
            f'{name}-Lambda-LogGroup',
            log_group_name=f"/aws/lambda/{lambda_handler.function_name}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        """API Gateway - integrates all methods and ressources - used for Lambda invocation"""
        api = api_gw.HttpApi(self, 
                    f'{name}-ApiGw',
                    default_integration=integrations.LambdaProxyIntegration(handler=lambda_handler))
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        #STREAMLIT RELATED START
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        '''
        cluster = ecs.Cluster(self, f"{name}-Streamlit-Cluster", vpc=vpc)
        
        ecs_task = ecs.FargateTaskDefinition(
            self,
            f'{name}-Streamlit-Task-Def',            
        )

        streamlit_container = ecs_task.add_container(
            f'{name}-Streamlit-Container',
            image=ecs.ContainerImage.from_asset('streamlit-docker'),
            essential=True,
            environment={
                'API_URL': api.url,
            },
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=f'{name}-Streamlit-Log'
            )            
        )
        
        streamlit_container.add_port_mappings(
            ecs.PortMapping(
                container_port=8501,
                host_port=8501,
                protocol=ecs.Protocol.TCP
            )
        )
        
        """Efs Volume - shared between Lambda / Streamlit"""
        ecs_task.add_volume(name=f'{name}-Efs-Volume',  
                efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=fs.file_system_id,                
        ))
        
        """Efs Mountpoint"""
        streamlit_container.add_mount_points(
            ecs.MountPoint(
                container_path="/mnt/data",
                read_only=False,
                source_volume=f'{name}-Efs-Volume'
        ))
        
       
        ecs_task.add_to_task_role_policy(
            statement=iam.PolicyStatement(
                actions=["efs:*"],
                resources=['*'],
                effect=iam.Effect.ALLOW
            )
        )
       
        """Fargate Service that hosts the Streamlit Application"""
        ecs_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, f'{name}-Fargate-Service',
            cluster=cluster,            
            cpu=256,                    
            desired_count=1,            
            task_definition = ecs_task,
            memory_limit_mib=512,     
            public_load_balancer=True, 
            platform_version=ecs.FargatePlatformVersion.VERSION1_4, #https://forums.aws.amazon.com/thread.jspa?messageID=960420
            
        )  
        
        fs.connections.allow_default_port_from(
            ecs_service.service.connections)
        '''
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        #STREAMLIT RELATED END
        """"""""""""""""""""""""""""""""""""""""""""""""""""""
        
        core.CfnOutput(self, 'URL', value=api.url);
        

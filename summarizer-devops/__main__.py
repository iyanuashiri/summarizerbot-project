"""An AWS Python Pulumi program"""
import pulumi
import pulumi_aws
from pulumi_aws.lambda_ import FunctionEnvironmentArgs

from resources.ecr_instance import create_repository
from resources.app_runner_instance import create_service, source_config
from resources.lambda_instance import create_function, summarizer_bot_environment, get_mentions_environment, \
    create_summaries_environment
from resources.s3_instance import create_bucket, create_object, ACLBucket, ACLBucketObject

config = pulumi.Config()

canvassly_project_availability_zone = pulumi_aws.config.region

###########################################################################################################
# Elastic Container Registry
###########################################################################################################

ecr_result = create_repository(resource_name_='summarizer-project', name_='summarizer-project')

###############################################################################################################
# App Runner
##############################################################################################################


app_runner_result = create_service(resource_name_='summarizer-project', service_name_='summarizerbot-dev',
                                   source_configuration_=source_config)

new_app_runner_result = create_service(resource_name_='new-summarizer-project', service_name_='new-summarizer-web',
                                       source_configuration_=source_config)

####################################
# Lambda
###################################


create_summaries = create_function(resource_name_='create-summaries-prod', name_='create-summaries-prod',
                                   description='Lambda function to create summaries by an API endpoint',
                                   environment=create_summaries_environment,
                                   image_uri='605344284032.dkr.ecr.us-east-1.amazonaws.com/summarizer-project:create-summaries',
                                   role='arn:aws:iam::605344284032:role/service-role/get-twitter-mentions-role-tvqidii8')

get_mentions = create_function(resource_name_='get-twitter-mentions-prod', name_='get-twitter-mentions-prod',
                               description='Lambda function for getting twitter mentions.',
                               environment=get_mentions_environment,
                               image_uri='605344284032.dkr.ecr.us-east-1.amazonaws.com/summarizer-project:get-mentions',
                               role='arn:aws:iam::605344284032:role/service-role/get-twitter-mentions-role-tvqidii8')

summarizer_bot = create_function(resource_name_='summarizer-bot-prod', name_='summarizer-bot-prod',
                                 description='Twitter bot to summarize an article',
                                 environment=summarizer_bot_environment,
                                 image_uri='605344284032.dkr.ecr.us-east-1.amazonaws.com/summarizer-project:summarizer-bot',
                                 role='arn:aws:iam::605344284032:role/service-role/get-twitter-mentions-role-tvqidii8')

summarizer_ml = create_function(resource_name_='summarizer-ml-prod', name_='summarizer-ml-prod',
                                description='Lambda function to summarize an article by using sumy AI package',
                                image_uri='605344284032.dkr.ecr.us-east-1.amazonaws.com/summarizer-project:summarizer-ml',
                                role='arn:aws:iam::605344284032:role/service-role/get-twitter-mentions-role-tvqidii8',
                                timeout=60)

# Export the name of the bucket
pulumi.export('ecr', ecr_result.repository_url)
pulumi.export('ecr_registry', ecr_result.registry_id)
pulumi.export('create-summaries', create_summaries.urn)
pulumi.export('get-mentions', get_mentions.urn)

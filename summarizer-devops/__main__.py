"""An AWS Python Pulumi program"""
import pulumi
import pulumi_aws

from resources.ecr_instance import create_repository
from resources.app_runner_instance import create_service, source_config


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


# Export the name of the bucket
pulumi.export('ecr', ecr_result.repository_url)
pulumi.export('ecr_registry', ecr_result.registry_id)

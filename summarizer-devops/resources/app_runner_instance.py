import functools
from enum import Enum
from typing import Mapping

from pulumi_aws.apprunner import Service, ServiceSourceConfigurationArgs, \
    ServiceSourceConfigurationAuthenticationConfigurationArgs, ServiceInstanceConfigurationArgs, \
    ObservabilityConfiguration, ServiceObservabilityConfigurationArgs, \
    ObservabilityConfigurationArgs, ObservabilityConfigurationTraceConfigurationArgs, \
    ServiceSourceConfigurationImageRepositoryArgs, ServiceSourceConfigurationImageRepositoryImageConfigurationArgs

# from decouple import config


###########################################################
# Source Configuration
###########################################################

class Connection(Enum):
    GITHUB = 'GITHUB'


class ConfigurationSource(Enum):
    REPOSITORY = 'REPOSITORY'
    API = 'API'


class CodeVersionType(Enum):
    BRANCH = 'BRANCH'


class Runtime(Enum):
    PYTHON_3 = 'PYTHON_3'
    NODEJS_12 = 'NODEJS_12'
    NODEJS_14 = 'NODEJS_14'
    NODEJS_16 = 'NODEJS_16'
    CORRETTO_8 = 'CORRETTO_8'
    CORRETTO_11 = 'CORRETTO_11'
    GO_1 = 'GO_1'
    DOTNET_6 = 'DOTNET_6'
    PHP_81 = 'PHP_81'
    RUBY_31 = 'RUBY_31'


####################################################
# Image Configuration
####################################################

class ImageRepositoryType(Enum):
    ECR = 'ECR'
    ECR_PUBLIC = 'ECR_PUBLIC'


def set_service_source_config(access_role_arn: str, auto_deployments_enabled: bool,
                              image_identifier: str, image_repository_type: str,
                              start_command: str = None, port: str = None,
                              runtime_environment_variables: Mapping[str, str] = None,
                              connection_arn: str = None):
    authentication_configuration = ServiceSourceConfigurationAuthenticationConfigurationArgs(
        access_role_arn=access_role_arn, connection_arn=connection_arn)
    image_config = \
        ServiceSourceConfigurationImageRepositoryImageConfigurationArgs(port=port,
                                                                        runtime_environment_variables=runtime_environment_variables,
                                                                        start_command=start_command)
    image_repo = \
        ServiceSourceConfigurationImageRepositoryArgs(image_identifier=image_identifier,
                                                      image_repository_type=image_repository_type,
                                                      image_configuration=image_config)
    source_configuration = ServiceSourceConfigurationArgs(authentication_configuration=authentication_configuration,
                                                          auto_deployments_enabled=auto_deployments_enabled,
                                                          image_repository=image_repo)
    return source_configuration


ACCESS_ROLE_ARN = 'arn:aws:iam::605344284032:role/app-runner-access-role'
CONNECTION_ARN = 'arn:aws:apprunner:us-east-1:605344284032:connection/iyanuashiri-github' \
                 '/2d48335838a448b3ab693f12a75e2d60'
IMAGE_IDENTIFIER = '605344284032.dkr.ecr.us-east-1.amazonaws.com/summarizer-project:summarizer-web'

# START_COMMAND = 'docker compose up --build'
PORT = '5000'
RUNTIME_ENVIRONMENT = {'SECRET_KEY': 'w&u(3gkaxs2-%*rjdvrjwo4s$pcj0j8gcc4@1#l8h(gn%k#7o_',
                       'ALLOWED_HOSTS': '0.0.0.0:5000, 127.0.0.1:5000,'}

source_config = set_service_source_config(access_role_arn=ACCESS_ROLE_ARN,
                                          auto_deployments_enabled=True,
                                          image_identifier=IMAGE_IDENTIFIER,
                                          image_repository_type=str(ImageRepositoryType.ECR.value),
                                          port=PORT,
                                          runtime_environment_variables=RUNTIME_ENVIRONMENT)


###################################################################################################
# Instance
###################################################################################################

class CPU(Enum):
    ONE_ZERO_TWO_FOUR = 1024
    TWO_ZERO_FOUR_EIGHT = 2048


class Memory(Enum):
    TWO_ZERO_FOUR_EIGHT = 2048
    THREE_ZERO_SEZEN_TWO = 3072
    FOUR_ZERO_NINE_SIX = 4096


INSTANCE_ROLE_ARN = 'arn:aws:iam::605344284032:role/app-runner-instance-role'

service_instance_configuration = \
    ServiceInstanceConfigurationArgs(
        cpu=str(CPU.ONE_ZERO_TWO_FOUR.value),
        # instance_role_arn=INSTANCE_ROLE_ARN,
        memory=str(Memory.TWO_ZERO_FOUR_EIGHT.value)
    )


def manage_instance_configuration(instance_configuration: ServiceInstanceConfigurationArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(instance_configuration=instance_configuration)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


############################################################################################
# Observability
############################################################################################

service_observability_configuration = ServiceObservabilityConfigurationArgs(observability_configuration_arn='',
                                                                            observability_enabled=True)


def manage_observability_configuration(observability_configuration: ServiceObservabilityConfigurationArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(observability_configuration=observability_configuration)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


###########################
#
########################


@manage_instance_configuration(instance_configuration=service_instance_configuration)
def create_service(resource_name_: str, service_name_: str, source_configuration_: ServiceSourceConfigurationArgs,
                   **kwargs):
    service = Service(resource_name=resource_name_, service_name=service_name_,
                      source_configuration=source_configuration_, **kwargs)
    return service

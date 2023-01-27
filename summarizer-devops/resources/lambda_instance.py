import functools
from enum import Enum
from typing import Sequence, Mapping

from pulumi_aws.lambda_ import Function, FunctionImageConfigArgs, FunctionDeadLetterConfigArgs, \
    FunctionEphemeralStorageArgs, FunctionFileSystemConfigArgs, FunctionEnvironmentArgs
from pulumi import Archive


class Architectures(Enum):
    x86_64 = ['x86_64']
    arm64 = ['arm64']


archive = Archive()


class PackageType(Enum):
    ZIP = 'Zip'
    IMAGE = 'Image'

##################################
# Dead Letter Config
##################################


dead_letter_config = FunctionDeadLetterConfigArgs(target_arn='')


def manage_dead_letter_config(dead_letter_config: FunctionDeadLetterConfigArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(dead_letter_config=dead_letter_config)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated

##################################
# Ephemeral Storage
#################################

ephemeral_storage = FunctionEphemeralStorageArgs(size = 1)

def manage_ephemeral_storage(ephemeral_storage: FunctionEphemeralStorageArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(ephemeral_storage=ephemeral_storage)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated

##################################
# Environment
#################################

create_summaries_variables = {'POST_URL': 'https://'}
create_summaries_environment = FunctionEnvironmentArgs(variables=create_summaries_variables)

get_mentions_variables = {}
get_mentions_environment = FunctionEnvironmentArgs(variables=get_mentions_variables)

summarizer_bot_variables = {}
summarizer_bot_environment = FunctionEnvironmentArgs()


def manage_environment(variables: FunctionEnvironmentArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(variables=variables)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated


####################################
# File System Config
###################################

file_system_config = FunctionFileSystemConfigArgs(arn='', local_mount_path='')

def manage_file_system_config(file_system_config: FunctionFileSystemConfigArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(file_system_config=file_system_config)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated

###################################
# Image Config
##################################
image_config = FunctionImageConfigArgs(commands=Sequence['str'], entry_points=Sequence['str'], working_directory='')

def manage_image_config(image_config:FunctionImageConfigArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(image_config=image_config)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated


#####################################
# KMS
#####################################


def manage_kms_key_arn(kms_key_arn: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(kms_key_arn=kms_key_arn)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


####################################
#
####################################

def create_function(resource_name_: str, name_: str, description: str, image_uri: str, role: str,
                    architectures=None,
                    memory_size: int = 128, package_type: str = PackageType.IMAGE.value, publish: bool = False,
                    timeout: int = 3, **kwargs):
    if architectures is None:
        architectures = Architectures.x86_64.value
    function = Function(resource_name=resource_name_, description=description, image_uri=image_uri, role=role,
                        architectures=architectures, memory_size=memory_size, name=name_, package_type=package_type,
                        publish=publish, timeout=timeout, **kwargs)
    return function

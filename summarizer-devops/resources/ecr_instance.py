import functools
from enum import Enum
from typing import Sequence, Mapping

from pulumi_aws.ecr import Repository, RepositoryEncryptionConfigurationArgs, RepositoryImageScanningConfigurationArgs


class ImageTagMutability(Enum):
    IMMUTABLE = 'IMMUTABLE'
    MUTABLE = 'MUTABLE'


def manage_image_scanning_configuration(image_scanning_configuration: RepositoryImageScanningConfigurationArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(image_scanning_configuration=image_scanning_configuration)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated


def manage_mutability(image_tag_mutability: str = str(ImageTagMutability.MUTABLE.value)):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(image_tag_mutability=image_tag_mutability)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated


def manage_encryption_configurations(encryption_configurations_: Sequence[RepositoryEncryptionConfigurationArgs]):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(encryption_configurations=encryption_configurations_)
            result = func(*args, **kwargs)
            return result
        return wrapped
    return decorated


def create_repository(resource_name_: str, name_: str, tags: Mapping[str, str] = None, force_delete: bool = False,
                      **kwargs):
    repository = Repository(resource_name=resource_name_, name=name_, force_delete=force_delete, tags=tags, **kwargs)
    return repository

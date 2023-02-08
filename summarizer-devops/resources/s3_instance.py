import functools
from enum import Enum
from typing import Union

from pulumi_aws.s3 import Bucket, BucketObject, BucketCorsRuleArgs, BucketGrantArgs, BucketLifecycleRuleArgs, \
    BucketLoggingArgs, BucketObjectLockConfigurationRuleArgs, BucketReplicationConfigurationArgs, \
    BucketServerSideEncryptionConfigurationArgs, BucketServerSideEncryptionConfigurationRuleArgs, BucketVersioningArgs, \
    BucketWebsiteArgs, BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs
from pulumi import Asset, Archive


###############################
# Acceleration Status
###############################

class AccelerationStatus(Enum):
    ENABLED = 'Enabled'
    SUSPENDED = 'Suspended'


def manage_acceleration_status(acceleration_status: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(acceleration_status=acceleration_status)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


###############################
# Request Payer
##############################

class RequestPayer(Enum):
    BUCKET_OWNER = 'BucketOwner'
    REQUESTER = 'Requester'


def manage_request_payer(request_payer: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(request_payer=request_payer)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


###############################
# Server Side Encryption
###############################


class EncryptionAlgorithm(Enum):
    AES256 = 'AES256'
    AWS_KMS = 'aws:kms'


def set_server_side_encryption(see_algorithm: str, bucket_key_enabled: bool = True, kms_master_key_id: str = None):
    apply_by_default = BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs \
        (sse_algorithm=str(see_algorithm), kms_master_key_id=kms_master_key_id)

    configuration_rule = BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=apply_by_default,
        bucket_key_enabled=bucket_key_enabled)

    server_side_encryption_configuration = BucketServerSideEncryptionConfigurationArgs(rule=configuration_rule)

    return server_side_encryption_configuration


def manage_server_side_encryption(server_side_encryption_configuration: BucketServerSideEncryptionConfigurationArgs):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(server_side_encryption_configuration=server_side_encryption_configuration)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


#################################################################################################
# Bucket
################################################################################################


class ACLBucket(Enum):
    PRIVATE = 'private'
    PUBLIC_READ = 'public-read'
    PUBLIC_READ_WRITE = 'public-read-write'
    AWS_EXEC_READ = 'aws-exec-read'
    AUTHENTICATED_READ = 'authenticated-read'
    LOG_DELIVERY_WRITE = 'log-delivery-write'


def create_bucket(resource_name: str, acl: str, bucket: str, force_destroy: bool,
                  **kwargs):
    bucket = Bucket(resource_name=resource_name, acl=acl, bucket=bucket, force_destroy=force_destroy, **kwargs)
    return bucket


################################################################################################
# Bucket Object
##############################################################################################


class ACLBucketObject(Enum):
    PRIVATE = 'private'
    PUBLIC_READ = 'public-read'
    PUBLIC_READ_WRITE = 'public-read-write'
    AWS_EXEC_READ = 'aws-exec-read'
    AUTHENTICATED_READ = 'authenticated-read'
    BUCKET_OWNER_READ = 'bucket-owner-read'
    BUCKET_OWNER_FULL_CONTROL = 'bucket-owner-full-control'


def create_object(resource_name: str, acl: str, bucket: str, key: str,
                  source: Union[Asset, Archive], **kwargs):
    bucket_object = BucketObject(resource_name=resource_name, bucket=bucket, acl=acl, key=key, source=source, **kwargs)
    return bucket_object


#####################
# Content
#####################


def manage_content(content: str, content_base64: str, content_disposition: str, content_encoding: str,
                   content_language: str, content_type: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(content=content, content_base64=content_base64, content_disposition=content_disposition,
                          content_encoding=content_encoding, content_language=content_language,
                          content_type=content_type)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


##########################
# Server Side Encryption
##########################

def manage_server_side_encryption_bucket_object(bucket_key_enabled: bool, kms_key_id: str, server_side_encryption: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(bucket_key_enabled=bucket_key_enabled, kms_key_id=kms_key_id,
                          server_side_encryption=server_side_encryption)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


###################################
# Object Lock
###################################

def manage_object_lock(object_lock_legal_hold_status: str, object_lock_mode: str, object_lock_retain_until_date: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(object_lock_legal_hold_status=object_lock_legal_hold_status,
                          object_lock_mode=object_lock_mode,
                          object_lock_retain_until_date=object_lock_retain_until_date)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated


###########################################
# Storage Class
###########################################

class StorageClass(Enum):
    STANDARD = 'STANDARD'
    GLACIER = 'GLACIER'


def manage_storage_class(storage_class: str):
    def decorated(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            kwargs.update(storage_class=storage_class)
            result = func(*args, **kwargs)
            return result

        return wrapped

    return decorated

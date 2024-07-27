from alibabacloud_credentials.client import Client as CredClient
from alibabacloud_ecs20140526.client import Client as EcsClient
from alibabacloud_tea_openapi.models import Config as EcsConfig


def create_client() -> EcsClient:
    credentialsClient = CredClient()
    ecsConfig = EcsConfig(credential=credentialsClient)
    ecsConfig.endpoint = "ecs.cn-beijing.aliyuncs.com"
    ecsClient = EcsClient(ecsConfig)
    return ecsClient

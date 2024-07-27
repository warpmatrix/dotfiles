import time
from loguru import logger as log

from alibabacloud_ecs20140526.client import Client as EcsClient
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_ecs20140526 import models as ecs_models

from aliyun import client
from comm.event import Event
from comm.listener.feishu_bot import FeishuBot
from comm.manager import EventManager

topic: str = "A100 availability"


def query_resource_availability(client: EcsClient, region_id: str):
    describe_available_resource_request = ecs_models.DescribeAvailableResourceRequest(
        region_id=region_id,
        destination_resource="InstanceType",
        instance_type="ecs.gn7e-c16g1.4xlarge",
    )
    runtime = RuntimeOptions()

    try:
        resp = client.describe_available_resource_with_options(
            describe_available_resource_request, runtime
        )
        for available_zone in resp.body.available_zones.available_zone:
            status = (
                available_zone.available_resources.available_resource[0]
                .supported_resources.supported_resource[0]
                .status
            )

            assert isinstance(status, str)
            message = f"check A100 availability in {region_id}: {status}"
            log.info(message)
            if status == "Available":
                event = Event(topic, message)
                EventManager().notify(event)

    except Exception as error:
        print(error.message)
        UtilClient.assert_as_string(error.message)


if __name__ == "__main__":
    feishu_bot = FeishuBot()
    EventManager().subscribe(topic, feishu_bot)
    ecsClient = client.create_client()
    region_id="cn-beijing"
    while True:
        query_resource_availability(ecsClient, region_id)
        time.sleep(10 * 60)

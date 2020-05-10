import boto3
from config.config import get_config_file
from botocore.exceptions import ClientError

VPN_INSTANCE_ID = get_config_file().get("aws_ec2").get("vpn_instance_id")

class AwsService:

    def __init__(self):
        self.__config = get_config_file().get("aws_ec2")
        self.__key = self.__config.get("aws_access_key_id")
        self.__secret = self.__config.get("aws_secret_access_key")
        self.__region = self.__config.get("ec2_region_name")
        self._client = None
    
    def _init_connect(self):
        self._client = boto3.client(
            'ec2',
            region_name=self.__region,
            aws_access_key_id=self.__key,
            aws_secret_access_key=self.__secret
        )
    
    def list_instances(self):
        return self._client.describe_instances(        
            InstanceIds=[
                VPN_INSTANCE_ID
            ]
        )
    def start_instance(self):
        return self._client.start_instances(
            InstanceIds=[
                VPN_INSTANCE_ID
            ]
        )

    def stop_instance(self):
        return self._client.stop_instances(
            InstanceIds=[
                VPN_INSTANCE_ID
            ]
        )
    
    def replace_elastic_address(self):
        allocation_ip = self.__find_allocation_id_from_instance_ip()
        response = self.__release_elastic_address(allocation_ip=allocation_ip)
        if response:
            result = self.__allowcate_elastic_address()
            return result
        return None

    def __find_allocation_id_from_instance_ip(self):
        address = self._client.describe_addresses(Filters=[{
            'Name': 'instance-id',
            'Values': [
                VPN_INSTANCE_ID
            ]
        }])
        return address.get('Addresses')[0].get('AllocationId')
    
    def __allowcate_elastic_address(self):
        try:
            allocation = self._client.allocate_address(Domain='standard')
            response = self._client.associate_address(
                AllocationId=allocation['AllocationId'],
                InstanceId=VPN_INSTANCE_ID
            )
            print(response)
            return response
        except ClientError as e:
            print(e)
            return None
    
    def __release_elastic_address(self, allocation_ip: str):
        try:
            response = self._client.release_address(AllocationId=allocation_ip)
            print('Address released')
            return response
        except ClientError as e:
            print(e)
            return None 


    def assign_elsticId_to_instance(self, elastic_ip: str):
        try:
            response = self._client.associate_address(AllocationId=elastic_ip,
                                            InstanceId=VPN_INSTANCE_ID)
            print(response)
            return response
        except ClientError as e:
            print(e)
            return None

    
    
    def list_instance_status(self):
        return self._client.get_all_instance_status()
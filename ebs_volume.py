"""Data class for EBS volume data."""
class EBSVolume:
    """
    Filters out irrelevant boto3 EBS data. Adds custom/enriches current EC2 data.
    """
    def __init__(self, volume_data:dict):
        self.id = volume_data["VolumeId"]
        self.volume_type = volume_data["VolumeType"]
        self.create_time = volume_data["CreateTime"]
        self.size = volume_data["Size"]
        self.state = volume_data["State"]
        self.instance_id = volume_data["Attachments"][0]["InstanceId"]
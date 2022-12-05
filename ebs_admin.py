import json

import aws_auth
from ebs_volume import EBSVolume

REGIONS = [ "ap-northeast-1", "ap-northeast-2", "ap-northeast-3", "ap-south-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2"]

def write_output_json(resp:dict) -> None:
    """Useful for testing to get raw boto3 output.
    Writes to olympus_output.json in json format."""
    with open("output.json", 'a', encoding="UTF-8") as outfile:
        outfile.write(json.dumps(resp, default=str))

def upgrade_to_gp3(vols:list):
    for i in enumerate(REGIONS, 0):
        client = aws_auth.botosesh.client('ec2', region_name=REGIONS[i[0]])
    for volume in vols:
        if volume.volume_type == "gp2":
            client.modify_volume(
                VolumeId=volume.id,
                VolumeType='gp3'
            )
            print(f"{volume.id} modified to gp3.")
            
def enumerate_volumes(res:dict):
    _raw_response_data = res["Volumes"]
    if _raw_response_data is not None:
        volumes = []
        for i in enumerate(_raw_response_data, 0):
            volumes.append(EBSVolume(_raw_response_data[i[0]]))
    return volumes

def main():
    for i in enumerate(REGIONS, 0):
        response = aws_auth.botosesh.client('ec2', region_name=REGIONS[i[0]])
        if aws_auth.validate_response_code(response):
            write_output_json(response)
    # ebs_volumes = enumerate_volumes(response)
    # upgrade_to_gp3(ebs_volumes)
        
if __name__ == "__main__":
    main()
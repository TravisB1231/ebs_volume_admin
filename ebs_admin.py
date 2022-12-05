import sys
import json

import aws_auth
from ebs_volume import EBSVolume

REGION = "us-east-2"

def write_output_json(resp:dict) -> None:
    """Useful for testing to get raw boto3 output.
    Writes to olympus_output.json in json format."""
    with open("output.json", 'w', encoding="UTF-8") as outfile:
        outfile.write(json.dumps(resp, default=str))

def upgrade_to_gp3(vols:list):
    client = aws_auth.botosesh.client('ec2', region_name=REGION)
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
    response = aws_auth.botosesh.client('ec2', region_name=REGION).describe_volumes()
    if aws_auth.validate_response_code(response):
        write_output_json(response)
        ebs_volumes = enumerate_volumes(response)
        upgrade_to_gp3(ebs_volumes)
        
if __name__ == "__main__":
    main()
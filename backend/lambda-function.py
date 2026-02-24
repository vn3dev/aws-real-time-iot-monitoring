import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
client = boto3.client("iot-data")
table = dynamodb.Table('PrinterProfiles')

def lambda_handler(event, context):
    device_id = event.get("PrinterId").capitalize()
    sensor_value = event["data"]["value"]

    response = table.get_item(Key={"PrinterId": device_id})

    if "Item" in response:
        device_profile = response["Item"]
        print(f"Device profile fetched: {device_profile}")

        lower_threshold = float(device_profile["Thresholds"]["Lower"])
        upper_threshold = float(device_profile["Thresholds"]["Upper"])
        time_window = int(device_profile["Window"])

        print(f"Processing {device_id} with sensor value: {sensor_value}")
        print(f"Current OutOfBoundsCount: {device_profile['OutOfBoundsCount']}")
        print(f"EventCount before processing: {device_profile.get('EventCount', 0)}")

        is_out_of_bounds = sensor_value < lower_threshold or sensor_value > upper_threshold

        if is_out_of_bounds:
            device_profile["OutOfBoundsCount"] = int(device_profile.get("OutOfBoundsCount", 0)) + 1
        else:
            device_profile["OutOfBoundsCount"] = 0

        if device_profile["OutOfBoundsCount"] >= time_window:
            device_profile["EventCount"] = int(device_profile.get("EventCount", 0)) + 1
            device_profile["OutOfBoundsCount"] = 0
            iot_republish(device_id, device_profile)

        response = table.update_item(
            Key={"PrinterId": device_id},
            UpdateExpression="SET OutOfBoundsCount = :oob, EventCount = :ec",
            ExpressionAttributeValues={
                ":oob": device_profile["OutOfBoundsCount"],
                ":ec": device_profile["EventCount"]
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Update response: {response}")

    print("Current device processing complete. Generating output:")
    generate_output()
    
    return {"status": "processed"}

def iot_republish(device_id, new_record):
    event_count = int(new_record["EventCount"])
    payload = json.dumps({"PrinterId": device_id, "events": event_count})
    response = client.publish(topic="anom/pred", qos=1, payload=payload)
    return

def generate_output():
    response = table.scan()
    devices = response.get('Items', [])
    
    sorted_devices = sorted(devices, key=lambda d: int(d['EventCount']), reverse=True)

    output = [(device['PrinterId'], int(device['EventCount'])) for device in sorted_devices]
    
    print("Sorted output (PrinterId, EventCount):")
    for device_id, event_count in output:
        print(f"{device_id}, {event_count}")
    
    return output
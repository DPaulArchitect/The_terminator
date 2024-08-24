import json
import boto3

# List of allowed instance types
ALLOWED_INSTANCE_TYPES = ["t2.micro", "t2.small","t3.micro", "t3.small"]

def lambda_handler(event, context):
    import json
import boto3

# List of allowed instance types
ALLOWED_INSTANCE_TYPES = ["t2.micro", "t2.small", "t3.micro","t3.small"]

def lambda_handler(event, context):
    # Parse the JSON string in the 'invokingEvent' field
    invoking_event = json.loads(event['invokingEvent'])
    
    # Extract configuration item details
    configuration_item = invoking_event.get('configurationItem')
    
    if configuration_item:
        instance_id = configuration_item['resourceId']
        instance_type = configuration_item['configuration'].get('instanceType')

        if instance_type and instance_type not in ALLOWED_INSTANCE_TYPES:
            ec2_client = boto3.client('ec2')
            print(f"Instance {instance_id} of type {instance_type} is not allowed. Terminating...")
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} terminated.")
        else:
            print(f"Instance {instance_id} of type {instance_type} is allowed or instanceType is not defined.")
    else:
        print("No configuration item found in the event.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Operation completed')
    }


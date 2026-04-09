import json
import boto3
import os

# Load config from environment variables
KB_ID = os.environ.get('KB_ID')
MODEL_ID = os.environ.get('MODEL_ID', 'us.amazon.nova-2-lite-v1:0')
BEDROCK_REGION = os.environ.get('BEDROCK_REGION', 'us-east-1')
INFERENCE_PROFILE_ARN = os.environ.get('INFERENCE_PROFILE_ARN', '')

# Create Bedrock client
client = boto3.client('bedrock-agent-runtime', region_name=BEDROCK_REGION)

# Use inference profile ARN if provided, otherwise construct model ARN from region and model ID
if INFERENCE_PROFILE_ARN:
    MODEL_ARN = INFERENCE_PROFILE_ARN
else:
    MODEL_ARN = f"arn:aws:bedrock:{BEDROCK_REGION}::foundation-model/{MODEL_ID}"

retrieve_generate_config = {
    'type': 'KNOWLEDGE_BASE',
    'knowledgeBaseConfiguration': {
        'knowledgeBaseId': KB_ID,
        'modelArn': MODEL_ARN
    }
}


def lambda_handler(event, context):
    try:
        # Validate configuration
        if not KB_ID or not MODEL_ARN:
            return _error_response(400, "Missing KB_ID or MODEL_ARN environment variables")

        # Parse request
        body = json.loads(event.get("body") or "{}")
        prompt = body.get("prompt", "").strip()

        # Validate prompt
        if not prompt:
            return _error_response(400, "Prompt cannot be empty")

        print(f"Processing prompt: {prompt}")

        # Retrieve and generate answer
        response = client.retrieve_and_generate(
            input={
                'text': prompt
            },
            retrieveAndGenerateConfiguration=retrieve_generate_config
        )

        response_body = response["output"]["text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "reply": response_body
            })
        }

    except Exception as e:
        print(f"Lambda error: {str(e)}")
        return _error_response(500, str(e))


def _error_response(status_code, error_message):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "error": error_message
        })
    }

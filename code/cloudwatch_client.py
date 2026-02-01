import os
import time
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

cloudwatch = boto3.client("cloudwatch")

model_id = "BEDROCK_MODEL_ARN"

bedrock = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
)
prompt = "Hello" * 1000

# Measure TTFT with streaming
start_time = time.time()
response = bedrock.invoke_model_with_response_stream(
    modelId=model_id,
    body=json.dumps({"prompt": prompt}),
)

# Time to first chunk = TTFT
ttft = None
full_response = ""

for event in response["body"]:
    if ttft is None:
        ttft = (time.time() - start_time) * 1000  # ms

    chunk = event.get("chunk")
    if chunk:
        chunk_data = json.loads(chunk.get("bytes", b"{}").decode())
        if "generation" in chunk_data:
            full_response += chunk_data["generation"]

print(f"\nPrompt: {prompt}")
print(f"TTFT: {ttft:.2f}ms" if ttft else "TTFT: N/A")
print(f"Response: {full_response}")

# Publish to CloudWatch
# Note: Cannot publish to AWS/Bedrock (AWS-managed namespace)
# Use a custom namespace that will appear near Bedrock in the console
cloudwatch.put_metric_data(
    Namespace="Bedrock/Custom",
    MetricData=[
        {
            "MetricName": "TTFT",
            "Value": ttft,
            "Unit": "Milliseconds",
            "Dimensions": [{"Name": "ModelId", "Value": model_id}],
        }
    ],
)

def handler(event, context):
    """Simple Netlify Function health check (bypasses Flask)."""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status":"ok","source":"netlify-function"}'
    }

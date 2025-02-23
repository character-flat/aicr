from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
import hmac, hashlib

GITHUB_SECRET = 'randomkey'
app = FastAPI()

@app.get("/")
def base_route():
    #HTML content
    content = """
    <html>
        <head>
            <title>FastAPI</title>
        </head>
        <body>
            <h1>Welcome to FastAPI</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content)
    
# Health check endpoint
@app.get("/ping")
def ping():
    return JSONResponse(content={"message": "pong"})

#setting up webhook listener
@app.api_route("/webhook", methods=["GET", "POST"])
async def github_webhook(request: Request, x_github_event: str = Header(None), x_hub_signature_256: str = Header(None)):
    if request.method == "GET":
        return JSONResponse(content={"message": "Webhook GET route is live"})

    body = await request.body()

    # Validate signature
    if not is_valid_signature(body, x_hub_signature_256, GITHUB_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    payload = await request.json()
    print(f"Received event: {x_github_event}")
    print(payload)

    return JSONResponse(content={"message": f"Received {x_github_event} event"})


def is_valid_signature(payload_body, signature_header, secret):
    if signature_header is None or secret is None:
        return False

    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(secret.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature)
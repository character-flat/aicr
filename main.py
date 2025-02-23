from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

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
async def github_webhook(request: Request):
    if request.method == "GET":
        return JSONResponse(content={"message": "Webhook GET route is live"})

    if request.method == "POST":
        payload = await request.json()
        event = request.headers.get('X-GitHub-Event')
        print(f"Received event: {event}")
        print(payload)
        return JSONResponse(content={"message": "Webhook received"})

#another branch
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Strict CORS Policy Middleware
# This ensures only the allowed origin gets the Access-Control-Allow-Origin header.
# Preflights from unlisted origins will naturally be rejected (no ACAO header).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-5eqayn.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# 2. Custom Headers Middleware (X-Request-ID and X-Process-Time)
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    # Start timer and generate unique ID
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())

    # Process the request
    response = await call_next(request)

    # Calculate duration
    process_time = time.perf_counter() - start_time
    
    # Append required headers to every response
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

    return response

# 3. The Stats Endpoint
@app.get("/stats")
def calculate_stats(values: str):
    # Parse the comma-separated integers
    nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    
    if not nums:
        return {"error": "No values provided"}

    # Compute statistics
    count_val = len(nums)
    sum_val = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = sum_val / count_val

    # Return the exact JSON structure required
    return {
        "email": "24f2005537@ds.study.iitm.ac.in",
        "count": count_val,
        "sum": sum_val,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }

import httpx

async def log(stack: str, level: str, package: str, message: str):
    log_data = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post("http://your-test-server/log", json=log_data)
        except Exception as e:
            # Local fallback if the test server is unreachable
            print(f"Logging failed: {e}")

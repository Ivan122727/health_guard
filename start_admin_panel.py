import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "shared.sqladmin_.asgi:app",
        host="0.0.0.0", 
        port=5665,
        reload=True
    )
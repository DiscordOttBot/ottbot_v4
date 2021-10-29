from fastapi import FastAPI
import uvicorn

app: FastAPI = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

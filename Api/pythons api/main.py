from fastapi import FastAPI

app = FastAPI(title="Python API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health")
def health():
    return {"status": "ok"}

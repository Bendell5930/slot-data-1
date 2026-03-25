from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/machines")
def machines():
    return [
        {"name":"Dragon Link #24","heat":80},
        {"name":"Lightning Link #11","heat":55},
        {"name":"Buffalo Gold #6","heat":20}
    ]

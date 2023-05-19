from fastapi import FastAPI
from router import product

app = FastAPI()
app.include_router(router=product.router)


if __name__ == "__main__":
    import uvicorn
    print("\n*** JALAN BOY***")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True)

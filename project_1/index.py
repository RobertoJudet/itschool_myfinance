# this is our root file, when we execute this we will start our app
# webpage for fastapi framework https://fastapi.tiangolo.com/tutorial/,
# also https://realpython.com/fastapi-python-web-apis/

# uvicorn index:app --reload --port 7777
# uvicorn is the server which will start
# index:app, index -> the file name, app -> the FastAPI object name
# --reload -> the server will restart when we modify the code
# --port <port_number> -> select on which port to start


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from stock_factory import StockFactory
from stock_repo import StockRepository
from models import StockModel
from exceptions import StockNotFound

app = FastAPI(
    title="Name of our app",  # TODO for homework, name your application
    # <major_version>.<minor_version>.<patch_version>
    version="0.2.0",  # increase version after finishing homework
    description="",  # TODO add a description
)


@app.get(
    "/health",
    summary="This will be visible at start",
    description="We can describe this API call",
    response_description="We can describe the response",
)
def health() -> dict:
    return {
        "status": "online",
        "engine": "on",
    }


stock_repo = StockRepository()


@app.post("/stocks")
def add_new_stock(stock_info: StockModel):
    new_stock = StockFactory().make_from_model(stock_info)
    stock_repo.add(new_stock)


# example if you want to do a tasks app return the list of tasks, and rename the url /items -> /tasks
@app.get("/stocks", response_model=list[StockModel])
def get_stocks(field: str = None):
    return stock_repo.get_all()


#TODO create a get for a single stock, we give the ticker and receive more information
# additional information: long summary, on which exchange it is, country, number of employees, industry

# we can put an id in the URL to select only one resource
@app.get("/stocks/{ticker_id}", response_model=StockModel)
def get_one_stock(ticker_id: str):
    return stock_repo.get_by_ticker(ticker_id)



# TODO add a put method to edit your domain item


@app.delete("/stocks")
def remove_stock(ticker: str):
    stock_repo.remove(ticker)


@app.on_event("startup")
def load_list_of_items():
    stock_repo.load()


@app.exception_handler(StockNotFound)
def handle_stock_not_found(exception, request):
    return JSONResponse(content="The stock you requested was not saved in our app!", status_code=404)

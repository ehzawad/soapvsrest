from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from lxml import etree

app = FastAPI()

# Data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Shared in-memory database
items = []

# Function to populate initial data
def populate_initial_data():
    global items
    items = [
        Item(id=1, name="Laptop", description="A powerful computing device"),
        Item(id=2, name="Smartphone", description="A portable communication device"),
        Item(id=3, name="Headphones", description="Audio listening equipment")
    ]

# Helper functions for CRUD operations
def create_item(item: Item):
    if any(i.id == item.id for i in items):
        raise ValueError("Item with this ID already exists")
    items.append(item)
    return item

def get_items():
    return items

def get_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise ValueError("Item not found")
    return item

def update_item(item_id: int, updated_item: Item):
    index = next((index for index, i in enumerate(items) if i.id == item_id), None)
    if index is None:
        raise ValueError("Item not found")
    items[index] = updated_item
    return updated_item

def delete_item(item_id: int):
    global items
    original_length = len(items)
    items = [item for item in items if item.id != item_id]
    if len(items) == original_length:
        raise ValueError("Item not found")

def delete_all_items():
    global items
    items.clear()

# REST API endpoints
@app.post("/rest/items", response_model=Item)
async def rest_create_item(item: Item):
    try:
        return create_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rest/items", response_model=List[Item])
async def rest_read_items():
    return get_items()

@app.get("/rest/items/{item_id}", response_model=Item)
async def rest_read_item(item_id: int):
    try:
        return get_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/rest/items/{item_id}", response_model=Item)
async def rest_update_item(item_id: int, item: Item):
    try:
        return update_item(item_id, item)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/rest/items/{item_id}")
async def rest_delete_item(item_id: int):
    try:
        delete_item(item_id)
        return {"message": "Item deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/rest/items")
async def rest_delete_all_items():
    delete_all_items()
    return {"message": "All items deleted"}

# SOAP API endpoint
@app.post("/soap")
async def soap_endpoint(body: str = Body(...)):
    try:
        root = etree.fromstring(body)
        soap_body = root.find(".//{http://schemas.xmlsoap.org/soap/envelope/}Body")
        operation = soap_body[0].tag.split("}")[-1]

        response_body = ""
        
        if operation == "CreateItem":
            item = Item(
                id=int(soap_body[0].find("id").text),
                name=soap_body[0].find("name").text,
                description=soap_body[0].find("description").text
            )
            try:
                created_item = create_item(item)
                response_body = f"<CreateItemResponse><item><id>{created_item.id}</id><name>{created_item.name}</name><description>{created_item.description}</description></item></CreateItemResponse>"
            except ValueError as e:
                response_body = f"<CreateItemResponse><error>{str(e)}</error></CreateItemResponse>"
        
        elif operation == "GetItems":
            items = get_items()
            items_xml = "".join([f"<item><id>{item.id}</id><name>{item.name}</name><description>{item.description}</description></item>" for item in items])
            response_body = f"<GetItemsResponse>{items_xml}</GetItemsResponse>"
        
        elif operation == "GetItem":
            item_id = int(soap_body[0].find("id").text)
            try:
                item = get_item(item_id)
                response_body = f"<GetItemResponse><item><id>{item.id}</id><name>{item.name}</name><description>{item.description}</description></item></GetItemResponse>"
            except ValueError as e:
                response_body = f"<GetItemResponse><error>{str(e)}</error></GetItemResponse>"
        
        elif operation == "UpdateItem":
            item_id = int(soap_body[0].find("id").text)
            updated_item = Item(
                id=item_id,
                name=soap_body[0].find("name").text,
                description=soap_body[0].find("description").text
            )
            try:
                item = update_item(item_id, updated_item)
                response_body = f"<UpdateItemResponse><item><id>{item.id}</id><name>{item.name}</name><description>{item.description}</description></item></UpdateItemResponse>"
            except ValueError as e:
                response_body = f"<UpdateItemResponse><error>{str(e)}</error></UpdateItemResponse>"
        
        elif operation == "DeleteItem":
            item_id = int(soap_body[0].find("id").text)
            try:
                delete_item(item_id)
                response_body = "<DeleteItemResponse><message>Item deleted</message></DeleteItemResponse>"
            except ValueError as e:
                response_body = f"<DeleteItemResponse><error>{str(e)}</error></DeleteItemResponse>"
        
        elif operation == "DeleteAllItems":
            delete_all_items()
            response_body = "<DeleteAllItemsResponse><message>All items deleted</message></DeleteAllItemsResponse>"
        
        else:
            response_body = "<ErrorResponse>Unknown operation</ErrorResponse>"

        soap_response = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                {response_body}
            </soap:Body>
        </soap:Envelope>
        """
        
        return soap_response
    except Exception as e:
        return f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ErrorResponse>{str(e)}</ErrorResponse>
            </soap:Body>
        </soap:Envelope>
        """

@app.on_event("startup")
async def startup_event():
    populate_initial_data()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

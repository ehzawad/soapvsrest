# soapvsrest

REST API Commands:

1. Create an item:
```
curl -X POST -H "Content-Type: application/json" -d '{"id": 4, "name": "Tablet", "description": "A portable touchscreen device"}' http://localhost:8000/rest/items
```

2. Get all items:
```
curl http://localhost:8000/rest/items
```

3. Get a specific item:
```
curl http://localhost:8000/rest/items/1
```

4. Update an item:
```
curl -X PUT -H "Content-Type: application/json" -d '{"id": 1, "name": "Updated Laptop", "description": "An updated powerful computing device"}' http://localhost:8000/rest/items/1
```

5. Delete a specific item:
```
curl -X DELETE http://localhost:8000/rest/items/2
```

6. Delete all items:
```
curl -X DELETE http://localhost:8000/rest/items
```

SOAP API Commands:

1. Create an item:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><CreateItem><id>5</id><name>Smartwatch</name><description>A wearable smart device</description></CreateItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

2. Get all items:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetItems></GetItems></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

3. Get a specific item:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetItem><id>1</id></GetItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

4. Update an item:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><UpdateItem><id>1</id><name>Updated Laptop</name><description>An updated powerful computing device</description></UpdateItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

5. Delete a specific item:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><DeleteItem><id>3</id></DeleteItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

6. Delete all items:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><DeleteAllItems></DeleteAllItems></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

Additional commands to test the synchronization between REST and SOAP:

1. Add an item with REST, then retrieve it with SOAP:
```
curl -X POST -H "Content-Type: application/json" -d '{"id": 6, "name": "E-reader", "description": "A digital reading device"}' http://localhost:8000/rest/items

curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetItem><id>6</id></GetItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

2. Update an item with SOAP, then retrieve it with REST:
```
curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><UpdateItem><id>1</id><name>Super Laptop</name><description>An extremely powerful computing device</description></UpdateItem></soap:Body></soap:Envelope>' http://localhost:8000/soap

curl http://localhost:8000/rest/items/1
```

3. Delete an item with REST, then try to retrieve it with SOAP:
```
curl -X DELETE http://localhost:8000/rest/items/2

curl -X POST -H "Content-Type: text/xml" -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetItem><id>2</id></GetItem></soap:Body></soap:Envelope>' http://localhost:8000/soap
```

These commands cover all the CRUD operations for both REST and SOAP APIs. You can use them to test the functionality and verify that both APIs are working on the same shared data store. Remember to replace `http://localhost:8000` with the appropriate URL if your server is running on a different host or port.

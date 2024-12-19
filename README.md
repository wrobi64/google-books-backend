# Setup
Make sure python is installed and setup on your machine

Run:
```
pip3 install -t lib -r requirements.txt
```
or
```
pip install -t lib -r requirements.txt
```

This will install the required python libraries to run this service.

# Run locally
Run:
```
uvicorn main:app --reload
```
The app is now set up to run from http://127.0.0.1:8000

To call the search endpoint simply use http://127.0.0.1:8000/search?q=search+term

To view documation on the endpoint and test with an interface open http://127.0.0.1:8000/docs#/

# Deploying to AWS Lambda
Create a zip file where the app and dependencies are in the same closure.
```
(cd lib; zip ../lambda_function.zip -r .)
```
Add our main file
```
zip lambda_function.zip -u main.py
```

# Lambda URL
https://5vmvwhyxt6eudjhcnjofft3hkm0jervh.lambda-url.us-east-1.on.aws/
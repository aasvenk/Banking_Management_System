# Banking_System


## Development setup

## Install postgres

```
brew install postgres@15
```

### Activate python environment

```
# Create enviroment (make sure to be in the correct path) 
python -m venv venv
# Activate environment
source ./venv/bin/activate
# Deactivate
deactivate
```

### Install (Activate venv and do below command) 
```
pip install -r requirements.txt
```


### You can generate the secret keys using below code

```
python -c 'import secrets; print(secrets.token_hex())'
```


### Run the FastAPi server with below command : 
```
uvicorn main:app --reload
```

### Swagger 
```
http://127.0.0.1:8000/docs

```


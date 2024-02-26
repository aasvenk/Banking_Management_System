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

### Create a .env file in backend Parent folder in similar format. 
### Update the SECRET_KEY,POSTGRES_USER,POSTGRES_PW,POSTGRES_URL(Fill details in the placeholders in brackets and remove the square brackets),PORT
```
SECRET_KEY=''
POSTGRES_USER='' 
POSTGRES_PW=""
POSTGRES_URL="postgresql://[POSTGRES_USER]:[POSTGRES_PW]@127.0.0.1:[PORT]/banking_system"
POSTGRES_DB="banking_system"
HOST = "127.0.0.1"
PORT = "5433" 
# JWT_SECRET_KEY=
# CROSS_ORIGIN_URL= 
# GOOGLE_CLIENT_ID=
BACKEND_URL="127.0.0.1:8000"
# FRONTEND_URL=
# MAIL_SERVER=
# MAIL_PORT=
# MAIL_USERNAME=
# MAIL_PASSWORD=
```
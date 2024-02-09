# Banking_System


## Development setup

## Install postgres

```
brew install postgres@15
```

### Activate python environment

```
# Create enviroment
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

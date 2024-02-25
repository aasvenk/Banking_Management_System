from passlib.context import CryptContext

#defining a context that handles hashing
passwordContext= CryptContext(schemes=["bcrypt"],deprecated="auto")


#Using the context to hash the password and return the hashed pwd.
def getHashPassword(password):
    return passwordContext.hash(password)
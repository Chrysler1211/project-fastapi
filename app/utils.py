from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash(password: str):

    return password_hash.hash(password)

def verify(plain_passoword: str, hashed_password: str):

    return password_hash.verify(plain_passoword, hashed_password)

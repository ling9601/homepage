from cryptography.fernet import Fernet

key = b'NOwSWR-3SMiZV0G1IJ9ghoQkCvfZomVjH9Q4m3IwwHc='
f =Fernet(key)

def Code2Token(code):
    return f.encrypt(str.encode(code))
import random
import string

DB_URL = "champsifbb.db"

key = ''.join(random.choice(string.ascii_letters+string.ascii_uppercase+string.digits) for i in range(12))
SECRET_KEY = key
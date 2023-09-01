from pymongo import MongoClient
from urllib.parse import quote_plus

username = "Camaro"
password = "WdMzaNfNtAXSVEH5"

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.n3xhgkp.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("¡Ping exitoso! Te has conectado correctamente a MongoDB.")
except Exception as e:
    print(e)


# Crea una instancia del cliente de MongoDB y conecta al servidor
client = MongoClient(uri)

# Verifica la conexión imprimiendo el número de bases de datos disponibles
database_names = client.list_database_names()
print("Bases de datos disponibles:")
for db_name in database_names:
    print("- " + db_name)
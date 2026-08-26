''' 
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

url = "https://kv-groupmasterminds.vault.azure.net/"
client = SecretClient(vault_url=url, credential=DefaultAzureCredential())

for name in ["postgres-host", "postgres-database", "postgres-user", "postgres-port"]:
    print(name, "=", client.get_secret(name).value)

print("password length =", len(client.get_secret("postgres-password").value))

'''

from time_app import get_database_credentials
host, db, user, pw, port = get_database_credentials()
print(host, db, user, port, "pwlen=", len(pw))
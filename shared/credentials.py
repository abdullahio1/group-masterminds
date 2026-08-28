from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import logging
from functools import lru_cache


# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Azure Key Vault configuration
KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL", "https://kv-groupmasterminds.vault.azure.net/")



@lru_cache(maxsize=1)
def get_database_credentials():
    """Get database credentials from Azure Key Vault or environment variables"""
    try:
        # Try to get credentials from Azure Key Vault first
        if KEY_VAULT_URL:
            logger.info("Attempting to get credentials from Azure Key Vault...")
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

            # Get secrets from Key Vault
            host = secret_client.get_secret("postgres-host").value
            database = secret_client.get_secret("postgres-database").value
            user = secret_client.get_secret("postgres-user").value
            password = secret_client.get_secret("postgres-password").value
            port = secret_client.get_secret("postgres-port").value

            logger.info(f"Successfully retrieved credentials from Azure Key Vault")
            logger.info(
                f"Connecting to: host={host}, database={database}, user={user}, port={port}"
            )
            logger.debug(
                f"Password length: {len(password)} characters"
            )  # Don't log actual password

            return host, database, user, password, port

    except Exception as e:
        logger.warning(f"Could not get credentials from Key Vault: {e}")


@lru_cache(maxsize=1)
def get_storage_credentials():
    """Get storage credentials from Azure Key Vault or environment variables"""
    storage_connection_string = ""
    try:
        # Try to get credentials from Azure Key Vault first
        if KEY_VAULT_URL:
            logger.info("Attempting to get credentials from Azure Key Vault...")
            credential = DefaultAzureCredential()
            secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

            storage_connection_string = secret_client.get_secret(
                "storage-connection-string"
            ).value

            logger.info("Successfully retrieved credentials from Azure Key Vault")
            logger.debug("Connecting to: storage_connection_string")

    except Exception as e:
        logger.warning(f"Could not get credentials from Key Vault: {e}")
    return storage_connection_string

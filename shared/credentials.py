from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import logging



#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Azure Key Vault configuration
KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL", "https://kv-groupmasterminds.vault.azure.net/")


def get_database_credentials():
    """Get database credentials from Azure Key Vault or environment variables"""
    try:
        # Try to get credentials from Azure Key Vault first
        if KEY_VAULT_URL and KEY_VAULT_URL != "https://kv-groupmasterminds.vault.azure.net/":
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
            logger.info(f"Connecting to: host={host}, database={database}, user={user}, port={port}")
            logger.debug(f"Password length: {len(password)} characters")  # Don't log actual password
            return host, database, user, password, port
            
    except Exception as e:
        logger.warning(f"Could not get credentials from Key Vault: {e}")
        logger.info("Falling back to environment variables...")
    
    # Fallback to environment variables
    host = os.getenv("POSTGRES_HOST", "localhost")
    database = os.getenv("POSTGRES_DB", "timemanagement")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    port = os.getenv("POSTGRES_PORT", "5432")
    
    logger.info("Using credentials from environment variables")
    logger.info(f"Connecting to: host={host}, database={database}, user={user}, port={port}")
    logger.debug(f"Password length: {len(password)} characters")  # Don't log actual password
    return host, database, user, password, port
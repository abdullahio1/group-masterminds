#!/usr/bin/env bash
# =====================================================================
# Azure setup for the Consultant Time-management POC (group-masterminds)
# Run these one section at a time. Each line is a single command.
#
# Resources created (all in one resource group, one region):
#   - Resource group
#   - Storage account + blob container ("reports")
#   - PostgreSQL Flexible Server + database ("timemanagement")
#   - Key Vault + 5 secrets (DB connection details)
# =====================================================================


# ---------------------------------------------------------------------
# Shared values (edit if you want different names)
# Names marked GLOBALLY UNIQUE must be unique across all of Azure.
# ---------------------------------------------------------------------
#   Region        : northeurope
#   Resource group: groupmasterminds-rg
#   Storage       : stgroupmasterminds        (GLOBALLY UNIQUE, lowercase+digits, 3-24)
#   Container     : reports
#   PostgreSQL     : psql-groupmasterminds     (GLOBALLY UNIQUE)
#   DB name       : timemanagement
#   DB admin user : pgadmin
#   Key Vault     : kv-groupmasterminds        (GLOBALLY UNIQUE)


# =====================================================================
# 0. LOG IN
# =====================================================================
az login
# Press Enter to accept your default subscription (SkillioLearners).
az account show --output table


# =====================================================================
# 1. RESOURCE GROUP  (the container for everything else)
# =====================================================================
az group create --name groupmasterminds-rg --location northeurope --output table


# =====================================================================
# 2. STORAGE ACCOUNT + BLOB CONTAINER
# =====================================================================
az storage account create --resource-group groupmasterminds-rg --name stgroupmasterminds --location northeurope --sku Standard_LRS --kind StorageV2 --output table

# Grab an account key, then create the "reports" container with it.
# (On Windows CMD, run the keys list command, copy the key, and paste it
#  in place of <KEY> below. In Git Bash you can use the $(...) version.)
az storage account keys list -g groupmasterminds-rg -n stgroupmasterminds --query "[0].value" --output tsv

az storage container create --name reports --account-name stgroupmasterminds --account-key "<KEY>" --output table


# =====================================================================
# 3. POSTGRESQL FLEXIBLE SERVER + DATABASE
# =====================================================================
# Note: --database-name is NOT allowed here on current CLI, so the
# server and the database are created in two separate commands.
# When prompted "enable access to client IP (y/n)" -> answer y.
az postgres flexible-server create --resource-group groupmasterminds-rg --name psql-groupmasterminds --location northeurope --admin-user pgadmin --admin-password "password" 
--tier Burstable --sku-name Standard_B1ms --storage-size 32 --version 16

# Create the database inside the server (flag is --name / -n, not --database-name)
az postgres flexible-server db create --resource-group groupmasterminds-rg --server-name psql-groupmasterminds --name timemanagement

# (Optional) verify the database exists
az postgres flexible-server db list --resource-group groupmasterminds-rg --server-name psql-groupmasterminds --output table


# =====================================================================
# 4. KEY VAULT
# =====================================================================
az keyvault create --name kv-groupmasterminds --resource-group groupmasterminds-rg --location northeurope --output table

# NOTE ON PERMISSIONS:
# A student/Contributor account CANNOT assign itself the secrets role.
# The teacher (an Owner) granted the "Key Vault Secrets Officer" role
# on kv-groupmasterminds. If you ever hit an "InsufficientPermissions"
# or "AuthorizationFailed" error here, ask an Owner to grant that role.
# (RBAC assignments can take ~60s to take effect.)


# =====================================================================
# 5. STORE THE 5 SECRETS  (names must match the app exactly)
# =====================================================================
az keyvault secret set --vault-name kv-groupmasterminds --name postgres-host --value "psql-groupmasterminds.postgres.database.azure.com"
az keyvault secret set --vault-name kv-groupmasterminds --name postgres-database --value "timemanagement"
az keyvault secret set --vault-name kv-groupmasterminds --name postgres-user --value "pgadmin"
az keyvault secret set --vault-name kv-groupmasterminds --name postgres-password --value "Sommar1717!!12"
az keyvault secret set --vault-name kv-groupmasterminds --name postgres-port --value "5432"

# (Optional) read one back to confirm
az keyvault secret show --vault-name kv-groupmasterminds --name postgres-password --query value -o tsv


# =====================================================================
# 6. TEST THE DATABASE CONNECTION  (needs psql installed)
# =====================================================================
psql "host=psql-groupmasterminds.postgres.database.azure.com port=5432 dbname=timemanagement user=pgadmin sslmode=require"


# =====================================================================
# USEFUL LATER
# =====================================================================
# Stop the DB between work sessions (saves cost):
#   az postgres flexible-server stop  -g groupmasterminds-rg -n psql-groupmasterminds
# Start it again:
#   az postgres flexible-server start -g groupmasterminds-rg -n psql-groupmasterminds
# Reset the DB password (then update the postgres-password secret to match):
#   az postgres flexible-server update -g groupmasterminds-rg -n psql-groupmasterminds --admin-password "<new>"
# Delete EVERYTHING when the project is graded:
#   az group delete --name groupmasterminds-rg --yes --no-wait
from azure.storage.blob import BlobServiceClient


def upload_report_blob(connection_string: str, filename: str, blob_path: str) -> None:
    service = BlobServiceClient.from_connection_string(connection_string)

    container = service.get_container_client("data")

    # Check if container exists; create it only if it doesn't
    try:
        if not container.exists():
            container.create_container()
            print("Container 'data' created successfully.")
        else:
            print("Container 'data' already exists. Skipping creation.")
    except Exception as e:
        print(f"Warning: Could not verify or create container: {e}")

    # Upload the file
    try:
        with open(filename, "rb") as f:
            container.upload_blob(
                name=f"exports/{blob_path}/{filename}", data=f, overwrite=True
            )
        print(f"Successfully uploaded {filename} to Azure Storage.")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Cannot upload {filename}: File does not exist locally."
        )
    except Exception as e:
        raise RuntimeError(f"Failed to upload blob to Azure: {e}")

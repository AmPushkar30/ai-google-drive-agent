from services.drive_service import get_drive_service


def search_drive(query):

    service = get_drive_service()

    try:

        results = service.files().list(
            q=query,
            pageSize=20,
            fields="files(id,name,mimeType,modifiedTime,webViewLink)"
        ).execute()

        return results.get("files", [])

    except Exception as e:
        return {"error": str(e)}
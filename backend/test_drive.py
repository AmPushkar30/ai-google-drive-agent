from services.drive_service import get_drive_service

service = get_drive_service()

results = service.files().list(
    pageSize=10,
    fields="files(id, name, mimeType)"
).execute()

files = results.get('files', [])

for file in files:
    print(file)
from tools.drive_search import search_drive

query = "trashed=false"

files = search_drive(query)

print(files)

if isinstance(files, dict) and "error" in files:
    print("ERROR:")
    print(files["error"])

else:

    print("Total Files:", len(files))

    for file in files:

        print("Name:", file["name"])
        print("Type:", file["mimeType"])
        print("Modified:", file["modifiedTime"])
        print("Link:", file["webViewLink"])
        print("-" * 50)
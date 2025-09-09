from zipfile import ZipFile
import os

def zip_project():
    filename = "alex_notify_bot_v19_payload.zip"
    with ZipFile(filename, "w") as zipf:
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith(".py") or file.endswith(".txt"):
                    zipf.write(os.path.join(root, file))
    return filename
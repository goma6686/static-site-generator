import os
import shutil


def copy_files():
    destination = './public'
    source = './static'
    #check if destination folder exists
    if not os.path.exists(destination):
        print("Creating destination folder")
        os.makedirs(destination)
        print(f"{destination} folder created")
    else:
        #clear destination folder
        print("Clearing destination folder")
        for file in os.listdir(destination):
            file_path = os.path.join(destination, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print(f"{destination} folder cleared")

    print(f"Copying from {source} to {destination}...")
    #copy all files and subdirectories, nested files, etc.
    list_of_files = os.listdir(source)
    for file in list_of_files:
        #construct full path
        source_path = os.path.join(source, file)
        destination_path = os.path.join(destination, file)
        print(f"Copying {source_path} to {destination_path}")
        #copy
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
    print("Done!")
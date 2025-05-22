from file_system import MiniFileSystem

fs = MiniFileSystem()

while True:
    print(f"\n Current Directory: {fs.get_current_path()}")
    print("=== Mini File System Emulator ===")
    print("1. Create File")
    print("2. Write File")
    print("3. Read File")
    print("4. Delete File")
    print("5. Truncate File")
    print("6. List Files")
    print("7. Show Disk Status")
    print("8. Show File Metadata")
    print("9. Save File System")
    print("10. Load File System")
    print("11. Make Directory")
    print("12. Change Directory")
    print("13. List Directory")
    print("0. Exit")
    choice = input("Choose: ")

    # Inputan Menu
    # Manipulasi File
    if choice == '1':
        fname = input("File name: ")
        print(fs.create(fname))
    elif choice == '2':
        print("Available files:", fs.list_files_only())
        fname = input("File name: ")
        data = input("Data: ")
        print(fs.write(fname, data))
    elif choice == '3':
        print("Available files:", fs.list_files_only())
        fname = input("File name: ")
        print("Content:", fs.read(fname))
    elif choice == '4':
        print("Available files:", fs.list_files_only())
        fname = input("File name: ")
        print(fs.delete(fname))
    elif choice == '5':
        print("Available files:", fs.list_files_only())
        fname = input("File name: ")
        print(fs.truncate(fname))
        
# Information File
    elif choice == '6':
        print(fs.ls())
    elif choice == '7':
        fs.show_disk()
    elif choice == '8':
        print("Available files:", fs.list_files_only())
        fname = input("File name: ")
        print(fs.show_metadata(fname))

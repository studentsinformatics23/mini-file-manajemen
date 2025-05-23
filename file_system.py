import datetime
import json
import os

class MiniFileSystem:
    def __init__(self, total_blocks=100):
        self.disk = [None] * total_blocks
        self.fs = {
            'name' : '/',
            'type' : 'dir',
            'children' : {}
        }

        self.current_dir = self.fs

    def get_current_path(self):
        path = []

        def find_path(node, target, curr_path):
            if node == target:
                path.extend(curr_path)
                return True
            if node['type'] == 'dir':
                for name, child in node['children'].items():
                    if find_path(child, target, curr_path + [name]):
                        return True
            return False

        find_path(self.fs, self.current_dir, ['/'])  # root path starts with /
        return '/' if len(path) == 1 else '/'.join(path)

    
    def mkdir(self, dirname):
        if dirname in self.current_dir['children']:
            return "Directory already exists."
        self.current_dir['children'][dirname] = {
            'name': dirname,
            'type': 'dir',
            'children': {}
        }
        return f"Directory '{dirname}' created."
    
    def cd(self, dirname):
        if dirname == "..":
            # Naik ke atas (jika bukan root)
            if self.current_dir == self.fs:
                return "Already at root directory."
            path = self._find_parent(self.fs, self.current_dir)
            if path:
                self.current_dir = path
                return "Moved up to parent directory."
            else:
                return "Parent not found."
        elif dirname in self.current_dir['children']:
            target = self.current_dir['children'][dirname]
            if target['type'] == 'dir':
                self.current_dir = target
                return f"Entered directory '{dirname}'."
            else:
                return f"'{dirname}' is not a directory."
        else:
            return "Directory not found."
  
# Manipulasi File
    def create(self, filename):
        if filename in self.current_dir['children']:
            return "File already exists."
        self.current_dir['children'][filename] = {
            'name': filename,
            'type': 'file',
            'start_block': None,
            'size': 0,
            'timestamp': datetime.datetime.now().isoformat(),
            'content': ''
        }
        return f"File '{filename}' created."

    def write(self, filename, data):
        if filename not in self.current_dir['children']:
            return "File not found."
        file = self.current_dir['children'][filename]
        if file['type'] != 'file':
            return f"'{filename}' is not a file."

        needed = len(data) // 10 + 1
        free_blocks = [i for i, blk in enumerate(self.disk) if blk is None]
        if len(free_blocks) < needed:
            return "Not enough space on disk."

        for i in range(needed):
            chunk = data[i*10:(i+1)*10]
            self.disk[free_blocks[i]] = chunk

        file['start_block'] = free_blocks[0]
        file['size'] = needed
        file['content'] = data
        file['timestamp'] = datetime.datetime.now().isoformat()
        return f"Data written to '{filename}'."

    def read(self, filename):
        if filename not in self.current_dir['children']:
            return "File not found."
        file = self.current_dir['children'][filename]
        if file['type'] != 'file':
            return f"'{filename}' is not a file."
        return file['content']

    def delete(self, filename):
        if filename not in self.current_dir['children']:
            return "File not found."
        file = self.current_dir['children'][filename]
        if file['type'] != 'file':
            return f"'{filename}' is not a file."

        # Bebaskan blok
        content = file['content']
        needed = len(content) // 10 + 1
        start = file['start_block']
        if start is not None:
            for i in range(start, start + needed):
                if i < len(self.disk):
                    self.disk[i] = None

        del self.current_dir['children'][filename]
        return f"File '{filename}' deleted."

    def list_files(self):
        if not self.current_dir['children']:
            return "No files or directories."
        
        output = []
        for name, item in self.current_dir['children'].items():
            icon = "[DIR]" if item['type'] == 'dir' else "[FILE]"
            output.append(f"{icon} {name}")
        return "\n".join(output)
    
    def list_files_only(self):
        files = [
            name for name, item in self.current_dir['children'].items()
            if item['type'] == 'file'
        ]
        if not files:
            return "No files available."
        return ", ".join(files)
    
    def truncate(self, filename):
        if filename not in self.current_dir['children']:
            return "File not found."
        file = self.current_dir['children'][filename]
        if file['type'] != 'file':
            return f"'{filename}' is not a file."

        content = file['content']
        needed = len(content) // 10 + 1
        start = file['start_block']

        if start is not None:
            for i in range(start, start + needed):
                if i < len(self.disk):
                    self.disk[i] = None
                    
            file['start_block'] = None
            file['size'] = 0
            file['content'] = ''
            file['timestamp'] = datetime.datetime.now().isoformat()
            return f"File '{filename}' truncated."
        
    def show_disk(self):
            print("\nDisk Status (X = used, . = free):")
            for i in range(0, len(self.disk), 10):
                line = self.disk[i:i+10]
                print(''.join(['X' if blk else '.' for blk in line]))

    def show_metadata(self, filename):
        if filename not in self.current_dir['children']:
            return "File not found."
        file = self.current_dir['children'][filename]
        if file['type'] != 'file':
            return f"'{filename}' is not a file."

        return (
                f"\nMetadata for '{filename}':\n"
                f"  Start Block : {file.get('start_block')}\n"
                f"  Size        : {file.get('size')} block(s)\n"
                f"  Timestamp   : {file.get('timestamp')}\n"
                f"  Content     : '{file.get('content')}'"
        )

    def ls(self):
        if not self.current_dir['children']:
            return "Directory is empty."
        listing = []
        for name, item in self.current_dir['children'].items():
            icon = "[DIR]" if item['type'] == 'dir' else "[FILE]"
            listing.append(f"{icon} {name}")
        return "\n".join(listing)
    
    def _find_parent(self, current, target):
        for name, child in current['children'].items():
            if child == target:
                return current
            if child['type'] == 'dir':
                found = self._find_parent(child, target)
                if found:
                    return found
                return None
            
# Save and Load File System
    def save_to_file(self, path='data/fs_dump.json'):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = {
            'fs': self.fs,
            'disk': self.disk,
            'current_path': self.get_current_path()
        }

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

        return f"File system saved to '{path}'."

    def load_from_file(self, path='data/fs_dump.json'):
        if not os.path.exists(path):
            return "No saved file system found."

        with open(path, 'r') as f:
            data = json.load(f)
            self.fs = data['fs']
            self.disk = data['disk']
            # Pulihkan current_dir dari path
            self.current_dir = self._get_dir_by_path(data.get('current_path', '/'))

        return f"File system loaded from '{path}'."
    
    def list_files_only(self):
        files = [
            name for name, item in self.current_dir['children'].items()
            if item['type'] == 'file'
        ]
        if not files:
            return "No files available."
        return ", ".join(files)
    

    def _get_dir_by_path(self, path_str):
        if path_str == '/' or not path_str:
            return self.fs

        parts = path_str.strip('/').split('/')
        curr = self.fs
        for part in parts:
            if part in curr['children'] and curr['children'][part]['type'] == 'dir':
                curr = curr['children'][part]
            else:
                return self.fs  # fallback ke root jika gagal
            return curr
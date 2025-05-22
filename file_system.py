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
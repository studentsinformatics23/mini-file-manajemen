import datetime
import json
import os

class MiniFileSystem:
  def _init_(self, total_blocks=100):
          self.disk = [None] * total_blocks
          self.fs = {
              'name' : '/',
              'type' : 'dir',
              'children' : {}
          }

        self.current_dir = self.fs

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
        
# Directory Manipulation

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

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
        return None
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

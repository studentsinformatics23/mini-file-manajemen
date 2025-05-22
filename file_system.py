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
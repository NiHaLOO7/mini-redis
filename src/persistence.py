import os
import base64
class AOF:
    def __init__(self, filepath):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.file = open(filepath, 'a')
    
    def log(self, command):
        if getattr(self, 'replaying', False):
            return
        line = ' '.join(command)
        encoded = base64.b64encode(line.encode()).decode()
        self.file.write(encoded + "\n")
        self.file.flush()

    def replay(self, execute_fn):
        self.replaying = True
        file = open(self.filepath, 'r')
        for line in file:
            decoded = base64.b64decode(line.strip()).decode()
            command = decoded.split()
            if command:
                execute_fn(command)
        file.close()
        self.replaying = False

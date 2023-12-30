import socket
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("server.log"),
                        logging.StreamHandler()
                    ])

class FakeFileSystem:
    def __init__(self):
        self.files = {"root": {}}
        self.current_path = ["root"]

    def ls(self, show_all=False):
        current_dir = self.files
        for dir in self.current_path:
            current_dir = current_dir[dir]

        items = []
        for item in current_dir.keys():
            if item.startswith('.') and not show_all:
                continue
            if isinstance(current_dir[item], dict):
                items.append(item + "/")
            else:
                items.append(item)
        return '\n'.join(items)

    def touch(self, filename):
        current_dir = self.files
        for dir in self.current_path:
            current_dir = current_dir[dir]
        current_dir[filename] = ''

    def echo(self, text, filename):
        current_dir = self.files
        for dir in self.current_path:
            current_dir = current_dir[dir]
        current_dir[filename] = text
        return f"Content written to {filename}"

    def cat(self, filename):
        current_dir = self.files
        for dir in self.current_path:
            current_dir = current_dir[dir]
        if filename in current_dir:
            return current_dir[filename]
        return "File not found"

    def mkdir(self, dirname):
        current_dir = self.files
        for dir in self.current_path:
            current_dir = current_dir[dir]
        if dirname not in current_dir:
            current_dir[dirname] = {}
            return f"Directory '{dirname}' created"
        return "Directory already exists"

    def cd(self, dirname):
        if dirname == "..":
            if len(self.current_path) > 1:
                self.current_path.pop()
            return ""
        else:
            current_dir = self.files
            for dir in self.current_path:
                current_dir = current_dir[dir]
            if dirname in current_dir and isinstance(current_dir[dirname], dict):
                self.current_path.append(dirname)
                return ""
            else:
                return "Directory not found"

    def handle_command(self, command):
        logging.info(f"Command received: {command}")
        if ">" in command:
            parts = command.split(">")
            if len(parts) == 2 and parts[0].strip().startswith("echo"):
                text = parts[0][5:].strip().strip('"')
                filename = parts[1].strip()
                return self.echo(text, filename)

        args = command.split()
        if not args:
            return None

        if args[0] == "exit":
            return "exit"

        if args[0] == "ls":
            show_all = len(args) > 1 and args[1] == "-la"
            return self.ls(show_all)
        elif args[0] == "touch" and len(args) > 1:
            self.touch(args[1])
            return f"Created file {args[1]}"
        elif args[0] == "mkdir" and len(args) > 1:
            return self.mkdir(args[1])
        elif args[0] == "cd" and len(args) > 1:
            return self.cd(args[1])
        elif args[0] == "cat" and len(args) > 1:
            return self.cat(args[1])
        else:
            return "Invalid command"

def client_thread(conn, file_system):
    conn.sendall(b"/$ ")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            response = file_system.handle_command(command)
            if response == "exit":
                break
            if response is not None:
                conn.sendall(response.encode() + b"\n")
            conn.sendall(b"/$ ")
    finally:
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)

    print("Server started. Waiting for connections...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected with {addr}")

            threading.Thread(target=client_thread, args=(conn, FakeFileSystem())).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

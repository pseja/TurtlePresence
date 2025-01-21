from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pypresence import Presence
import time
import os

FILE_PATH = "E:\\TWoW\\Imports\\TurtlePresenceData.txt"
CLIENT_ID = ""


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, rpc):
        self.rpc = rpc

    def on_modified(self, event):
        if event.src_path == os.path.abspath(FILE_PATH):
            try:
                presence_data = self.parse_file(FILE_PATH)
                self.update_discord_presence(self.rpc, presence_data)
            except Exception as e:
                print(f"Error processing file: {e}")

    @staticmethod
    def parse_file(file_path):
        """Parse the file and return a dictionary of presence data."""
        presence_data = {}
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                presence_data[key] = value
        return presence_data


    def update_discord_presence(self, rpc, presence_data):
        """Update Discord Rich Presence."""
        # TODO FIX SMALL_IMAGE
        try:
            rpc.update(
                details=f"{presence_data['name']} - Level {presence_data['level']}",
                state=f"{presence_data['zone']} {f"- {presence_data['subzone']}" if presence_data['subzone'] != "" else ""}",
                small_image=f".\\class_images\\{presence_data['class']}.png",
                small_text=f"{presence_data['race']} {f"- {presence_data['class']}" if presence_data['class'] != "" else ""}"
            )
        except Exception as e:
            print(f"Failed to update Discord presence: {e}")


def main():
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    print("Connected to Discord RPC")

    event_handler = FileChangeHandler(rpc)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_PATH), recursive=False)

    try:
        print(f"Watching for changes in {FILE_PATH}...")
        observer.start()
        while True:
            time.sleep(1)  # keep main thread alive
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping observer...")
    observer.join()


if __name__ == "__main__":
    main()

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pypresence import Presence
import time
import os

FILE_PATH = "E:\\TWoW\\Imports\\TurtlePresenceData.txt"
CLIENT_ID = ""


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, rpc, start):
        self.rpc = rpc
        self.start = start


    def on_modified(self, event):
        if event.src_path == os.path.abspath(FILE_PATH):
            try:
                presence_data = self.parse_file(FILE_PATH)
                self.update_discord_presence(self.rpc, presence_data)
            except Exception as e:
                print(f"Error processing file: {e}")


    @staticmethod
    def parse_file(file_path):
        presence_data = {}
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("=", 1)
                presence_data[key] = value
        return presence_data


    def update_discord_presence(self, rpc, presence_data):
        details = f"{presence_data['name']} - Level {presence_data['level']}"
        state = ""
        if presence_data['zone'] == "" and presence_data['subzone'] == "":
            state = "In character selection"
        else:
            state = f"{presence_data['zone']} - {presence_data['subzone']}" if presence_data['subzone'] != "" else presence_data['zone']
        large_image = "twow"
        large_text = "Turtle WoW — Mysteries of Azeroth"
        small_image = f"{presence_data['class'].lower()}"
        small_text = f"{presence_data['race']} {presence_data['class']}"

        try:
            rpc.update(
                start=self.start,
                details=details,
                state=state,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text
            )
        except Exception as e:
            print(f"Failed to update Discord presence: {e}")


def main():
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    print("Connected to Discord RPC")

    event_handler = FileChangeHandler(rpc, time.time())
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_PATH), recursive=False)

    try:
        print("Observing game activity...")
        observer.start()
        while True:
            time.sleep(1)  # keep main thread alive
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping observer...")
    observer.join()


if __name__ == "__main__":
    main()

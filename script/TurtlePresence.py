from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pypresence import Presence
import time
import os

TWOW_PATH = "E:\\TWoW" # change this path to your Turtle WoW directory
FILE_PATH = f"{TWOW_PATH}\\Imports\\TurtlePresenceData.txt" # DON'T CHANGE THIS!
CLIENT_ID = "" # insert your Discord developer Application ID here


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
        details = f"{presence_data['name']} - Level {presence_data['level']}" # character name and level on the first line
        state = ""
        if presence_data['zone'] == "" and presence_data['subzone'] == "":
            state = "In character selection" # if there is no zone and subzone, you are probably in character selection
        else:
            state = f"{presence_data['zone']} - {presence_data['subzone']}" if presence_data['subzone'] != "" else presence_data['zone'] # "zone - subzone", if subzone is "" only zone is shown
        large_image = "twow" # name of the twow image without the file extension
        large_text = "Turtle WoW — Mysteries of Azeroth" # text for large image if you hover over it
        small_image = f"{presence_data['class'].lower()}" # small image with class icon
        small_text = f"{presence_data['race']} {presence_data['class']}" # text for small image if you hover over it

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
    print("Connecting to Discord RPC...", end=" ")
    try:
        rpc.connect()
        print("✅")
    except Exception as e:
        print("❌")
        print(f"\n  > Failed to connect to Discord RPC: {e}")
        input("\nPress Enter to exit...")
        return 1

    event_handler = FileChangeHandler(rpc, time.time())
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_PATH), recursive=False)

    try:
        print("Observing game activity...")
        observer.start()
        while True:
            time.sleep(1)  # keep main thread alive
    except KeyboardInterrupt:
        print("Stopping observer...", end=" ")
        observer.stop()
        print("✅")

        print("Clearing Discord RPC activity...", end=" ")
        try:
            rpc.clear()
            print("✅")
        except Exception as e:
            print("❌")
            print(f"\n  > Failed to clear Discord RPC: {e}")

        print("Disconnecting from Discord RPC...", end=" ")
        try:
            rpc.close()
            print("✅")
        except Exception as e:
            print("❌")
            print(f"\n  > Failed to disconnect from Discord RPC: {e}")

    observer.join()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

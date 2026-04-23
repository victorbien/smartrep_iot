import uuid
from datetime import datetime
#from mqtt_client import publish

class SessionManager:
    def __init__(self, equipment):
        self.state = {
            name: {
                "occupied": False,
                "session_id": None,
                "start_time": None
            }
            for name in equipment
        }

    def handle(self, name, occupied_now):
        prev = self.state[name]["occupied"]

        if not prev and occupied_now:
            self.start_session(name)

        elif prev and not occupied_now:
            self.end_session(name)

    def start_session(self, name):
        session_id = str(uuid.uuid4())
        start_time = datetime.utcnow()

        self.state[name].update({
            "occupied": True,
            "session_id": session_id,
            "start_time": start_time
        })

        #publish({
        #    "event": "session_start",
        #    "equipment": name,
        #    "session_id": session_id,
        #    "start_time": start_time.isoformat()
        #})

        print(f"{name} → SESSION START")

    def end_session(self, name):
        end_time = datetime.utcnow()
        start_time = self.state[name]["start_time"]

        duration = (end_time - start_time).total_seconds()

        #publish({
        #    "event": "session_end",
        #    "equipment": name,
        #    "session_id": self.state[name]["session_id"],
        #    "start_time": start_time.isoformat(),
        #    "end_time": end_time.isoformat(),
        #    "duration_s": duration
        #})

        print(f"{name} → SESSION END ({duration:.1f}s)")

        self.state[name] = {
            "occupied": False,
            "session_id": None,
            "start_time": None
        }

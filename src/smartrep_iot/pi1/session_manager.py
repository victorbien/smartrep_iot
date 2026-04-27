import uuid
from datetime import datetime
from mqtt_client import publish
from config import EVENT, EQUIPMENT_NAME, SESSION_ID, START_TIME, END_TIME, SESSION_DURATION, OCCUPIED

class SessionManager:
    def __init__(self, equipment):
        self.state = {
            name: {
                OCCUPIED: False,
                SESSION_ID: None,
                START_TIME: None
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
            OCCUPIED: True,
            SESSION_ID: session_id,
            START_TIME: start_time
        })

        publish({
            EVENT: "session_start",
            EQUIPMENT_NAME: name,
            SESSION_ID: session_id,
            START_TIME: start_time.isoformat()
        })

        print(f"{name} → SESSION START")

    def end_session(self, name):
        end_time = datetime.utcnow()
        start_time = self.state[name]["start_time"]

        duration = (end_time - start_time).total_seconds()

        publish({
            EVENT: "session_end",
            EQUIPMENT_NAME: name,
            SESSION_ID: self.state[name]["session_id"],
            START_TIME: start_time.isoformat(),
            END_TIME: end_time.isoformat(),
            SESSION_DURATION: duration
        })

        print(f"{name} → SESSION END ({duration:.1f}s)")

        self.state[name] = {
            OCCUPIED: False,
            SESSION_ID: None,
            START_TIME: None
        }


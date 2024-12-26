from typing import List, Dict, Any, Optional
import hashlib
import time

from caldav import DAVClient
from caldav.elements import dav, cdav
from datetime import datetime


from ..module_cache import ModuleCache
from ...utils.logger import Logger

class CalDAV():

    def __init__(self, url: str, username: Optional[str] = None, password: Optional[str] = None):
        self._log = Logger()
        self._log.debug(f"Using url: {url} (username: {username} - password: {password})")
        self.__client = DAVClient(url = url, username = username, password = password)
        principal = self.__client.principal()
        calendars = principal.calendars()
        if not calendars:
            print("No calendars found!")
            exit(1)
        calendar = calendars[0]
        print(f"Using calendar: {calendar.name}")
        """
        events = calendar.date_search(
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 2)
        )
        """
        events = calendar.events()
        for event in events:
            print("Event found:")
            print(event.data)

            from icalendar import Calendar
            cal = Calendar.from_ical(event.data)

            for component in cal.walk():
                if component.name == "VEVENT":
                    print("Summary:", component.get("summary"))
                    print("Start:", component.get("dtstart").dt)
                    print("End:", component.get("dtend").dt)
                    print("Location:", component.get("location"))
                    print()
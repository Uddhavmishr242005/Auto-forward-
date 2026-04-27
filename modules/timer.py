import re
from database.state import StateManager
from config import MAX_HOURS, MAX_MINUTES, MAX_SECONDS

class TimerManager:
    def __init__(self):
        self.state_manager = None

    async def initialize(self):
        self.state_manager = StateManager()
        await self.state_manager.initialize()

    def parse_timer(self, text: str) -> tuple[int, int, int] | None:
        text = text.strip().lower()
        if not text:
            return None

        # Support HH:MM:SS
        if ':' in text:
            parts = text.split(':')
            if len(parts) == 3:
                try:
                    hours, minutes, seconds = map(int, parts)
                    return hours, minutes, seconds
                except ValueError:
                    return None
            return None

        # Support expressions like 60s, 10 sec, 4 second, 5m, 2h
        seconds = 0
        matches = re.findall(r'(?P<value>\d+)\s*(?P<unit>h|hr|hour|hours|m|min|minute|minutes|s|sec|second|seconds)?', text)
        if not matches:
            return None

        for value, unit in matches:
            value = int(value)
            if unit in ('h', 'hr', 'hour', 'hours'):
                seconds += value * 3600
            elif unit in ('m', 'min', 'minute', 'minutes'):
                seconds += value * 60
            else:
                seconds += value

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return hours, minutes, secs

    async def set_timer(self, text: str):
        parsed = self.parse_timer(text)
        if not parsed:
            return "Invalid timer format. Use 60s, 10 sec, 4 seconds, 1:30:10, or 2m."

        hours, minutes, seconds = parsed
        if hours > MAX_HOURS or minutes > MAX_MINUTES or seconds > MAX_SECONDS:
            return f"Invalid timer! Max: {MAX_HOURS}h {MAX_MINUTES}m {MAX_SECONDS}s"

        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        if total_seconds <= 0:
            return "Timer must be greater than 0!"

        await self.state_manager.set_delay(total_seconds)
        return f"Timer set to {hours}h {minutes}m {seconds}s ({total_seconds}s total)"

    async def get_current_timer(self):
        delay = (await self.state_manager.get_all())['delay_time']
        hours = delay // 3600
        minutes = (delay % 3600) // 60
        seconds = delay % 60
        return f"Current timer: {hours}h {minutes}m {seconds}s"
from discord import Activity, ActivityType
from datetime import timezone, timedelta

# Your current timezone here
currentTimezone = timezone(timedelta(hours=2, minutes=30))

# Category under which the channel names are to be changed
categoryName = "Schedule"

# Custom bot status
botActivity = Activity(name="with discord", type=ActivityType.playing)

# Discord bot token
BOT_TOKEN = "XXX"

# Google calendar Id
calendarId = "calendar-id@group.calendar.google.com"

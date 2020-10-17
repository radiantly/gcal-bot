from asyncio import sleep
from datetime import datetime, timedelta, timezone

import discord

from cal import getEvents
from config import currentTimezone, categoryName, botActivity, BOT_TOKEN

client = discord.Client()


async def updateChannels(guildChannels: list):
    # Returns time in HH:MM format with no leading zero
    prettyTime = lambda eventTime: eventTime["dateTime"].strftime("%I:%M").lstrip("0")

    # Computes channel name
    channelName = (
        lambda event: f'{prettyTime(event["start"])}-{prettyTime(event["end"])} {event["summary"]}'
    )

    # Gets current time to specified timezone
    currentTime = lambda: datetime.now(currentTimezone)

    # Helper method to convert datetimestr to datetime obj
    def toDatetimeObj(eventTime: str):
        eventTime["dateTime"] = datetime.fromisoformat(eventTime["dateTime"])

    # Helper method to quickly edit channels
    async def editChannels(text1: str, text2: str):
        for channel1, channel2 in guildChannels:
            await channel1.edit(name=text1)
            await channel2.edit(name=text2)

    while True:
        # Get next 2 events
        thisEvent, nextEvent = getEvents()

        # The response returns datetime strings. Convert these to datetime objects
        toDatetimeObj(thisEvent["start"])
        toDatetimeObj(thisEvent["end"])
        toDatetimeObj(nextEvent["start"])
        toDatetimeObj(nextEvent["end"])

        # If next event is more than 10mins away, display "Free now :)"
        if thisEvent["start"]["dateTime"] > currentTime() + timedelta(minutes=10):
            await editChannels("Free now :)", f"Next: {channelName(thisEvent)}")

            # Wait for event to start
            timeForEventStart = thisEvent["start"]["dateTime"] - currentTime()
            print(f"Sleeping for {timeForEventStart.total_seconds()}")
            await sleep(timeForEventStart.total_seconds())

        # Show event
        await editChannels(channelName(thisEvent), f"Next: {channelName(nextEvent)}")

        # Calculate time left for next update
        timeLeftForThisEventEnd = thisEvent["end"]["dateTime"] - currentTime()
        nextUpdateDelay = max(timeLeftForThisEventEnd.total_seconds(), 600)

        print(f"Next update in {nextUpdateDelay}")
        await sleep(nextUpdateDelay)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    await client.change_presence(activity=botActivity)

    channels = []
    for guild in client.guilds:
        category = discord.utils.get(guild.categories, name=categoryName)
        if not category or len(category.channels) < 2:
            continue
        channels.append(category.channels[:2])

    await updateChannels(channels)


@client.event
async def on_message(message):
    if message.author == client.user:
        return


def main():
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()

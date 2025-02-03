import asyncio
import datetime

import ctftime_api
from ctftime_api.models import Event


async def main():
    client = ctftime_api.CTFTimeClient()

    # Get top teams for the current year
    top_teams = await client.get_top_teams_per_year()
    print("Top Teams:", top_teams)

    # Get top teams for a specific country
    top_teams_us = await client.get_top_team_by_country("US")
    print("Top Teams in US:", top_teams_us)

    # Get events information between two dates
    start_date = datetime.datetime(2024, 12, 4)
    end_date = datetime.datetime(2024, 12, 9)
    events = await client.get_events_information(start_date, end_date)
    print("Events:", events)

    # Find the snakeCTF event
    event: Event | None = None
    for e in events:
        if e.title.startswith("snakeCTF"):
            event = e
            break

    # Get information about a specific event
    event_info = await client.get_event_information(event.ctf_id)
    print("Event Information:", event_info)

    # Get information about teams with pagination
    teams = await client.get_teams_information(limit=5, offset=0)
    print("Teams:", teams)

    # Get information about a specific team
    team_info = await client.get_team_information(event.organizers[0].id)
    print("Team Information:", team_info)

    # Get event results for the current year
    event_results = await client.get_event_results()
    print("Event Results:", event_results)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

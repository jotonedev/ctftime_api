from datetime import datetime

import httpx
from httpx import URL, Timeout

from pydantic_extra_types.country import CountryAlpha2

from ctftime_api.models.vote import Vote
from ctftime_api.models.event import Event, EventResult
from ctftime_api.models.team import TeamRank, Team, TeamComplete


__all__ = ["CTFTimeClient"]


class CTFTimeClient:
    def __init__(self, client: httpx.AsyncClient | None = None, *args, **kwargs):
        """
        Initialize the CTFTime API client.
        :param client: The httpx.AsyncClient to use. If None, a new client will be created.
        :param args: Args that will be passed to the httpx.AsyncClient constructor.
        :param kwargs: Kwargs that will be passed to the httpx.AsyncClient constructor.
        """
        if client is not None:
            self._client = client
        else:
            self._client = httpx.AsyncClient(*args, **kwargs)
        self._base_url = URL("https://ctftime.org/api/v1/")

    async def close(self):
        """Close the underlying httpx.AsyncClient."""
        await self._client.aclose()

    async def get_top_teams_per_year(
        self, year: int | None = None, limit: int = 10
    ) -> list[TeamRank]:
        """
        Get the top teams in the leaderboard for a specific year.
        :param year: The year to get the top teams for. If None, the current year will be used.
        :param limit: The number of teams to get.
        :return: A list of the top teams.
        """
        if year is None:
            url = self._base_url.join("top/")
            year = datetime.now().year
        else:
            url = self._base_url.join(f"top/{year}/")
        response = await self._client.get(url, params={"limit": limit})
        response.raise_for_status()

        teams = response.json().get(f"{year}", [])

        return [TeamRank.model_validate(team) for team in teams]

    async def get_top_team_by_country(
        self, country: str | CountryAlpha2
    ) -> list[TeamRank]:
        """
        Get the top teams in the leaderboard for a specific country.
        :param country: The country to get the top teams for.
            It can be a pycountry Country object or a two-letter country code.
        :return: A list of the top teams.
        """
        if isinstance(country, CountryAlpha2):
            country = country
        elif isinstance(country, str):
            if len(country) != 2:
                raise ValueError(
                    "Country must be a two-letter country code or a pycountry Country object."
                )

        url = self._base_url.join("top-by-country/").join(f"{country}/")
        response = await self._client.get(url)
        response.raise_for_status()

        teams = response.json()

        return [TeamRank.model_validate(team) for team in teams]

    async def get_events_information(
        self, start: int | datetime, end: int | datetime, limit: int = 10
    ) -> list[Event]:
        """
        Get information about events that are happening between two dates.
        :param start: The start date of the events.
            It can be a Unix timestamp or a datetime object.
        :param end: The end date of the events.
            It can be a Unix timestamp or a datetime object.
        :param limit: The number of events to get.
        :return: A list of events.
        """
        if isinstance(start, datetime):
            start = int(start.timestamp())
        if isinstance(end, datetime):
            end = int(end.timestamp())

        if start > end:
            raise ValueError("The start date must be before the end date.")

        url = self._base_url.join("events/")
        response = await self._client.get(
            url, params={"start": start, "finish": end, "limit": limit}
        )
        response.raise_for_status()

        events = response.json()

        return [Event.model_validate(event) for event in events]

    async def get_event_information(self, event_id: int) -> Event:
        """
        Get information about a specific event.
        :param event_id: The ID of the event.
        :return: The event information.
        """
        url = self._base_url.join(f"events/{event_id}/")
        response = await self._client.get(url)
        response.raise_for_status()

        event = response.json()

        return Event.model_validate(event)

    async def get_teams_information(
        self, limit: int = 100, offset: int = 0
    ) -> list[Team]:
        """
        Get information about teams.
        :param limit: The number of teams to get.
        :param offset: The offset to start from.
        :return: A list of teams.
        """
        url = self._base_url.join("teams/")
        response = await self._client.get(
            url, params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()

        teams = response.json().get("results", [])

        return [Team.model_validate(team) for team in teams]

    async def get_team_information(self, team_id: int) -> TeamComplete:
        """
        Get information about a specific team.
        :param team_id: The ID of the team.
        :return: The team information.
        """
        url = self._base_url.join(f"teams/{team_id}/")
        response = await self._client.get(url)
        response.raise_for_status()

        team = response.json()

        return TeamComplete.model_validate(team)

    async def get_event_results(
        self, year: int | None = None
    ) -> dict[int, EventResult]:
        """
        Get the results of the events for a specific year.
        :param year: The year to get the results for.
            If None, the current year will be used.
        :return: A dictionary of event results.
        """
        if year is None:
            url = self._base_url.join("results/")
        else:
            url = self._base_url.join(f"results/{year}/")

        response = await self._client.get(url)
        response.raise_for_status()

        event = response.json()

        return {
            int(ctf_id): EventResult(**result, ctf_id=ctf_id)
            for ctf_id, result in event.items()
        }

    async def get_votes_per_year(
        self, year: int | None, timeout: Timeout | int | float | None = None
    ) -> list[Vote]:
        """
        Get the votes for a specific year.
        This API call may take a long time to complete.
        :param year: The year to get the votes for or None for the current year.
        :param timeout: The timeout for the request.
            If None, the session timeout will be used.
        :return: A list of votes.
        """
        if year is None:
            year = datetime.now().year

        if timeout is None:
            timeout = self._client.timeout

        url = self._base_url.join(f"votes/{year}/")
        response = await self._client.get(url, timeout=timeout)
        response.raise_for_status()

        votes = response.json()

        return [Vote(**vote) for vote in votes]

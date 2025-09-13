import importlib.util
from datetime import datetime
from typing import Any

import httpx
from httpx import URL, Timeout

from ctftime_api.models.country import CountryCode
from ctftime_api.models.event import Event, EventResult
from ctftime_api.models.team import Team, TeamComplete, TeamRank
from ctftime_api.models.vote import Vote

__all__ = ["CTFTimeClient"]

h2 = importlib.util.find_spec("httpcore.h2")


class CTFTimeClient:
    def __init__(self, client: httpx.AsyncClient | None = None, **kwargs):
        """
        Initialize the CTFTime API client.
        :param client: The httpx.AsyncClient to use. If None, a new client will be created.
        :param kwargs: Kwargs that will be passed to the httpx.AsyncClient constructor.
        """
        if client is not None:
            self._client = client
        else:
            if h2 is not None:
                kwargs.setdefault("http2", True)
            self._client = httpx.AsyncClient(**kwargs)
        self._base_url = URL("https://ctftime.org/api/v1/")

    async def _get(self, url: str | URL, **kwargs) -> Any:
        """
        Perform a GET request.
        :param url: The url to make the request to.
        :param kwargs: Additional arguments to pass to the request.
        :return: The response JSON.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        response = await self._client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

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
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        if year is None:
            url = self._base_url.join("top/")
            year = datetime.now().year
        else:
            url = self._base_url.join(f"top/{year}/")

        response: dict[str, list[dict]] = await self._get(url, params={"limit": limit})
        teams = response.get(f"{year}", [])

        return [TeamRank.from_dict(team) for team in teams]

    async def get_top_team_by_country(
        self, country: str | CountryCode
    ) -> list[TeamRank]:
        """
        Get the top teams in the leaderboard for a specific country.
        :param country: The country to get the top teams for.
            It can be a pycountry Country object or a two-letter country code.
        :return: A list of the top teams.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        :raise ValueError: If the country is not a two-letter country code or a pycountry Country object.
        """
        if isinstance(country, str):
            if len(country) != 2:
                raise ValueError(
                    "Country must be a two-letter country code or a pycountry Country object."
                )

        url = self._base_url.join("top-by-country/").join(f"{country}/")
        teams: list[dict[str, Any]] = await self._get(url)

        return [TeamRank.from_dict(team) for team in teams]

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
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        :raise ValueError: If the start date is after the end date.
        """
        if isinstance(start, datetime):
            start = int(start.timestamp())
        if isinstance(end, datetime):
            end = int(end.timestamp())

        if start > end:
            raise ValueError("The start date must be before the end date.")

        url = self._base_url.join("events/")
        events: list[dict[str, Any]] = await self._get(
            url, params={"start": start, "finish": end, "limit": limit}
        )

        return [Event.from_dict(event) for event in events]

    async def get_event_information(self, event_id: int) -> Event:
        """
        Get information about a specific event.
        :param event_id: The ID of the event.
        :return: The event information.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        url = self._base_url.join(f"events/{event_id}/")
        event: dict[str, Any] = await self._get(url)

        return Event.from_dict(event)

    async def get_teams_information(
        self, limit: int = 100, offset: int = 0
    ) -> list[Team]:
        """
        Get information about teams.
        :param limit: The number of teams to get.
        :param offset: The offset to start from.
        :return: A list of teams.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        url = self._base_url.join("teams/")

        response: dict[str, Any] = await self._get(
            url, params={"limit": limit, "offset": offset}
        )
        teams: list[dict[str, Any]] = response.get("results", [])

        return [Team.from_dict(team) for team in teams]

    async def get_team_information(self, team_id: int) -> TeamComplete:
        """
        Get information about a specific team.
        :param team_id: The ID of the team.
        :return: The team information.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        url = self._base_url.join(f"teams/{team_id}/")
        team: dict[str, Any] = await self._get(url)

        return TeamComplete.from_dict(team)

    async def get_event_results(
        self, year: int | None = None
    ) -> dict[int, EventResult]:
        """
        Get the results of the events for a specific year.
        :param year: The year to get the results for.
            If None, the current year will be used.
        :return: A dictionary of event results.
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        if year is None:
            url = self._base_url.join("results/")
        else:
            url = self._base_url.join(f"results/{year}/")

        event: dict[str, dict] = await self._get(url)

        return {
            int(ctf_id): EventResult.from_dict(result)
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
        :raise httpx.HTTPStatusError: If the response status code is not successful.
        """
        if year is None:
            year = datetime.now().year

        if timeout is None:
            timeout = self._client.timeout

        url = self._base_url.join(f"votes/{year}/")
        votes: list[dict] = await self._get(url, timeout=timeout)

        return [Vote.from_dict(vote) for vote in votes]

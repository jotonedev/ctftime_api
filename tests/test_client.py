import unittest
from datetime import datetime

import httpx

from ctftime_api.client import CTFTimeClient
from ctftime_api.models.event import Event, EventResult
from ctftime_api.models.team import Team, TeamComplete, TeamRank
from ctftime_api.models.vote import Vote


def get_client(response) -> CTFTimeClient:
    async def handler(request):
        return httpx.Response(200, json=response)

    transport = httpx.MockTransport(handler)
    async_client = httpx.AsyncClient(transport=transport)
    return CTFTimeClient(client=async_client)


class TestCTFTimeClient(unittest.IsolatedAsyncioTestCase):
    async def test_get_top_teams_per_year(self):
        current_year = str(datetime.now().year)
        mock_response = {
            current_year: [
                {"team_name": "Dragon Sector", "points": 1793.17, "team_id": 3329},
                {
                    "team_name": "Plaid Parliament of Pwning",
                    "points": 1592.18,
                    "team_id": 284,
                },
            ]
        }
        client = get_client(mock_response)
        teams = await client.get_top_teams_per_year()
        self.assertIsInstance(teams, list)
        self.assertTrue(all(isinstance(t, TeamRank) for t in teams))
        self.assertEqual(teams[0].team_id, 3329)
        self.assertEqual(teams[0].team_name, "Dragon Sector")
        self.assertEqual(teams[1].team_id, 284)
        self.assertEqual(teams[1].team_name, "Plaid Parliament of Pwning")
        await client.close()

    async def test_get_top_team_by_country(self):
        mock_response = [
            {
                "country_place": 1,
                "team_id": 210132,
                "points": 57.70,
                "team_country": "RU",
                "place": 36,
                "team_name": "Drovosec",
                "events": 3,
            },
            {
                "country_place": 2,
                "team_id": 273508,
                "points": 53.08,
                "team_country": "RU",
                "place": 39,
                "team_name": "CYBERSQD",
                "events": 3,
            },
        ]
        client = get_client(mock_response)
        teams = await client.get_top_team_by_country("US")
        self.assertIsInstance(teams, list)
        self.assertEqual(teams[0].team_id, 210132)
        self.assertEqual(teams[0].team_name, "Drovosec")
        self.assertEqual(teams[1].team_id, 273508)
        self.assertEqual(teams[1].team_name, "CYBERSQD")
        await client.close()

    async def test_get_event_information(self):
        mock_response = {
            "organizers": [
                {"id": 3641, "name": "Marauders"},
                {"id": 4890, "name": "Men in Black Hats"},
            ],
            "ctftime_url": "https://ctftime.org/event/165/",
            "ctf_id": 26,
            "weight": 80,
            "duration": {"hours": 21, "days": 1},
            "live_feed": "",
            "logo": "",
            "id": 165,
            "title": "Ghost in the Shellcode 2015",
            "start": "2015-01-16T20:30:00+00:00",
            "participants": 110,
            "location": "Washington, DC",
            "finish": "2015-01-18T17:30:00+00:00",
            "description": "<img src=https://ghostintheshellcode.com/>",
            "format": "Jeopardy",
            "is_votable_now": False,
            "prizes": "",
            "format_id": 1,
            "onsite": False,
            "restrictions": "Open",
            "url": "http://ghostintheshellcode.com/",
            "public_votable": False,
        }
        client = get_client(mock_response)
        event = await client.get_event_information(165)
        self.assertIsInstance(event, Event)
        self.assertEqual(event.id, 165)
        self.assertEqual(event.title, "Ghost in the Shellcode 2015")
        await client.close()

    async def test_get_team_information(self):
        mock_response = {
            "academic": False,
            "primary_alias": "More Smoked Leet Chicken",
            "name": "More Smoked Leet Chicken",
            "rating": {
                "2025": {
                    "rating_place": 827,
                    "organizer_points": 0,
                    "rating_points": 4.65635065443,
                    "country_place": 31,
                }
            },
            "logo": "https://ctftime.org//media/team/mslc_150x150_ctftime.png",
            "country": "RU",
            "id": 1005,
            "aliases": [
                "LeetChicken",
                "MoreSmokedLeetChicken",
                "Leet Chicken",
                "MSLC",
                "MoreSmoked LeetChicken",
            ],
        }
        client = get_client(mock_response)
        team = await client.get_team_information(1005)
        self.assertIsInstance(team, TeamComplete)
        self.assertEqual(team.team_id, 1005)
        self.assertEqual(team.team_name, "More Smoked Leet Chicken")
        self.assertEqual(team.primary_alias, "More Smoked Leet Chicken")
        await client.close()

    async def test_get_teams_information(self):
        mock_response = {
            "limit": 2,
            "results": [
                {
                    "aliases": ["MiTeam", ".MiT."],
                    "country": "RU",
                    "academic": False,
                    "id": 1,
                    "name": "MiT",
                },
                {
                    "aliases": ["smokedchicken"],
                    "country": "RU",
                    "academic": False,
                    "id": 2,
                    "name": "Smoked Chicken",
                },
            ],
            "offset": 0,
        }
        client = get_client(mock_response)
        teams = await client.get_teams_information(limit=2, offset=0)
        self.assertEqual(len(teams), 2)
        self.assertTrue(all(isinstance(t, Team) for t in teams))
        self.assertEqual(teams[0].team_id, 1)
        self.assertEqual(teams[0].team_name, "MiT")
        self.assertEqual(teams[1].team_id, 2)
        self.assertEqual(teams[1].team_name, "Smoked Chicken")
        await client.close()

    async def test_get_events_information(self):
        mock_response = [
            {
                "organizers": [{"id": 10498, "name": "th3jackers"}],
                "ctftime_url": "https://ctftime.org/event/190/",
                "ctf_id": 93,
                "weight": 5,
                "duration": {"hours": 12, "days": 0},
                "live_feed": "",
                "logo": "",
                "id": 190,
                "title": "WCTF  - th3jackers",
                "start": "2015-01-23T20:00:00+00:00",
                "participants": 18,
                "location": "",
                "finish": "2015-01-24T08:00:00+00:00",
                "description": "Registration will be open when CTF Start\r\n#WCTF #th3jackers\r\nhttp://ctf.th3jackers.com/",
                "format": "Jeopardy",
                "is_votable_now": False,
                "prizes": "",
                "format_id": 1,
                "onsite": False,
                "restrictions": "Open",
                "url": "http://ctf.th3jackers.com/",
                "public_votable": False,
            }
        ]
        client = get_client(mock_response)
        start_date = datetime(2015, 1, 23)
        end_date = datetime(2015, 1, 24)
        events = await client.get_events_information(
            start=start_date, end=end_date, limit=1
        )
        self.assertEqual(len(events), 1)
        self.assertTrue(all(isinstance(ev, Event) for ev in events))
        self.assertEqual(events[0].id, 190)
        self.assertEqual(events[0].title, "WCTF  - th3jackers")
        self.assertEqual(events[0].ctf_id, 93)
        self.assertEqual(events[0].duration.hours, 12)
        await client.close()

    async def test_get_event_results(self):
        mock_response = {
            "101": {
                "title": "Event Results",
                "time": 1737741600,
                "scores": [
                    {"team_id": 280849, "points": "6296.0000", "place": 1},
                    {"team_id": 369827, "points": "6006.0000", "place": 2},
                ],
            }
        }
        client = get_client(mock_response)
        results = await client.get_event_results(2023)
        self.assertIn(101, results)
        self.assertIsInstance(results[101], EventResult)
        self.assertEqual(results[101].title, "Event Results")
        await client.close()

    async def test_get_votes_per_year(self):
        mock_response = [
            {
                "event_id": 2467,
                "user_id": 68035,
                "user_teams": [369827, 225509, 109611],
                "weight": "25.00",
                "creation_date": 1737916238,
            },
            {
                "event_id": 2467,
                "user_id": 204301,
                "user_teams": [351259],
                "weight": "25.00",
                "creation_date": 1737916305,
            },
        ]
        client = get_client(mock_response)
        votes = await client.get_votes_per_year(2025)
        self.assertIsInstance(votes, list)
        self.assertTrue(all(isinstance(v, Vote) for v in votes))
        self.assertEqual(len(votes), 2)
        self.assertEqual(votes[0].event_id, 2467)
        self.assertEqual(votes[0].user_id, 68035)
        self.assertEqual(votes[0].weight, "25.00")

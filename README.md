# ctftime_api

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ctftime_api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fctftime_api%2F)
![PyPI - Status](https://img.shields.io/pypi/status/ctftime_api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fctftime_api%2F)
![PyPI - Version](https://img.shields.io/pypi/v/ctftime_api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fctftime_api%2F)

A simple Python wrapper for the CTFTime API that provides an asynchronous interface to retrieve CTF event and team information.

## Features

- **Asynchronous**: Utilize Python's async/await for non-blocking API requests.
- **Type Safe**: Fully type annotated using Pydantic models.
- **Modular**: Organized into client and models modules for easy maintenance and extension.
- **Tested**: Includes comprehensive unit tests in the [tests](tests/) directory.

## Installation

Install via pip:

```sh
pip install ctftime_api
```

## Usage

Create a client to interact with the CTFTime API. For example, to get the top teams for the current year:

```python
import asyncio
from ctftime_api.client import CTFTimeClient

async def main():
    client = CTFTimeClient()
    top_teams = await client.get_top_teams_per_year()
    for team in top_teams:
        print(f"{team.name} (ID: {team.id}) - Points: {team.points}")
    await client.close()

asyncio.run(main())
```

For more detailed examples, check the examples directory.

## Documentation

Full API documentation is available at [https://jotonedev.github.io/ctftime_api](https://jotonedev.github.io/ctftime_api).

## Contributing

This project is licensed under the GNU General Public License v3 or later (GPLv3+).

## Additional Resources

- [Project Documentation Website](https://jotonedev.github.io/ctftime_api)
- [GitHub Repository](https://github.com/jotonedev/ctftime_api)

## License

This project is released under the [GPL 3.0 or later](LICENSE) license.

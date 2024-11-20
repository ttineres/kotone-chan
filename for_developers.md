# ことねちゃんbot for Developers

This page outlines the installation steps for running ことねちゃんbot on Discord.

> [!Note]
> This repository contains variables that are specific to ことねちゃんbot. To run your own bot, consider modifying those variables, such as the emoji dicts in `kotone/utils/emoji.py`.

# Prerequisites

ことねちゃんbot currently runs on Python 3.12 or 3.13.

# Installation

After [cloning this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository), create a virtual environment in the same directory. (This step is optional but recommended.)

```
# Linux / macOS
$ python3 -m venv .venv
$ . .venv/bin/activate

# Windows
> py -3 -m venv .venv
> .venv\Scripts\activate
```

Next, install the `kotone` package using pip.

```
# Linux / macOS
$ python3 -m pip install .

# Windows
> py -3 -m pip install .
```

# Running the bot

Ensure that your bot has the following Discord permissions:

|Permission          |         |
|--------------------|---------|
|`Send Messages`     |Necessary|
|`Manage Messages`   |Optional |
|`Use Slash Commands`|Necessary|

The following environment variables, stored in `.env`, are used to configure the bot:

|Variable         |Content                                                                         |
|-----------------|--------------------------------------------------------------------------------|
|`DISCORD_TOKEN`  |Your Discord bot token                                                          |
|`YOUTUBE_API_KEY`|Your YouTube API key, only necessary for running `kotone/slash_youtube_utils.py`|
|`TEST_GUILD`     |Your private Discord server for debugging this bot                              |
|`DEBUGGING`      |Set this value to `TRUE` for debugging; see below                               |

Run the bot.

```
$ kotone-init
```

Your bot is now live on Discord!

In debug mode with `DEBUGGING` set to `'TRUE'`, your bot will only update commands to your personal testing Discord server.

# Testing the bot

Install the necessary modules from `test_requirements.txt`.

```
pip install -r test_requirements.txt
```

Run the tests inside `tests` directory using `coverage`.

```
$ coverage run -m pytest
```

To generate a report, either use

```
$ coverage report
```

or

```
$ coverage html
```
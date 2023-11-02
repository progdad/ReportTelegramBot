***UPD:** The Bot was permanently terminated, and it's not to be found on Telegram. The repository is not deleted as it contains useful examples on working with different python tools for Telegram.* 

.

## Introduction

**It is the source code of _@blockru_bot_ telegram bot. Bot sends reports on telegram channels you send him.**

.

.

.

## Quick Setup

**First and foremost is to setup a userbot for your telegram account. It's implemented with the [_pyrogram library_](https://docs.pyrogram.org/).**

**[Complete instruction(Ukrainian language)](https://telegra.ph/%D0%86nstrukc%D1%96ya-koristuvannya-botom-blockru-bot-04-02)**

.

.

.

## Project Structure:

*_The project structure is organized as follows to manage various aspects of the bot's functionality_

**1** **_logs/_** directory is just logs. It contains .log files for each user who has merely started the bot. 
Each log file name is just a user id in telegram - _<user_id>.log_.

.

.

**2** **_user_sessions/_** dir contains user sessions of users' userbots. 

.

.


**3 _scripts/_ directory contains all the python project files:**

.
    
**3.1** **_bot.py_** is the primary project file that runs telegram bot. __ init __.py file contains _API_BOT_TOKEN_ variable 
that is supposed to save the bot's api token.

.

**3.2** **_core_buttons/_** .py files in this directory handle inline and keyboard buttons.

.

**3.3** **_database/_** dir stores sqlite _database.db_ file which is created when the first user to use the bot sets up his userbot data.
Database contains only three fields: _user_id_, _api_id_ and _api_hash_, that are needed every time when a user reports channels. 
This directory also has _api_data.py_ file which interacts with the database. [_aiosqlite_](https://pypi.org/project/aiosqlite/) library is used as an sqlite driver for python.

.

**3.4** **_logger_settings/_** is a directory for handling logs and sending error messages to users.

.

**3.5** **_handlers/_** directory has two primary project tools for the project bot:

**3.5.1** _setup_userbot.py_ stores a class which is responsible for setting up userbots and userbot sessions.

**3.5.2** _report_handler.py_ sends reports.

.

**_fsm_states/_** directory contains all the aiogram FSMContext states.
.

**It is the source code of _@blockru_bot_ telegram bot. Bot sends reports on telegram channels that you send to it.**
**But at first you have to set up your userbot, that is possible because of pyrogram library > _https://docs.pyrogram.org/_**

**You can see complete instruction here(Ukrainian language) > _https://telegra.ph/%D0%86nstrukc%D1%96ya-koristuvannya-botom-blockru-bot-04-02_**

.

.

.

# PROJECT STRUCTURE:

**1** **_logs/_** directory is just logs. It contains .log files for each user who has at least started the bot. 
Each log file name is just a user id in telegram - _<user_id>.log_

.

.

**2** **_user_sessions/_** dir contains user sessions of users userbots. 

.

.


**3 _scripts/_ directory contains all the python project files:**

.
    
**3.1** **_bot.py_** is the main project file that runs telegram bot. __ init __.py file contains _API_BOT_TOKEN_ variable 
that is supposed to save telegram bot api token.

.

**3.2** **_core_buttons/_** directory is responsible for inline and keyboard buttons, that are imported into all the other project files.

.

**3.3** **_database/_** dir saves sqlite _database.db_ file which will be created when the first user who uses the bot sets up his userbot.
Database contains only three fields: _user_id_, _api_id_ and _api_hash_, that are needed every time when user reports channels. 
This directory also has _api_data.py_ file which interacts with the database. aiosqlite library is used as a python sqlite driver.

.

**3.4** In the **_logger_settings/_** are contained two python files that set up project logging and the function that informs user about errors.

.

**3.5** **_handlers/_** directory has two necessary project tools, that actually makes this project work:

**3.5.1** First is _setup_userbot.py_ that is contains class which is responsible for setting up userbot and userbot session.

**3.5.2** And the second tool is _report_handler.py_ which make reports on the channel.

*****_fsm_states/_** directory is a directory that contains all the aiogram FSMContext states.

.

# Join the bot and Слава Україні !

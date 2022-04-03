from __future__ import annotations
import aiosqlite
from logger_settings.logger_setup import set_logger


class BotDB:
    @staticmethod
    async def __create_table(cursor):
        await cursor.execute("CREATE TABLE IF NOT EXISTS user_api (uid INTEGER, api_id VARCHAR(20), api_hash VARCHAR(100))")

    async def get_api_data(self, uid: int):
        logger = await set_logger(namespace="BotDB.get_api_data", uid=uid)

        connection = await aiosqlite.connect("database/database.db")
        cursor = await connection.cursor()

        await self.__create_table(cursor)

        logger.info("request for getting user data")
        await cursor.execute(f"SELECT api_id, api_hash FROM user_api WHERE uid={uid}")
        api_data = await cursor.fetchall()
        logger.info("successful request")

        await connection.close()

        return api_data

    async def save_api_data(self, uid: int, api_id: str, api_hash: str):
        logger = await set_logger(namespace="BotDB.save_api_data", uid=uid)

        connection = await aiosqlite.connect("database/database.db")
        cursor = await connection.cursor()

        await self.__create_table(cursor)

        data = await self.get_api_data(uid)
        if data:
            await connection.execute(f"DELETE FROM user_api WHERE uid={uid}")
            logger.info("successfully deleted user data from the database")

        await cursor.execute(f"INSERT INTO user_api VALUES ('{uid}', '{api_id}', '{api_hash}')")
        await connection.commit()
        await connection.close()
        logger.info("successfully saved user data into the database")
        

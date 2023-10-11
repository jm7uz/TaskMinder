from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            telegram_id bigint NOT NULL UNIQUE,
            fullname varchar(250),
            PRIMARY KEY (telegram_id)
        )
        """
        await self.execute(sql, execute=True)
    
    async def create_table_messages(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Messages (
            id SERIAL PRIMARY KEY,
            user_id bigint NOT NULL,
            yesterday varchar(5000),
            today varchar(5000),
            tomorrow varchar(5000),
            created_at DATE NOT NULL DEFAULT CURRENT_DATE
        )
        """
        await self.execute(sql, execute=True)
    
    async def create_table_time_control(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Time (
            id SERIAL PRIMARY KEY,
            time TIME
        )
        """
        await self.execute(sql, execute=True)
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id : int, fullname : str):
        sql = """
        INSERT INTO Users(telegram_id, fullname) VALUES($1, $2)
        """
        return await self.execute(sql, telegram_id, fullname, fetchrow=True)
    
    async def add_message(self, user_id, yesterday, today, tomorrow):
        sql = """
        INSERT INTO Messages(user_id, yesterday, today, tomorrow) VALUES($1, $2, $3, $4)
        """
        return await self.execute(sql, user_id, yesterday, today, tomorrow, fetchrow=True)

    async def add_time(self, time):
        sql = """
        INSERT INTO Time(time) VALUES($1)
        """
        return await self.execute(sql, time, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def update_user_fullname(self, fullname, telegram_id):
        sql = "UPDATE Users SET fullname=$1 WHERE telegram_id=$2"
        return await self.execute(sql, fullname, telegram_id, execute=True)
    
    async def select_all_messages(self):
        sql = "SELECT * FROM Messages"
        return await self.execute(sql, fetch=True)
    
    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_messages(self):
        await self.execute("DELETE FROM Messages WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def get_scheduled_messages(self, current_time):
        sql = "SELECT * FROM Time WHERE time=$1"
        return await self.execute(sql, current_time, fetchval=True)
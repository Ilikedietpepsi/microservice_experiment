from nameko.rpc import rpc
from nameko.events import EventDispatcher
import asyncio
import aiomysql
import selectors


class AsyncMySQLX:
    name = "async_mysql_x"

    dispatch = EventDispatcher()

    def __init__(self):
        self.pool = None

    async def connect_to_mysql(self):
        self.pool = await aiomysql.create_pool(
            host="mysql",
            user="root",
            password="hezhenmin2000",
            db="test",
            autocommit=True
        )

    async def fetch_data(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM customer")
                rows = await cur.fetchall()
                return rows

    async def insert_data(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                sql_query = "INSERT INTO customer () VALUES ()"
                res = await cur.execute(sql_query)
                return res



    async def process_data(self, ACTION):
        if self.pool is None:
            pool = await self.connect_to_mysql()

        if ACTION == 'FETCH':
            rows = await self.fetch_data()

            processed_data = ''
            for x in rows:
                processed_data += str(x) + '\n'

            return processed_data
        if ACTION == 'INSERT':
            res = await self.insert_data()
            return res
        pool.close()
        await pool.wait_closed()
        return ''

    @rpc
    def run(self, ACTION):
        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
        asyncio.set_event_loop(loop)
        res = loop.run_until_complete(self.process_data(ACTION))
        self.dispatch("processed_data_event", res)
        return res
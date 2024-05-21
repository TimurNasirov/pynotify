from aiosqlite import connect
from bot import send
from random import randint, choice

def key():
    key = ''
    for i in range(20):
        if randint(1, 2) == 1:
            key += str(randint(1, 9))
        else:
            letter = choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
            if randint(1, 3) == 1:
                key += letter.upper()
            else:
                key += letter.lower()
    return key

class DB:
    async def init(self):
        self.connect = await connect('database.db')
        self.cursor = await self.connect.cursor()
    
    async def create_tables(self):
        await self.cursor.execute('CREATE TABLE IF NOT EXISTS keys(id INTEGER PRIMARY KEY, key TEXT, app TEXT)')
        await self.cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, userid TEXT, key TEXT)')
        await self.cursor.execute('CREATE TABLE IF NOT EXISTS notifies(id INTEGER PRIMARY KEY, key TEXT, user INTEGER, message TEXT)')

    async def query(self, query):
        await self.cursor.execute(query)
        await self.connect.commit()
    
    async def fetch(self, one=False):
        data = ''
        if one:
            data = await self.cursor.fetchone()
        else:
            data = await self.cursor.fetchall()
        return data

db = DB()

async def create_key(app):
    await db.query(f'INSERT INTO keys(key, app) VALUES("{key()}", "{app}")')
    await db.query(f'SELECT * FROM keys WHERE id=(SELECT MAX(id) FROM keys)')
    
    data = await db.fetch(1)
    return {'id': data[0], 'key': data[1], 'app': data[2]}

async def is_key(key):
    await db.query(f'SELECT * FROM keys WHERE key="{key}"')
    return await db.fetch(1)


async def create_user(key, userid):
    await db.query(f'INSERT INTO users(key, userid) VALUES("{key}", "{userid}")')
    await db.query(f'SELECT * FROM users WHERE id=(SELECT MAX(id) FROM users)')
    
    data = await db.fetch(1)
    return {'id': data[0], 'userid': data[1], 'key': data[2]}

async def is_user(id, key):
    await db.query(f'SELECT * FROM users WHERE id="{id}" AND key="{key}"')
    return await db.fetch(1)

async def delete_user(id):
    await db.query(f'DELETE FROM users WHERE id="{id}"')


async def create_notify(key, user, message):
    await db.query(f'INSERT INTO notifies(key, user, message) VALUES("{key}", "{user}", "{message}")')
    await db.query(f'SELECT * FROM notifies WHERE id=(SELECT MAX(id) FROM notifies)')
    data = await db.fetch(1)

    user_data = await is_user(user, key)
    key_data = await is_key(key)
    send(key_data[2] + ': ' + data[3], user_data[1])

    return {'id': data[0], 'userid': data[1], 'key': data[2], 'message': data[3]}

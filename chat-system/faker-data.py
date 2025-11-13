"""
Skript pro generování demo SQL dat pro Discord-like schéma.

Vygeneruje INSERT příkazy pro následující tabulky v pořádku respektujícím FK:
users, servers, server_members, roles, member_roles, channels, messages,
direct_messages, reactions, invites

Výstupní soubor: scripts/discord_demo_data.sql
"""
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Reproducibilita
SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# Počty položek (rozumné defaulty, upravitelné)
NUM_USERS = 60
NUM_SERVERS = 12
AVG_MEMBERS_PER_SERVER = 20
NUM_ROLES_PER_SERVER = 6
NUM_CHANNELS_PER_SERVER = 8
NUM_MESSAGES = 400
NUM_DIRECT_MESSAGES = 120
NUM_REACTIONS = 300
NUM_INVITES = 30

def random_datetime_within_year():
    start = datetime.now() - timedelta(days=365)
    end = datetime.now()
    delta = end - start
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=rand_seconds)).strftime('%Y-%m-%d %H:%M:%S')

sql_lines = []

def sql_val(v):
    # Format value for SQL: None -> NULL, strings quoted, ints left as-is
    if v is None:
        return 'NULL'
    if isinstance(v, (int, float)):
        return str(v)
    # escape single quotes
    s = str(v).replace("'", "''")
    return f"'{s}'"

def insert_lines(table, columns, values_list):
    sql_lines.append(f"-- {table}")
    for values in values_list:
        vals = ', '.join(sql_val(v) for v in values)
        col_str = ', '.join(columns)
        sql_lines.append(f"INSERT INTO {table} ({col_str}) VALUES ({vals});")
    sql_lines.append("")

# ---------- users ----------
users = []
for i in range(1, NUM_USERS + 1):
    username = fake.user_name()
    # ensure uniqueness by appending index if collision
    username = f"{username}{i}"
    email = f"{username}@{fake.free_email_domain()}"
    avatar_url = f"https://example.com/avatars/{i}.png"
    created_at = random_datetime_within_year()
    status = random.choice(['Online', 'Offline', 'Idle', 'Do not disturb'])
    users.append((i, username[:50], email[:100], avatar_url, created_at, status))

# ---------- servers ----------
servers = []
for i in range(1, NUM_SERVERS + 1):
    name = fake.company()[:100]
    icon_url = f"https://example.com/icons/server_{i}.png"
    owner_id = random.choice(users)[0]
    created_at = random_datetime_within_year()
    servers.append((i, name, icon_url, owner_id, created_at))

# ---------- server_members ----------
server_members = []
member_id = 1
server_member_map = {}  # (server_id) -> list of member ids
for server in servers:
    sid = server[0]
    members = set()
    num_members = max(5, min(NUM_USERS, int(random.gauss(AVG_MEMBERS_PER_SERVER, 5))))
    # pick unique users per server
    user_ids = random.sample([u[0] for u in users], k=min(num_members, len(users)))
    server_member_map[sid] = []
    for uid in user_ids:
        joined_at = random_datetime_within_year()
        nickname = fake.first_name() if random.random() < 0.5 else None
        server_members.append((member_id, uid, sid, joined_at, nickname[:50] if nickname else None))
        server_member_map[sid].append(member_id)
        member_id += 1

# ---------- roles ----------
roles = []
role_id = 1
server_roles_map = {}
for server in servers:
    sid = server[0]
    server_roles_map[sid] = []
    for pos in range(1, NUM_ROLES_PER_SERVER + 1):
        name = fake.word().capitalize()[:50]
        color = f"#{random.randint(0,0xFFFFFF):06x}"
        permissions = ''
        roles.append((role_id, sid, name, color, permissions, pos))
        server_roles_map[sid].append(role_id)
        role_id += 1

# ---------- member_roles ----------
member_roles = []
mr_id = 1
for sid, member_ids in server_member_map.items():
    available_roles = server_roles_map.get(sid, [])
    for mid in member_ids:
        # assign 0..3 roles randomly
        for rid in random.sample(available_roles, k=min(len(available_roles), random.randint(0,3))):
            member_roles.append((mr_id, mid, rid))
            mr_id += 1

# ---------- channels ----------
channels = []
channel_id = 1
channel_types = ['Text', 'Voice', 'Announcement']
server_channels_map = {}
for server in servers:
    sid = server[0]
    server_channels_map[sid] = []
    for pos in range(1, NUM_CHANNELS_PER_SERVER + 1):
        name = fake.word()[:100]
        ctype = random.choice(channel_types)
        created_at = random_datetime_within_year()
        channels.append((channel_id, sid, name, ctype, pos, created_at))
        server_channels_map[sid].append(channel_id)
        channel_id += 1

# ---------- messages ----------
messages = []
message_id = 1
for _ in range(NUM_MESSAGES):
    # pick a random server, then a random text channel in it
    server = random.choice(servers)
    sid = server[0]
    ch_list = server_channels_map.get(sid) or []
    if not ch_list:
        continue
    cid = random.choice(ch_list)
    author_id = random.choice(users)[0]
    content = fake.sentence(nb_words=random.randint(3, 20))
    created_at = random_datetime_within_year()
    messages.append((message_id, cid, author_id, content, created_at))
    message_id += 1

# ---------- direct_messages ----------
direct_messages = []
dm_id = 1
for _ in range(NUM_DIRECT_MESSAGES):
    sender = random.choice(users)[0]
    receiver = random.choice(users)[0]
    while receiver == sender:
        receiver = random.choice(users)[0]
    content = fake.sentence(nb_words=random.randint(1, 30))
    created_at = random_datetime_within_year()
    direct_messages.append((dm_id, sender, receiver, content, created_at))
    dm_id += 1

# ---------- reactions ----------
reactions = []
react_id = 1
emoji_choices = ['😀', '🎉', '👍', '❤️', '😮', '😢']
for _ in range(NUM_REACTIONS):
    if not messages:
        break
    mid = random.choice(messages)[0]
    uid = random.choice(users)[0]
    emoji = random.choice(emoji_choices)
    created_at = random_datetime_within_year()
    reactions.append((react_id, mid, uid, emoji, created_at))
    react_id += 1

# ---------- invites ----------
invites = []
inv_id = 1
for _ in range(NUM_INVITES):
    server = random.choice(servers)[0]
    chan = None
    # 50% chance invite is bound to a channel
    if random.random() < 0.5 and server_channels_map.get(server):
        chan = random.choice(server_channels_map[server])
    inviter = random.choice(users)[0]
    expires_at = None if random.random() < 0.3 else random_datetime_within_year()
    max_uses = None if random.random() < 0.4 else random.randint(1, 100)
    uses = 0 if max_uses is None else random.randint(0, max_uses)
    invites.append((inv_id, server, chan, inviter, expires_at, max_uses, uses))
    inv_id += 1

# Insert in FK-correct order
insert_lines('users', ['id', 'username', 'email', 'avatar_url', 'created_at', 'status'], users)
insert_lines('servers', ['id', 'name', 'icon_url', 'owner_id', 'created_at'], servers)
insert_lines('server_members', ['id', 'user_id', 'server_id', 'joined_at', 'nickname'], server_members)
insert_lines('roles', ['id', 'server_id', 'name', 'color', 'permissions', 'position'], roles)
insert_lines('member_roles', ['id', 'member_id', 'role_id'], member_roles)
insert_lines('channels', ['id', 'server_id', 'name', 'type', 'position', 'created_at'], channels)
insert_lines('messages', ['id', 'channel_id', 'author_id', 'content', 'created_at'], messages)
insert_lines('direct_messages', ['id', 'sender_id', 'receiver_id', 'content', 'created_at'], direct_messages)
insert_lines('reactions', ['id', 'message_id', 'user_id', 'emoji', 'created_at'], reactions)
insert_lines('invites', ['id', 'server_id', 'channel_id', 'inviter_id', 'expires_at', 'max_uses', 'uses'], invites)

# Uložení do souboru
out_dir = os.path.join(os.path.dirname(__file__) or '.', '')
sql_dump_path = os.path.join(out_dir, 'discord_demo_data.sql')
with open(sql_dump_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

print(f"Wrote {len(sql_lines)} SQL lines to {sql_dump_path}")

sql_dump_path

from faker import Faker
import pandas as pd
import mariadb
from Seeders.LensSeeder import LensSeeder
from Seeders.ContentSeeder import ContentSeeder
faker = Faker(['en_US','ja_JP','id_ID'])

ENTITY_TABLE_ROWS = 30
FOREIGN_TABLE_ROWS = 50
class UserSeeder:
    def __init__(self, cursor):
        self.cursor = cursor
        self.lens_seeder = LensSeeder(cursor)
        self.content_seeder = ContentSeeder(cursor)
        self.user_count = 0

    def run(self):
        # 1. Seed levels first (needed for Pengguna FK)
        self.seed_level_table()
        # 2. Seed users and get user_df
        user_df = self.seed_user_table()
        self.user_df = user_df
        # 3. Seed premium for users
        self.seed_premium_table(user_df)
        # 4. Seed room chats and get room_chat_df
        room_chat_df = self.seed_room_chat_table()
        self.room_chat_df = room_chat_df
        # 5. Seed tergabung_dalam (user-room join table)
        tergabung_dalam_df= self.seed_tergabung_dalam_table(user_df, room_chat_df)
        # 6. Seed content (and all child tables) using ContentSeeder
        self.content_seeder.seed_content_table(tergabung_dalam_df,self.lens_seeder.lens_count)
        print("UserSeeder run complete.")

    def seed_user_table(self):
        print("Seeding users...")
        users = []
        for i in range(ENTITY_TABLE_ROWS):
            user = {
                # 'id_user' removed, let DB auto-increment
                'id_level': faker.random_int(min=0, max=3),
                'email': faker.email(),
                'username': faker.user_name(),
                'no_telp': faker.phone_number(),
                'tanggal_lahir': faker.date_of_birth(minimum_age=12, maximum_age=60),
                'tanggal_pembuatan': faker.date_between(start_date='-3y', end_date='today'),
                'password': faker.password(),
            }
            users.append(user)
        # Convert to DataFrame
        user_df =  pd.DataFrame(users)
        # Insert into the database and get generated id_user
        id_users = []
        for idx, row in user_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Pengguna (id_level, email, username, no_telp, tanggal_lahir, tanggal_pembuatan, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row['id_level'],
                    row['email'],
                    row['username'],
                    row['no_telp'],
                    row['tanggal_lahir'],
                    row['tanggal_pembuatan'],
                    row['password'],
                )
            )
            id_users.append(self.cursor.lastrowid)
        user_df['id_user'] = id_users
        self.lens_seeder.seed_lens_table(user_df)
        self.user_count = len(users)
        self.seed_papmap_table(user_df)
        self.seed_berteman_table(user_df)
        return user_df
    
    def seed_level_table(self):
        print("Seeding level...")
        levels = [{"id_level": 0, "nama_level": "Not Rated", "upah":0,"minimum_lensa":0},
                 {"id_level": 1, "nama_level": "Bronze", "upah":1000000,"minimum_lensa":10},
                 {"id_level": 2, "nama_level": "Silver", "upah":2000000,"minimum_lensa":20},
                 {"id_level": 3, "nama_level": "Gold", "upah":3000000,"minimum_lensa":30},]
        # Convert to DataFrame
        level_df =  pd.DataFrame(levels)
        # Insert into the database
        for _, row in level_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Level (id_level, nama_level, upah, minimum_lensa)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row['id_level'],
                    row['nama_level'],
                    row['upah'],
                    row['minimum_lensa'],
                )
            )

    def seed_papmap_table(self, user_table: pd.DataFrame):
        print("Seeding papmap...")
        papmap = []
        for _, i in user_table.iterrows():
            n_entries = faker.random_int(min=2, max=5)
            timestamps = []
            for _ in range(n_entries):
                date = faker.date_between(start_date=i['tanggal_pembuatan'], end_date='today')
                start_time = faker.date_time_between(start_date=i['tanggal_pembuatan'], end_date='now')
                end_time = faker.date_time_between(start_date=start_time, end_date=date)
                if start_time > end_time:
                    start_time, end_time = end_time, start_time
                timestamp = {
                    "date": date,
                    'start_time': start_time,
                    'end_time': end_time,
                }
                valid = True
                for stamp in timestamps:
                    if stamp['date'] == date:
                        if start_time > stamp['start_time'] and start_time < stamp['end_time']:
                            valid = False
                if valid:
                    timestamps.append(timestamp)
                    papmap_entry = {
                        'waktu_mulai': start_time,
                        'waktu_akhir': end_time,
                        'id_user': i['id_user'],
                        'longitude': float(faker.longitude()),
                        'latitude': float(faker.latitude()),
                        'status': faker.random_element(elements=["public", "private"]),
                    }
                    papmap.append(papmap_entry)
        # Convert to DataFrame
        papmap_df = pd.DataFrame(papmap)
        # Insert into the database
        for _, row in papmap_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO PapMap (waktu_mulai, waktu_akhir, id_user, longitude, latitude, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row['waktu_mulai'],
                    row['waktu_akhir'],
                    row['id_user'],
                    row['longitude'],
                    row['latitude'],
                    row['status'],
                )
            )

    def seed_berteman_table(self, user_table: pd.DataFrame):
        print("Seeding berteman...")
        berteman = []
        user_ids = user_table['id_user'].tolist()
        user_creation_dates = pd.Series(user_table['tanggal_pembuatan'].values, index=user_table['id_user']).to_dict()
        for _, i in user_table.iterrows():
            n_friends = faker.random_int(min=3, max=6)
            possible_friends = [uid for uid in user_ids if uid != i['id_user']]
            n_friends = min(n_friends, len(possible_friends))
            if not possible_friends:
                continue
            chosen_friends_ids = faker.random_elements(elements=possible_friends, length=n_friends, unique=True)
            for friend_id in chosen_friends_ids:
                user1_id = i['id_user']
                user2_id = friend_id
                user1_creation_date = user_creation_dates[user1_id]
                min_start_date_berteman = user1_creation_date
                friendship_start_date = faker.date_between(start_date=min_start_date_berteman, end_date='today')
                streak = faker.random_int(min=0, max=100)
                # Only insert one direction (user1 < user2) to match PK
                if user1_id < user2_id:
                    berteman.append({
                        'id_user1': user1_id,
                        'id_user2': user2_id,
                        'streak': streak,
                        'tanggal_mulai': friendship_start_date
                    })
        # Convert to DataFrame
        berteman_df = pd.DataFrame(berteman)
        # Insert into the database
        for _, row in berteman_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Berteman (id_user1, id_user2, streak, tanggal_mulai)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row['id_user1'],
                    row['id_user2'],
                    row['streak'],
                    row['tanggal_mulai'],
                )
            )

    def seed_premium_table(self, user_table: pd.DataFrame):
        print("Seeding premium...")
        premium = []
        for _, i in user_table.iterrows():
            n_entries = faker.random_int(min=0, max=3)
            current_start = i['tanggal_pembuatan']
            for j in range(n_entries):
                start = faker.date_between(start_date=current_start, end_date='today')
                end = faker.date_between(start_date=start, end_date='today')
                premium_entry = {
                    # 'subscription_number' removed, let DB auto-increment
                    'id_user': i['id_user'],
                    'tanggal_subscribe': start,
                    'tanggal_expired': end,
                    'status': faker.random_element(elements=["active", "inactive"]),
                }
                premium.append(premium_entry)
                current_start = end
        # Convert to DataFrame
        premium_df = pd.DataFrame(premium)
        # Insert into the database
        for _, row in premium_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Premium (id_user, tanggal_subscribe, tanggal_expired, status)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row['id_user'],
                    row['tanggal_subscribe'],
                    row['tanggal_expired'],
                    row['status'],
                )
            )

    def seed_room_chat_table(self):
        print("Seeding room chat...")
        room_chat = []
        for _ in range(ENTITY_TABLE_ROWS):
            room = {
                'nama_room_chat': faker.text(max_nb_chars=20),
                'tanggal_pembuatan': faker.date_between(start_date='-3y', end_date='today'),
            }
            room_chat.append(room)
        # Convert to DataFrame
        room_chat_df = pd.DataFrame(room_chat)
        id_room_chats = []
        for _, row in room_chat_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO RoomChat (nama_room_chat, tanggal_pembuatan)
                VALUES (%s, %s)
                """,
                (
                    row['nama_room_chat'],
                    row['tanggal_pembuatan'],
                )
            )
            id_room_chats.append(self.cursor.lastrowid)
        room_chat_df['id_room_chat'] = id_room_chats
        return room_chat_df

    def seed_tergabung_dalam_table(self, user_df, room_chat_df):
        print("Seeding tergabung dalam...")
        tergabung_dalam = []
        for _, i in user_df.iterrows():
            n_rooms = faker.random_int(min=1, max=5)
            possible_rooms = room_chat_df[room_chat_df['tanggal_pembuatan'] >= i['tanggal_pembuatan']]
            if possible_rooms.empty:
                continue
            chosen_room_ids = faker.random_elements(elements=possible_rooms.index.tolist(), length=min(n_rooms, len(possible_rooms)), unique=True)
            for room_idx in chosen_room_ids:
                room = possible_rooms.loc[room_idx]
                tanggal_bergabung = faker.date_between(start_date=room['tanggal_pembuatan'], end_date='today')
                tergabung_dalam.append({
                    'id_user': i['id_user'],
                    'id_room_chat': room_idx + 1,  # Assuming auto-increment starts at 1
                    'tanggal_bergabung': tanggal_bergabung,
                })
        # Convert to DataFrame
        tergabung_dalam_df = pd.DataFrame(tergabung_dalam)
        # Insert into the database
        for _, row in tergabung_dalam_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO TergabungDalam (id_user, id_room_chat, tanggal_bergabung)
                VALUES (%s, %s, %s)
                """,
                (
                    row['id_user'],
                    row['id_room_chat'],
                    row['tanggal_bergabung'],
                )
            )
        return tergabung_dalam_df
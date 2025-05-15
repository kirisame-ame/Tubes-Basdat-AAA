from faker import Faker
import pandas as pd
from LensSeeder import LensSeeder
faker = Faker(['en_US','ja_JP','id_ID'])

ENTITY_TABLE_ROWS = 30
FOREIGN_TABLE_ROWS = 50
class UserSeeder:
    def __init__(self, db):
        self.db = db
        self.lens_seeder = LensSeeder(db)
        self.user_count = 0

    def run(self):
        # Example user data
        self.seed_user_table()
        self.seed_level_table()
    
    def seed_user_table(self):
        print("Seeding users...")
        users = []
        for i in range(ENTITY_TABLE_ROWS):
            user = {
                'id-user': i+1,
                'id-level': faker.random_int(min=0, max=3),
                'email': faker.email(),
                'username': faker.user_name(),
                'no-telp': faker.phone_number(),
                'tanggal-lahir': faker.date_of_birth(minimum_age=12, maximum_age=60),
                'tanggal-pembuatan': faker.date_between(start_date='-3y', end_date='today'),
                'password': faker.password(),
            }
            users.append(user)
        # Convert to DataFrame
        user_df =  pd.DataFrame(users)
        self.lens_seeder.seed_lens_table(user_df)
        self.user_count = len(users)
        self.seed_papmap_table(user_df)
        self.seed_berteman_table(user_df)
        # Insert into the database
    
    def seed_level_table(self):
        print("Seeding level...")
        levels = [{"id-level": 0, "nama-level": "Not Rated", "upah":0,"minimum-lensa":0},
                 {"id-level": 1, "nama-level": "Bronze", "upah":1000000,"minimum-lensa":10},
                 {"id-level": 2, "nama-level": "Silver", "upah":2000000,"minimum-lensa":20},
                 {"id-level": 3, "nama-level": "Gold", "upah":3000000,"minimum-lensa":30},]
        # Convert to DataFrame
        level_df =  pd.DataFrame(levels)
        # Insert into the database

    def seed_papmap_table(self,user_table:pd.DataFrame):
        print("Seeding papmap...")
        papmap = []
        for i in user_table:
            n_entries = faker.random_int(min=1, max=5)
            timestamps = []
            for j in range(n_entries):
                date = faker.date_between(start_date=i['tanggal-pembuatan'], end_date='today')
                start_time = faker.date_time_between(start_date=date, end_date=date)
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
                    # Don't allow overlapping timestamps
                    if stamp['date'] == date:
                        if start_time > stamp['start_time'] and start_time < stamp['end_time']:
                           valid = False
                if valid:
                    timestamps.append(timestamp)
                    papmap_entry = {
                        'waktu_mulai': start_time,
                        'waktu_akhir': end_time,
                        'id-user': i['id-user'],
                        'longitude': faker.longitude(),
                        'latitude': faker.latitude(),
                        'status': faker.random_element(elements=["public", "private"]),
                    }
                    papmap.append(papmap_entry)
                
        # Convert to DataFrame
        papmap_df =  pd.DataFrame(papmap)
        # Insert into the database

    def seed_berteman_table(self,user_table:pd.DataFrame):
        print("Seeding berteman...")
        berteman = []
        for i in user_table:
            n_friends = faker.random_int(min=1, max=5)
            for j in range(n_friends):
                friend = {
                    'id-user': i['id-user'],
                    'id-user-teman': faker.random_int(min=1, max=ENTITY_TABLE_ROWS),
                }
                friend_mirror = {
                    'id-user': friend['id-user-teman'],
                    'id-user-teman': friend['id-user'],
                }
                berteman.append(friend)
                berteman.append(friend_mirror)
        # Remove duplicates
        berteman = [dict(t) for t in {tuple(d.items()) for d in berteman}]
        # Remove self-friendships
        berteman = [friend for friend in berteman if friend['id-user'] != friend['id-user-teman']]
        # Convert to DataFrame
        berteman_df =  pd.DataFrame(berteman)
        # Insert into the database

    def seed_premium_table(self,user_table:pd.DataFrame):
        print("Seeding premium...")
        premium = []
        for i in user_table:
            subscription ={
                #WIP
            }
        # Convert to DataFrame
        premium_df =  pd.DataFrame(premium)
        # Insert into the database
    def seed_room_chat_table(self):
        print("Seeding room chat...")
        room_chat = []
        for j in range(ENTITY_TABLE_ROWS):
            room = {
                'id-room-chat': j,
                'nama-room-chat': faker.text(max_nb_chars=20),
                'tanggal-pembuatan': faker.date_between(start_date='-3y', end_date='today'),
            }
            room_chat.append(room)
        # Convert to DataFrame
        room_chat_df =  pd.DataFrame(room_chat)
        # Insert into the database
    def seed_tergabung_dalam_table(self,user_df,room_chat_df):
        print("Seeding tergabung dalam...")
        tergabung_dalam = []
        for i in user_df:
            n_rooms = faker.random_int(min=1, max=5)
            for j in range(n_rooms):
                # 5 tries to find a valid room
                for k in range(5):
                    room_id = faker.random_int(min=0, max=room_chat_df.shape[0]-1)
                    if room_chat_df.loc(room_id)['tanggal-pembuatan'] < i['tanggal-pembuatan']:
                        continue
                    else:
                        room = {
                            'id-user': i['id-user'],
                            'id-room-chat': room_id,
                            'tanggal-bergabung': faker.date_between(start_date=room_chat_df.loc(room_id)['tanggal-pembuatan'], 
                                                                    end_date='today'),
                        }
                        tergabung_dalam.append(room)
                        break
        # Convert to DataFrame
        tergabung_dalam_df =  pd.DataFrame(tergabung_dalam)
        # Insert into the database
from faker import Faker
import pandas as pd
import mariadb
ENTITY_TABLE_ROWS = 50
FOREIGN_TABLE_ROWS = 100
RANDOM_STATE = 34

faker = Faker(['en_US','ja_JP','id_ID'])
Faker.seed(RANDOM_STATE)

class LensSeeder:
    def __init__(self, cursor):
        self.cursor = cursor
        self.lens_count = 0
        self.lens_id_map = []  # To map DataFrame index to DB id_lens

    def seed_lens_table(self, user_table: pd.DataFrame):
        print("Seeding lenses...")
        lenses = []
        for _, i in user_table.iterrows():
            if i["id_level"] == 0:
                n_lenses = faker.random_int(min=1, max=9)
            elif i['id_level'] == 1:
                n_lenses = faker.random_int(min=10, max=19)
            elif i['id_level'] == 2:
                n_lenses = faker.random_int(min=20, max=29)
            elif i['id_level'] == 3:
                n_lenses = faker.random_int(min=30, max=50)
            for _ in range(n_lenses):
                lens = {
                    'id_user': i['id_user'],
                    'nama_lens': faker.word(),
                    'tanggal_rilis': faker.date_between(start_date=i['tanggal_pembuatan'], end_date='today'),
                }
                lenses.append(lens)
        lens_df = pd.DataFrame(lenses)
        self.lens_count = len(lenses)
        self.lens_id_map = []
        # Insert into the database and collect DB-generated id_lens
        for _, row in lens_df.iterrows():
            sql = "INSERT INTO Lens (id_user, nama_lens, tanggal_rilis) VALUES (%s, %s, %s)"
            val = (row['id_user'], row['nama_lens'], row['tanggal_rilis'])
            self.cursor.execute(sql, val)
        self.seed_tipe_lensa_table()
        return lens_df

    def seed_tipe_lensa_table(self):
        print("Seeding tipe_lensa...")
        types = ["face", "background", "both", "none"]
        tipe_lensa = []
        for id_lens in self.lens_id_map:
            tipe = {
                'id_lens': id_lens,
                'tipe_lensa': faker.random_element(elements=types),
            }
            tipe_lensa.append(tipe)
        tipe_lensa_df = pd.DataFrame(tipe_lensa)
        for _, row in tipe_lensa_df.iterrows():
            sql = "INSERT INTO TipeLensa (id_lens, tipe_lensa) VALUES (%s, %s)"
            val = (row['id_lens'], row['tipe_lensa'])
            self.cursor.execute(sql, val)
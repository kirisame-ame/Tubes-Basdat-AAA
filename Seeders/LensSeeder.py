from faker import Faker
import pandas as pd
ENTITY_TABLE_ROWS = 30
FOREIGN_TABLE_ROWS = 50
RANDOM_STATE = 34

faker = Faker(['en_US','ja_JP','id_ID'])
Faker.seed(RANDOM_STATE)

class LensSeeder:
    def __init__(self, db):
        self.db = db
        self.lens_count = 0

    def seed_lens_table(self,user_table:pd.DataFrame):
        print("Seeding lenses...")
        lenses = []
        for i in user_table:
            if i["id-level"]==0:
                n_lenses = faker.random_int(min=1, max=9)
            elif i['id-level']==1:
                n_lenses = faker.random_int(min=10, max=19)
            elif i['id-level']==2:
                n_lenses = faker.random_int(min=20, max=29)
            elif i['id-level']==3:
                n_lenses = faker.random_int(min=30, max=FOREIGN_TABLE_ROWS)
            for j in range(n_lenses):
                lens = {
                    'id-lens': len(lenses) + 1,
                    'id-user': i['id-user'],
                    'nama-lens': faker.word(),
                    'tanggal-rilis': faker.date_between(start_date=i['tanggal-pembuatan'], end_date='today'),
                }
                lenses.append(lens)
        # Convert to DataFrame
        lens_df =  pd.DataFrame(lenses)
        self.lens_count = len(lenses)
        # Insert into the database

        # create tipe_lensa table
        self.seed_tipe_lensa_table()
        
    def seed_tipe_lensa_table(self):
        print("Seeding tipe_lensa...")
        types = ["face","background","both","none"]
        tipe_lensa = []
        for i in range(self.lens_count):
            tipe = {
                'id-lens': i+1,
                'tipe-lensa': faker.random_element(elements=types),
            }
            tipe_lensa.append(tipe)
        # Convert to DataFrame
        tipe_lensa_df =  pd.DataFrame(tipe_lensa)
        # Insert into the database
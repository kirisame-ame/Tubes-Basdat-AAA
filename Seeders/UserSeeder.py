from faker import Faker
import pandas as pd
from LensSeeder import LensSeeder
faker = Faker(['en_US','ja_JP','id_ID'])

ENTITY_TABLE_ROWS = 30
FOREIGN_TABLE_ROWS = 50
class UserSeeder:
    def __init__(self, db):
        self.db = db

    def run(self):
        # Example user data
        user_table = self.seed_user_table()

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
            LensSeeder(self.db).seed_lens_table(user_table=pd.DataFrame(users))
        # Convert to DataFrame
        return pd.DataFrame(users)
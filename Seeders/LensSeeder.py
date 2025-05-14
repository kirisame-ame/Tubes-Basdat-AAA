from faker import Faker
import pandas as pd
faker = Faker(['en_US','ja_JP','id_ID'])
ENTITY_TABLE_ROWS = 30
FOREIGN_TABLE_ROWS = 50
class LensSeeder:
    def __init__(self, db):
        self.db = db

    def seed_lens_table(user_table:pd.DataFrame)-> pd.DataFrame:
        print("Seeding lenses...")
        lenses = []
        
        # Convert to DataFrame
        return pd.DataFrame(lenses)
from UserSeeder import UserSeeder
from ContentSeeder import ContentSeeder
import dotenv
import os
import pandas as pd
class PapchatSeeder:
    def __init__(self, host=None, user=None, password=None, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def run(self):
        
        # Database connection (replace with actual connection code)
        
        # Initialize seeders
        user_seeder = UserSeeder(self.db_name)
        content_seeder = ContentSeeder(self.db_name)
        
        # Run seeders
        user_seeder.run()
        # replace with actual tergabung_dalam_table
        content_seeder.seed_content_table(user_seeder.user_df)
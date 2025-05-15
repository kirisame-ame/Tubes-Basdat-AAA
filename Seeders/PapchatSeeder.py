from UserSeeder import UserSeeder
from ContentSeeder import ContentSeeder
import mariadb
import sys
import pandas as pd
class PapchatSeeder:
    def __init__(self, host=None, user=None, password=None, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        try:
            self.conn = mariadb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    def run(self):
        
        # Database connection (replace with actual connection code)
        
        # Initialize seeders
        user_seeder = UserSeeder(self.cursor)
        content_seeder = ContentSeeder(self.cursor)
        
        # Run seeders
        user_seeder.run()
        # replace with actual tergabung_dalam_table
        content_seeder.seed_content_table(user_seeder.user_df)
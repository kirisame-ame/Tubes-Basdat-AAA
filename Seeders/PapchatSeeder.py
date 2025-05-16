from Seeders.UserSeeder import UserSeeder
import mariadb
import sys
import pandas as pd
class PapchatSeeder:
    def __init__(self, host=None, user=None, password=None, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        
    def run(self,refresh=False):
        try:
            self.conn = mariadb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                # database=self.db_name
            )
            self.cursor = self.conn.cursor()
            if refresh:
                with open("Database/schema.sql", "r") as f:
                    schema_sql = f.read()
                for statement in schema_sql.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        self.cursor.execute(stmt)
                self.conn.commit()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        # Initialize and run the full user seeder (which now seeds everything, including content)
        user_seeder = UserSeeder(self.cursor)
        user_seeder.run()
        self.conn.commit()
        # No need to call ContentSeeder separately, as it's already called inside UserSeeder
        print("PapchatSeeder run complete.")

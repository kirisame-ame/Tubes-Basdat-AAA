from Seeders.PapchatSeeder import PapchatSeeder
import os
import mariadb
from dotenv import load_dotenv
if __name__ == "__main__":
    load_dotenv()
    seeder = PapchatSeeder(os.getenv("DB_HOST"),
                           os.getenv("DB_USER"),
                           os.getenv("DB_PASSWORD"),
                           os.getenv("DB_NAME"))
    seeder.run()
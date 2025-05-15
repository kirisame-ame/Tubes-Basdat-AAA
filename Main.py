from Seeders.PapchatSeeder import PapchatSeeder
import dotenv
if __name__ == "__main__":
    dotenv.load_dotenv()
    seeder = PapchatSeeder(dotenv.get("DB_HOST"),
                           dotenv.get("DB_USER"),
                           dotenv.get("DB_PASSWORD"),
                           dotenv.get("DB_NAME"))
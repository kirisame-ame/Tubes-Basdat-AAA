from faker import Faker
import pandas as pd
faker = Faker(['en_US','ja_JP','id_ID'])

FOREIGN_TABLE_ROWS = 50
class ContentSeeder:
    # TO DO: call other seeds inside func
    
    def __init__(self, db):
        self.db = db
        self.content_count = 0
        
    def seed_content_table(self, tergabung_dalam_table:pd.DataFrame):
        print("Seeding content...")
        contents = []
        while len(contents) < 50: #minimum content is 50
            for _, i in tergabung_dalam_table.iterrows():
                if len(contents) >= 50:
                    break  # stop if >= 50
                
                n_contents = faker.random_int(min=0, max=5)
                for j in range(n_contents):
                    if len(contents) >= 50:
                        break
                    
                    date = faker.date_between(start_date=i['tanggal-pembuatan'], end_date='today')
                    tipe = faker.random_element(['pap', 'chat'])
                    saved = faker.pybool()
                    content = {
                        'urutan-pengiriman': j,
                        'id-room-chat': i['id-room-chat'],
                        'id-user': i['id-user'],
                        'waktu-pembuatan': date,
                        'tipe-konten': tipe,
                        'disimpan': saved
                    }
                    contents.append(content)
        # Convert to DataFrame
        content_df = pd.DataFrame(contents)
        self.content_count = len(contents)
        # call other seeder
        self.seed_chat_table(content_df)
        self.seed_pap_table(content_df)
        # Insert into the database
    
    def seed_chat_table(self, konten_table:pd.DataFrame):
        print("Seeding chat...")
        chats = []
        for _,i in konten_table.iterrows():
            if i['tipe-konten'] == "chat":
                chat = {
                    'urutan-pengiriman' : i['urutan-pengiriman'],
                    'id-room-chat' : i['id-room-chat'],
                    'id-user' : i['id-user'],
                    'isi-pesan' : faker.text()
                }
                chats.append(chat)
        # Convert to DataFrame
        chat_df = pd.DataFrame(chats)
        # Insert into the database
    
    def seed_pap_table(self, konten_table: pd.DataFrame, lens_table: pd.DataFrame):
        print("Seeding pap...")
        lens_ids = lens_table['id-lens'].tolist()
        paps = []
        for _,i in konten_table.iterrows():
            if i['tipe-konten'] == "pap":
                type = faker.random_element(['video', 'foto'])
                if type == 'video':
                    duration = faker.random_int(min = 1, max = 60)
                else: #photo
                    duration = None
                random_idx = faker.random_int(min=0, max=len(lens_ids)-1)
                id_lens = lens_ids[random_idx]
                pap = {
                    'urutan-pengiriman' : i['urutan-pengiriman'],
                    'id-room-chat' : i['id-room-chat'],
                    'id-user' : i['id-user'],
                    'id-lens' : id_lens,
                    'tipe-pap': type,
                    'durasi'  :duration
                }
                paps.append(pap)
        # Convert to DataFrame
        pap_df = pd.DataFrame(paps)
        # call other seeder
        self.seed_add_on_table(pap_df)
        # Insert into the database
        
    def seed_add_on_table(self, pap_table:pd.DataFrame):
        print("Seeding add on...")
        add_ons = []
        image_height = 3023
        image_width = 4032
        for _, i in pap_table:
            x_start = faker.random_int(min=0, max=image_width)
            x_end = faker.random_int(min=x_start, max=image_width)
            y_start = faker.random_int(min=0, max=image_height)
            y_end = faker.random_int(min=y_start, max=image_height)
            type = faker.random_element(['image', 'caption'])
            add_on = {
                'id-add-on' : len(add_ons) + 1,
                'urutan-pengiriman' : i['urutan-pengiriman'],
                'id-room-chat' : i['id-room-chat'],
                'id-user' : i['id-user'],
                'x-awal' : x_start,
                'x-akhir' : x_end,
                'y-awal' : y_start,
                'y-akhir' : y_end,
                'tipe-add-on': type,
            }
            add_ons.append(add_on)
        # Convert to DataFrame
        add_on_df = pd.DataFrame(add_ons)
        # call other seeder
        self.seed_image_table(add_on_df)
        self.seed_caption_table(add_on_df)
        # Insert into the database

    def seed_caption_table(self, add_on_table: pd.DataFrame):
        print("Seeding caption...")
        captions = []
        fonts = ["Arial", "Helvetica", "Roboto", "Open Sans", "Lato", "Montserrat",
                 "Poppins", "Noto Sans", "Fira Sans"]
        for _,i in add_on_table.iterrows():
            if i['tipe-add-on'] == "caption":
                caption = {
                    'id-add-on' : i['id-add-on'],
                    'font-style' : faker.random_element(fonts),
                    'teks' : faker.text()
                }
                captions.append(caption)
        # Convert to DataFrame
        caption_df = pd.DataFrame(captions)
        # Insert into the database
        
    def seed_image_table(self, add_on_table: pd.DataFrame):
        print("Seeding image...")
        images = []
        for _,i in add_on_table.iterrows():
            if i['tipe-add-on'] == "image":
                image_url = faker.image_url(width=640, height=480)
                image = {
                    'id-add-on' : i['id-add-on'],
                    'nama-image' : image_url
                }
                images.append(image)
        # Convert to DataFrame
        content_df = pd.DataFrame(images)
        # Insert into the database
        
        
    
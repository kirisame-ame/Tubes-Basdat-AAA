from faker import Faker
import pandas as pd
faker = Faker(['en_US','ja_JP','id_ID'])

FOREIGN_TABLE_ROWS = 50
class ContentSeeder:
    # TO DO: call other seeds inside func
    
    def __init__(self, cursor):
        self.cursor = cursor
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
                    
                    date = faker.date_between(start_date=i['tanggal_pembuatan'], end_date='today')
                    tipe = faker.random_element(['pap', 'chat'])
                    saved = faker.pybool()
                    content = {
                        'urutan_pengiriman': j,
                        'id_room_chat': i['id_room_chat'],
                        'id_user': i['id_user'],
                        'waktu-pembuatan': date,
                        'tipe_konten': tipe,
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
        for _, row in content_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Konten (urutan_pengiriman, id_room_chat, id_user, waktu_pengiriman, tipe_konten, disimpan)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row['urutan_pengiriman'],
                    row['id_room_chat'],
                    row['id_user'],
                    row['waktu_pengiriman'],
                    row['tipe_konten'],
                    row['disimpan']
                )
            )
    
    def seed_chat_table(self, konten_table:pd.DataFrame):
        print("Seeding chat...")
        chats = []
        for _,i in konten_table.iterrows():
            if i['tipe_konten'] == "chat":
                chat = {
                    'urutan_pengiriman' : i['urutan_pengiriman'],
                    'id_room_chat' : i['id_room_chat'],
                    'id_user' : i['id_user'],
                    'isi_pesan' : faker.text()
                }
                chats.append(chat)
        # Convert to DataFrame
        chat_df = pd.DataFrame(chats)
        # Insert into the database
        for _, row in chat_df.interrows():
            self.cursor.execute(
                """
                INSERT INTO Chat (urutan_pengiriman, id_room_chat, id_user, isi_pesan)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row['urutan_pengiriman'],
                    row['id_room_chat'],
                    row['id_user'],
                    row['isi_pesan']
                )
            )
    
    def seed_pap_table(self, konten_table: pd.DataFrame, lens_table: pd.DataFrame):
        print("Seeding pap...")
        lens_ids = lens_table['id_lens'].tolist()
        paps = []
        for _,i in konten_table.iterrows():
            if i['tipe_konten'] == "pap":
                type = faker.random_element(['video', 'foto'])
                if type == 'video':
                    duration = faker.random_int(min = 1, max = 60)
                else: #photo
                    duration = None
                random_idx = faker.random_int(min=0, max=len(lens_ids)-1)
                id_lens = lens_ids[random_idx]
                pap = {
                    'urutan_pengiriman' : i['urutan_pengiriman'],
                    'id_room_chat' : i['id_room_chat'],
                    'id_user' : i['id_user'],
                    'id_lens' : id_lens,
                    'tipe_pap': type,
                    'durasi'  :duration
                }
                paps.append(pap)
        # Convert to DataFrame
        pap_df = pd.DataFrame(paps)
        # call other seeder
        self.seed_add_on_table(pap_df)
        # Insert into the database
        for _,row in pap_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Pap (urutan_pengiriman, id_room_chat, id_user, id_lens, tipe_pap, durasi)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row['urutan_pengiriman'],
                    row['id_room_chat'],
                    row['id_user'],
                    row['id_lens'],
                    row['tipe_pap'],
                    row['durasi']
                )
            )
        
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
                'id_add_on' : len(add_ons) + 1,
                'urutan_pengiriman' : i['urutan_pengiriman'],
                'id_room_chat' : i['id_room_chat'],
                'id_user' : i['id_user'],
                'x_awal' : x_start,
                'x_akhir' : x_end,
                'y_awal' : y_start,
                'y_akhir' : y_end,
                'tipe_add_on': type,
            }
            add_ons.append(add_on)
        # Convert to DataFrame
        add_on_df = pd.DataFrame(add_ons)
        # call other seeder
        self.seed_image_table(add_on_df)
        self.seed_caption_table(add_on_df)
        # Insert into the database
        for _, row in add_on_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO AddOn (id_add_on, urutan_pengiriman, id_room_chat, id_user, x_awal, x_akhir, y_awal, y_akhir, tipe_add_on)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row['id_add_on'],
                    row['urutan_pengiriman'],
                    row['id_room_chat'],
                    row['id_user'],
                    row['x_awal'],
                    row['x_akhir'],
                    row['y_awal'],
                    row['y_akhir'],
                    row['tipe_add_on']
                )
            )

    def seed_caption_table(self, add_on_table: pd.DataFrame):
        print("Seeding caption...")
        captions = []
        fonts = ["Arial", "Helvetica", "Roboto", "Open Sans", "Lato", "Montserrat",
                 "Poppins", "Noto Sans", "Fira Sans"]
        for _,i in add_on_table.iterrows():
            if i['tipe_add_on'] == "caption":
                caption = {
                    'id_add_on' : i['id_add_on'],
                    'font-style' : faker.random_element(fonts),
                    'teks' : faker.text()
                }
                captions.append(caption)
        # Convert to DataFrame
        caption_df = pd.DataFrame(captions)
        # Insert into the database
        for _, row in caption_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Caption (id_add_on, font-style, teks)
                VALUES (%s, %s, %s)
                """,
                (
                    row['id_add_on'],
                    row['font-style'],
                    row['teks']
                )
            )
        
    def seed_image_table(self, add_on_table: pd.DataFrame):
        print("Seeding image...")
        images = []
        for _,i in add_on_table.iterrows():
            if i['tipe_add_on'] == "image":
                image_url = faker.image_url(width=640, height=480)
                image = {
                    'id_add_on' : i['id_add_on'],
                    'nama-image' : image_url
                }
                images.append(image)
        # Convert to DataFrame
        content_df = pd.DataFrame(images)
        # Insert into the database
        for _, row in content_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Image (id_add_on, nama-image)
                VALUES (%s, %s)
                """,
                (
                    row['id_add_on'],
                    row['nama-image']
                )
            )
        
        
    
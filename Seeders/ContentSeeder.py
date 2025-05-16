from faker import Faker
import pandas as pd
faker = Faker(['en_US','ja_JP','id_ID'])

FOREIGN_TABLE_ROWS = 100
class ContentSeeder:
    def __init__(self, cursor):
        self.cursor = cursor
        self.content_count = 0
    
    def seed_content_table(self, tergabung_dalam_table: pd.DataFrame, lens_count: int):
        print("Seeding content...")
        contents = []
        while len(contents) < FOREIGN_TABLE_ROWS:
            for _, i in tergabung_dalam_table.iterrows():
                if len(contents) >= FOREIGN_TABLE_ROWS:
                    break
                n_contents = faker.random_int(min=0, max=5)
                for _ in range(n_contents):
                    if len(contents) >= FOREIGN_TABLE_ROWS:
                        break
                    date = faker.date_between(start_date=i['tanggal_bergabung'], end_date='today')
                    tipe = faker.random_element(['pap', 'chat'])
                    saved = faker.pybool()
                    content = {
                        # 'urutan_pengiriman' will be set by DB (AUTO_INCREMENT)
                        'id_room_chat': i['id_room_chat'],
                        'id_user': i['id_user'],
                        'waktu_pengiriman': date,
                        'tipe_konten': tipe,
                        'disimpan': saved
                    }
                    contents.append(content)
        content_df = pd.DataFrame(contents)
        self.content_count = len(contents)
        # Insert into the database and collect urutan_pengiriman
        inserted_rows = []
        for _, row in content_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Konten (id_room_chat, id_user, waktu_pengiriman, tipe_konten, disimpan)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    row['id_room_chat'],
                    row['id_user'],
                    row['waktu_pengiriman'],
                    row['tipe_konten'],
                    row['disimpan']
                )
            )
            inserted_row = row.copy()
            inserted_row['urutan_pengiriman'] = self.cursor.lastrowid
            inserted_rows.append(inserted_row)
        inserted_df = pd.DataFrame(inserted_rows)
        self.seed_chat_table(inserted_df)
        self.seed_pap_table(inserted_df, lens_count)

    def seed_chat_table(self, konten_table: pd.DataFrame):
        print("Seeding chat...")
        chats = []
        for _, i in konten_table.iterrows():
            if i['tipe_konten'] == "chat":
                chat = {
                    'urutan_pengiriman': i['urutan_pengiriman'],
                    'id_room_chat': i['id_room_chat'],
                    'id_user': i['id_user'],
                    'isi_pesan': faker.text()
                }
                chats.append(chat)
        chat_df = pd.DataFrame(chats)
        for _, row in chat_df.iterrows():
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

    def seed_pap_table(self, konten_table: pd.DataFrame, lens_count: int):
        print("Seeding pap...")
        # If lens_table is not provided, skip lens_id assignment
        paps = []
        for _, i in konten_table.iterrows():
            if i['tipe_konten'] == "pap":
                type = faker.random_element(['video', 'foto'])
                duration = faker.random_int(min=1, max=60) if type == 'video' else 0
                id_lens = faker.random_int(min=1, max=lens_count) if lens_count > 0 else None
                pap = {
                    'urutan_pengiriman': i['urutan_pengiriman'],
                    'id_room_chat': i['id_room_chat'],
                    'id_user': i['id_user'],
                    'id_lens': id_lens,
                    'tipe_pap': type,
                    'durasi': duration
                }
                paps.append(pap)
        pap_df = pd.DataFrame(paps)
        self.seed_add_on_table(pap_df)
        for _, row in pap_df.iterrows():
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

    def seed_add_on_table(self, pap_table: pd.DataFrame):
        print("Seeding add on...")
        add_ons = []
        image_height = 3023
        image_width = 4032
        for _, i in pap_table.iterrows():
            x_start = faker.random_int(min=0, max=image_width)
            x_end = faker.random_int(min=x_start, max=image_width)
            y_start = faker.random_int(min=0, max=image_height)
            y_end = faker.random_int(min=y_start, max=image_height)
            type = faker.random_element(['image', 'caption'])
            add_on = {
                # 'id_add_on' will be set by DB (AUTO_INCREMENT)
                'urutan_pengiriman': i['urutan_pengiriman'],
                'id_room_chat': i['id_room_chat'],
                'id_user': i['id_user'],
                'x_awal': x_start,
                'x_akhir': x_end,
                'y_awal': y_start,
                'y_akhir': y_end,
                'tipe_add_on': type,
            }
            add_ons.append(add_on)
        add_on_df = pd.DataFrame(add_ons)
        inserted_rows = []
        for _, row in add_on_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO AddOn (urutan_pengiriman, id_room_chat, id_user, x_awal, x_akhir, y_awal, y_akhir, tipe_add_on)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
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
            inserted_row = row.copy()
            inserted_row['id_add_on'] = self.cursor.lastrowid
            inserted_rows.append(inserted_row)
        inserted_df = pd.DataFrame(inserted_rows)
        self.seed_image_table(inserted_df)
        self.seed_caption_table(inserted_df)

    def seed_caption_table(self, add_on_table: pd.DataFrame):
        print("Seeding caption...")
        captions = []
        fonts = ["Arial", "Helvetica", "Roboto", "Open Sans", "Lato", "Montserrat",
                 "Poppins", "Noto Sans", "Fira Sans"]
        for _, i in add_on_table.iterrows():
            if i['tipe_add_on'] == "caption":
                caption = {
                    'id_add_on': i['id_add_on'],
                    'font_style': faker.random_element(fonts),
                    'teks': faker.text()
                }
                captions.append(caption)
        caption_df = pd.DataFrame(captions)
        for _, row in caption_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Caption (id_add_on, font_style, teks)
                VALUES (%s, %s, %s)
                """,
                (
                    row['id_add_on'],
                    row['font_style'],
                    row['teks']
                )
            )
    
    def seed_image_table(self, add_on_table: pd.DataFrame):
        print("Seeding image...")
        images = []
        for _, i in add_on_table.iterrows():
            if i['tipe_add_on'] == "image":
                image_url = faker.image_url(width=640, height=480)
                image = {
                    'id_add_on': i['id_add_on'],
                    'nama_image': image_url
                }
                images.append(image)
        image_df = pd.DataFrame(images)
        for _, row in image_df.iterrows():
            self.cursor.execute(
                """
                INSERT INTO Image (id_add_on, nama_image)
                VALUES (%s, %s)
                """,
                (
                    row['id_add_on'],
                    row['nama_image']
                )
            )



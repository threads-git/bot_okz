import sqlite3


class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, timeout=5)
        self.cursor = self.connection.cursor()
        # self.create_db()

    def create_db(self):
        try:
            query = ("CREATE TABLE  users("
                     "id INTEGER PRIMARY KEY,"
                     "user_name TEXT,"
                     "user_name_tg TEXT,"
                     "user_login TEXT,"
                     "user_phone TEXT,"
                     "user_direction TEXT,"
                     "telegram_id TEXT,"
                     "user_date_reg);")
            self.cursor.execute(query)
            self.connection.commit()
            print('Таблица создана')
        except sqlite3.Error as Error:
            print('#1 Ошибка при создании:', Error)

    def add_user(self, user_name, user_name_tg, user_login, user_phone, telegram_id, user_date_reg):
        # print('user_name, user_ground_area, user_phone, telegram_id', user_name, user_ground_area, user_phone, telegram_id)
        self.cursor.execute(f"INSERT INTO users (user_name, user_name_tg, user_login, user_phone,  telegram_id, user_date_reg) "
                            f"VALUES (?, ?, ?, ?, ?, ?)", (user_name, user_name_tg, user_login, user_phone, telegram_id, user_date_reg))
        self.connection.commit()
        print('Запись завершена')

    def select_user_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id, ))
        return users.fetchone()

    def check_access_user(self, user_phone):
        check = self.cursor.execute("Select * FROM Users_access Where user_phone = ?" , user_phone)
        return check.fetchone()

    def get_delay(self, telegram_id):
        delay = self.cursor.execute("SELECT count(by15) + count(by30) + count(by60) FROM delay d "
                                    "left join users u ON d.telegram_id=u.telegram_id WHERE  d.telegram_id = ?", (telegram_id, ))
        # delay = self.cursor.execute("SELECT * FROM delay  WHERE  telegram_id = ?", (telegram_id, ))
        return delay.fetchone()

    def get_data_delay(self, telegram_id):
        users = self.cursor.execute("SELECT max(data_delay) FROM delay WHERE telegram_id = ?", (telegram_id, ))
        return users.fetchone()

    def get_all_users(self):
        users = self.cursor.execute("SELECT count(id) FROM users")
        return users.fetchone()

    def add_delay(self, telegram_id, time_delay, data_delay):
        self.cursor.execute(f"INSERT INTO delay (telegram_id, by15, data_delay) "
                            f"VALUES (?, ?, ?)", (telegram_id, 1, data_delay))
        self.connection.commit()


    def get_fio(self, telegram_id):
        fio = self.cursor.execute("SELECT user_name FROM users WHERE telegram_id = ?", (telegram_id,))
        return fio.fetchone()

    def get_tg_id(self, user_name):
        usr = f'{user_name}%'
        fio = self.cursor.execute("SELECT telegram_id FROM users WHERE user_name like ?", (usr,))
        return fio.fetchone()


    def add_madical(self, telegram_id, data_medical):
        self.cursor.execute(f"INSERT INTO delay (telegram_id, medical, data_delay) "
                            f"VALUES (?, ?, ?)", (telegram_id, 1, data_medical))
        self.connection.commit()


    def add_vacation(self, telegram_id, data_vacation):
        self.cursor.execute(f"INSERT INTO delay (telegram_id, vacation, data_delay) "
                            f"VALUES (?, ?, ?)", (telegram_id, 1, data_vacation))
        self.connection.commit()


    def add_absent(self, telegram_id, data_absent, note):
        self.cursor.execute(f"INSERT INTO delay (telegram_id, absent, data_delay, note) "
                            f"VALUES (?, ?, ?, ?)", (telegram_id, 1, data_absent, note))
        self.connection.commit()


    def add_dayoff(self, telegram_id, data_dayoff):
        self.cursor.execute(f"INSERT INTO delay (telegram_id, dayoff, data_delay) "
                            f"VALUES (?, ?, ?)", (telegram_id, 1, data_dayoff))
        self.connection.commit()

    def get_all_user_info(self):
        all_user_info = self.cursor.execute(f"SELECT u.user_name, count(by15), count(by30), count(by60), count(vacation), count(medical) "
                            f"FROM users u left join delay d "
                            f"ON u.telegram_id = d.telegram_id "
                            f"group by(u.user_name) ")
        return all_user_info.fetchall()


    def adm_add_user(self, user_name, user_phone):
        self.cursor.execute(f"INSERT INTO  users_access (user_name, user_phone) "
                            f"VALUES (?, ?)", (user_name, user_phone))
        self.connection.commit()

    def adm_del_user(self, user_name, tgid):
        usr = f'{user_name}%'
        self.cursor.execute(f"delete from users_access where user_name like ?", (usr, ) )
        self.cursor.execute(f"delete from users where user_name like ?", (usr, ) )
        self.cursor.execute(f"delete from delay where telegram_id = ?", tgid)
        self.connection.commit()


    def __del__(self):
        self.cursor.close()
        self.connection.close()
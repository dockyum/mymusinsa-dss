
import mysql.connector
import MySQLdb


class MusinsaPipeline():

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='172.31.36.199',
            user='root',
            passwd='dss',
            database='top',
            charset='utf8',
            use_unicode=True
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS item""")        
        self.curr.execute("""create table IF NOT EXISTS item(
                        item_id text,
                        title text,
                        brand text,
                        o_price text,
                        s_price text,
                        img_link text,
                        link text,
                        )""")
        
    #         self.curr.execute("""create table if not exists size(
    #                         item_id text,
    #                         size_category text,
    #                         size_details text,
    #                         )""")
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        sql = ("""INSERT into item (title, brand, o_price, s_price, img_link, link, item_id)\
VALUES (%s, %s, %s, %s, %s, %s, %s)""")
        query = (
            item["title"],
            item["brand"],
            item["o_price"],
            item["s_price"],
            item["img_link"],
            item["link"],
            item["item_id"],
        )
        self.curr.execute(sql, query)
        
        self.conn.commit()    

from sqlalchemy import *
import pandas as pd


engine = create_engine("mysql://root:dss@3.36.125.234/mymusinsa?charset=utf8")

class MusinsaPipeline():
    def process_item(self, item, spider):
        df = pd.DataFrame([item])
        df.to_sql('item', con=engine, if_exists='append', index=False)
        engine.execute("SELECT * FROM item").fetchall()
        return item
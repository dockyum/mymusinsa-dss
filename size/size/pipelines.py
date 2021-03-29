
import pandas as pd
from itemadapter import ItemAdapter
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql://root:<#SECRET>@<#SECRET>/musinsa?charset=utf8")

class SizePipeline:
    def process_item(self, item, spider):
        df = pd.DataFrame([item])
        df.to_sql('size', con=engine, if_exists='append', index=False)
        engine.execute("SELECT * FROM size").fetchall()
        return item
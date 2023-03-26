import os
from sqlalchemy.orm import sessionmaker
from ic1.base.mbase import Product
from ic1.base.dbase import db_connect
from dotenv import load_dotenv
load_dotenv()

class Ic1Pipeline:
    def __init__(self) -> None:
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        instance = session.query(Product).filter_by(**item).one_or_none()
        if instance:
            return instance


        new_item = Product(
            url = item['url'],
            date = item['date'],
            name = item['name'], 
            processor = item['processor'], 
            core = item['core'], 
            mhz= item['mhz'],
            ram = item['ram'],
            screen = item['screen'],
            price = item['price'],
            rank = float(item['price'])*os.getenv('PRICE') + float(item['ram'])*os.getenv('RAM') + float(item['screen'])*os.getenv('SCREEN') + float(item['core'])*os.getenv('CORE')
            )
        try:
            session.add(new_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
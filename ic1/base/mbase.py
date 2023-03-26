from sqlalchemy import String, Column, Integer, Float
from ic1.base.dbase import Base

class Product(Base):
    __tablename__='ic1'
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True, comment='ID')
    name = Column("name",String, unique=False, comment='Название товара')
    core = Column("core",Integer, unique=False, comment='Количество ядер')
    ram = Column("ram",Integer, unique=False, comment='RAM')
    screen = Column("screen",Float, unique=False, comment='Диагональ экрана')
    price = Column("price",Integer, comment='Цена')
    url = Column("url",String, unique=True, comment='Ссылка на товар')
    rank = Column("rank",Float, comment='Вычисляемый ранг')
    date = Column("date",String, comment='Время загрузки данных')

    def __init__(self, id=None, name=None, core=None, ram=None, screen=None, price=None, url=None, rank=None, load_dttm=None) -> None:
        self.id=id
        self.name=name
        self.core=core
        self.ram=ram
        self.screen=screen
        self.price=price
        self.url=url
        self.rank=rank
        self.load_dttm=load_dttm
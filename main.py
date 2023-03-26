import os
import csv
import subprocess
import psycopg2 as pg
from dotenv import load_dotenv
load_dotenv()


# Проверим наличие таблицы ic1, если есть удалим
conn = pg.connect(host=os.getenv('PG_HOST'), port=int(os.getenv('PG_PORT')), user=os.getenv('PG_USER'), password= os.getenv('PG_PSWD'), dbname=os.getenv('PG_DB'))
with conn.cursor() as cursor:
    try:
        cursor.execute("DROP TABLE ic1;")
        conn.commit()  
    except Exception as e:
        print ("таблицы ic1 нет")
conn.close()

# Создадим таблицу ic1
conn = pg.connect(host=os.getenv('PG_HOST'), port=int(os.getenv('PG_PORT')), user=os.getenv('PG_USER'), password= os.getenv('PG_PSWD'), dbname=os.getenv('PG_DB'))
with conn.cursor() as cursor:
    cursor.execute("""
    CREATE TABLE public.ic1 (
        id serial4 NOT NULL,
        "name" varchar(128) NULL,
        core float4 NULL,
        ram int2 NULL,
        screen float4 NULL,
        price int8 NULL,
        url text NULL,
        "rank" int8 NULL,
        load_dttm timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT ic1_pk PRIMARY KEY (id)
    );
    CREATE INDEX ic1_screen_idx ON public.ic1 (screen,ram,core,price);

    -- Column comments
    COMMENT ON COLUMN public.ic1.id IS 'ид';
    COMMENT ON COLUMN public.ic1."name" IS 'Имя товара';
    COMMENT ON COLUMN public.ic1.core IS 'Кол-во ядер';
    COMMENT ON COLUMN public.ic1.ram IS 'Объем ОЗУ';
    COMMENT ON COLUMN public.ic1.screen IS 'Размер экрана';
    COMMENT ON COLUMN public.ic1.price IS 'Стоимость';
    COMMENT ON COLUMN public.ic1.url IS 'Линк';
    COMMENT ON COLUMN public.ic1."rank" IS 'Ранк';
    COMMENT ON COLUMN public.ic1.load_dttm IS 'Дата загрузки в БД';
""")
    conn.commit()  
    conn.close()

# Запуск парсера
subprocess.run("scrapy runspider spider/MySpider.py", shell=True)      


conn = pg.connect(host=os.getenv('PG_HOST'), port=int(os.getenv('PG_PORT')), user=os.getenv('PG_USER'), password= os.getenv('PG_PSWD'), dbname=os.getenv('PG_DB'))
with conn.cursor() as cursor:
    result=[['id', 'name', 'core', 'ram', 'screen', 'price', 'rank', 'url']]
    cursor.execute('''
    SELECT id, "name", core, ram, screen,  price, "rank", url
    FROM nouts
    ORDER BY "rank" DESC
    LIMIT 5;
    ''')
    for i in cursor:
        result.append([i["id"] , i["name"], i["core"], i["ram"], i["screen"], i["price"], i["rank"], i["url"]])
        with open('result-ic-1.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(result)
conn.close()
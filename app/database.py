# Database connection
import os

import pymysql

connection = pymysql.connect(host=os.getenv("DB_HOST"),
                             user=os.getenv("DB_USER"),
                             password=os.getenv("DB_PASSWORD"),
                             db=os.getenv("DB_NAME"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

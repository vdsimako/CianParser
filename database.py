import pandas as pd
import sqlite3
import sys

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def csv2sql(csvPath, con, sep=','):
	df = pd.read_csv(filePath, encoding='utf-8', header=None, names=['id', 'href', 'title', 'subtitle', 'amount', 'address'])
	df.title = df.apply(lambda row: row.title if pd.isna(row.subtitle) else row.subtitle, axis=1)
	df = df.drop('subtitle', axis=1)
	df.amount = df.amount.str.replace('\xa0₽', '')

	df.amount = df.amount.str.replace(' ','')

	df['floor'] = df.apply(lambda row: row.title.split(', ')[2].split(' ')[0], axis=1)
	df['area'] = df.apply(lambda row: row.title.split(', ')[1], axis=1)
	df['room_cnt'] = df.apply(lambda row: row.title.split(', ')[0].split('-')[0], axis=1)
	df = df.drop('title', axis=1)

	df.to_sql('t_offer', con=conn, if_exists='replace')

def clearDB():
	cursor.execute('drop table if exists t_offer')


def showTable(tableName):

	print('_-'*10 +tableName+ '-_'*10)

	cursor.execute(f'select * from {tableName}')
	for row in cursor.fetchall():
		print(row)

try:
	clearDB()
	filePath = sys.argv[1]
	csv2sql(filePath, conn)
	showTable('t_offer')
except Exception as e:
	raise e
	print('Вы не ввели путь к файлу')
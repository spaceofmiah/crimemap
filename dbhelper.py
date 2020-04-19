from datetime import datetime
import pymysql
import dbconfig


class DBHelper:
	def connect(self, database='crimemap'):
		return pymysql.connect(host='localhost', 
			user=dbconfig.DB_USERNAME,
			password=dbconfig.DB_PASSWORD,
			db=database)

		
	def add_crime(self, category, date, longitude, latitude, description):
		connection = self.connect()
		try:
			query = '''INSERT INTO crimes (category, date, longitude, latitude, description)
			VALUES('%s', '%s', '%s', '%s', '%s');'''%(category, date, longitude, latitude, description)

			with connection.cursor() as cursor:
				cursor.execute(query)
				connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()
	
	
	def get_all_crimes(self):
		connection = self.connect()
		try:
			query = "SELECT latitude, longitude, date, category, description from crimes"
			with connection.cursor() as cursor:
				cursor.execute(query)
				named_crimes = []
				for crime in cursor:
					named_crime = {
						'latitude': crime[0],
						'longitude': crime[1],
						'date': datetime.strftime(crime[2], '%Y-%m-%d'),
						'category': crime[3],
						'description': crime[4]
					}
					named_crimes.append(named_crime)
				return named_crimes
		except Exception as e:
			print(e)
		finally:
			connection.close()
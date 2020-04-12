import pymysql
import dbconfig


class DBHelper:

	def connect(self, database='crimemap'):
		return pymysql.connect(host='localhost', 
			user=dbconfig.DB_USERNAME,
			password=dbconfig.DB_PASSWORD,
			db=database)


	def get_all_inputs(self):
		connection = self.connect()
		try:
			query = "SELECT description from crimes;"
			with connection.cursor() as cursor:
				cursor.execute(query)
			return cursor.fetchall()
		except Exception as e:
			print(e)
		finally:
			connection.close()


	def add_input(self, data):
		connection = self.connect()
		try:
			# The following introduces a deliberate security flaw
			# see section on SQL injection below
			query = "INSERT INTO crimes (description) VALUES ('%s');"%(data)
			with connection.cursor() as cursor:
				cursor.execute(query)
				connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()


	def clear_all(self):
		connection = self.connect()
		try:
			query = "DELETE FROM crimes;"
			with connection.cursor() as cursor:
				cursor.execute(query)
				connection.commit()
		except Exception as e:
			print(e)
		else:
			connection.close()

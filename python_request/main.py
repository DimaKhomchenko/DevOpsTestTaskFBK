from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
import psycopg2
import os

class SimpleWrapper(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		decoded = post_data.decode('utf-8')
		with pg_connection.cursor() as cursor:
			try:
				sql = f"INSERT INTO data values (\'{decoded}\')"
				cursor.execute(sql)
				pg_connection.commit()
			except:
				print ("Failed transaction to DB, rolling back")
				pg_connection.rollback()
		self._set_response()
		self.wfile.write("POST request for {}\n".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleWrapper, port=8000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

if __name__ == '__main__':
	while True:
		try:
			pg_connection = psycopg2.connect(database=os.environ.get('POSTGRES_DB'), user=os.environ.get('POSTGRES_USER'), password=os.environ.get('POSTGRES_PASSWORD'), host=os.environ.get('POSTGRES_HOST'), port=os.environ.get('POSTGRES_PORT'))
		except psycopg2.OperationalError:
			print("Waiting for database to be ready")
			sleep(1)
			continue
		else:
			with pg_connection.cursor() as cursor:
				try:
					cursor.execute("""CREATE TABLE data	(PostData TEXT);""")
					pg_connection.commit()
				except psycopg2.errors.DuplicateTable:
					print("Database with this name alreadey exists, continuing in it")
					pg_connection.rollback()
				finally:
					break
	run()
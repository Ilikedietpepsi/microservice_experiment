from flask import Flask
from nameko.standalone.rpc import ServiceRpcProxy
import mysql.connector
import json
from werkzeug.middleware.profiler import ProfilerMiddleware
import redis

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='.')


def rpc_proxy(service):
    config = {'AMQP_URI': 'amqp://guest:guest@rabbit:5672'}
    return ServiceRpcProxy(service, config)

@app.route('/redis/<int:rows>')
def redis_add_data(rows):
    redis_db = redis.Redis(host='redis', port=6379, db=0)
    data = {f'key_{i}': f'value_{i}' for i in range(rows)}
    dict_str = json.dumps(data)
    redis_db.set('my_table', dict_str)
    return f'Added {rows} rows of data to Redis.'


@app.route('/<int:rows>')
def add_data(rows):
    connection = mysql.connector.connect(
        host='mysql',
        user='root',
        password='hezhenmin2000'
    )
    cursor = connection.cursor()

    print('Database "test" created successfully')

    cursor.execute('USE test')
    cursor.execute('DROP TABLE IF EXISTS customer')
    cursor.execute(
        'CREATE TABLE customer (id INT AUTO_INCREMENT PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )')
    for i in range(rows):
        cursor.execute('INSERT INTO customer () VALUES ()')
    connection.commit()
    cursor.close()
    connection.close()
    return 'Data inserted successfully'


@app.route('/async_mysql')
async def async_mysql():
    with rpc_proxy('async_mysql_x') as rpc:
        res = rpc.run('FETCH')
    return res


@app.route('/sync_mysql')
async def sync_mysql():
    with rpc_proxy('sync_mysql_y') as rpc:
        res = rpc.enhance_data('FETCH')
    return res

@app.route('/sync_redis')
async def sync_redis():
    with rpc_proxy('sync_redis_x') as rpc:
        res = rpc.process_data()
    return res
#
# @app.route('/http')
# def http():
#     with rpc_proxy('request') as rpc:
#         res = rpc.send_request()
#     return res



if __name__ == '__main__':
    app.run(port=8080)
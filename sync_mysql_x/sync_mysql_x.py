from nameko.rpc import rpc
import mysql.connector

class SyncServiceX:
    name = "sync_mysql_x"

    @rpc
    def process_data(self, ACTION):

        mydb = mysql.connector.connect(
            host="mysql",
            user="root",
            password="hezhenmin2000",
            database="test"
        )
        table = 'customer'

        mycursor = mydb.cursor()
        if ACTION == 'FETCH':
            mycursor.execute(f"SELECT * FROM {table}")

            myresult = mycursor.fetchall()
            processed_data = ''
            for x in myresult:
                processed_data += str(x) + '\n'
            mycursor.close()
            mydb.close()
            return processed_data
        if ACTION == 'INSERT':
            res = mycursor.execute(f"INSERT INTO {table} () VALUES ()")
            mydb.commit()
            mycursor.close()
            mydb.close()
            return res


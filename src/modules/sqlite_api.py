import sqlite3

class licitacionDataBase:
    def __init__(self, dbName, tableName, keyValues):
        conn = sqlite3.connect(dbName)
        print("Creando la tabla: " + tableName + ", en la base de datos: " + dbName + "...")
        try:
            conn.execute(f"CREATE TABLE {tableName}({keyValues});")
        except sqlite3.OperationalError:
            print("La tabla ya existe.")
        conn.close()
    
    def insert_values(self, db_name, table_name, key_names, values):
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Create a cursor
        cursor = conn.cursor()

        # Execute an INSERT statement to insert a new row into the table
        cursor.execute(f"INSERT INTO {table_name}({key_names}) VALUES ({','.join(['?'] * len(values))});", values)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    def delete_complete_row(self, db_name, table_name, rowid):
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Create a cursor
        cursor = conn.cursor()

        # Execute a DELETE statement to delete the row from the table
        cursor.execute(f"DELETE FROM {table_name} WHERE rowid = ?;", (rowid,))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
    
    def get_rows_given_value(self, db_name, table_name, key_name, value):
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Create a cursor
        cursor = conn.cursor()

        # Execute a SELECT statement to retrieve the rows from the table
        cursor.execute(f"SELECT * FROM {table_name} WHERE {key_name} = ?;", (value,))

        # Fetch the results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the results
        return results
    
    def delete_last_row(self, db_name, table_name):
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Create a cursor
        cursor = conn.cursor()

        # Get the number of rows in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        # Check if the table is empty
        if row_count == 0:
            print("Error: La tabla está vacía.")
        else:
            # Execute a DELETE statement to delete the last row from the table
            cursor.execute(f"DELETE FROM {table_name} WHERE rowid = (SELECT MAX(rowid) FROM {table_name});")

            # Commit the transaction
            conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    def read_table(self, db_name, table_name):
        # Connect to the database
        conn = sqlite3.connect(db_name)

        # Create a cursor
        cursor = conn.cursor()

        # Execute a SELECT statement to retrieve all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all rows from the SELECT statement
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the rows
        return rows
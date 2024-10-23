from mysql_conn import connect_to_mysql

# Conectarse a la base de datos
conn = connect_to_mysql()

if conn.is_connected():  # Llama a is_connected como método
    cursor = conn.cursor()

    # Consulta SQL
    query = "SELECT * FROM usuarios"
    
    try:
        # Ejecutar la consulta
        cursor.execute(query)

        # Iterar sobre las filas obtenidas
        for fila in cursor.fetchall():
            print(f"Id: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")

    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")
    
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

else:
    print("No se pudo conectar a la base de datos")


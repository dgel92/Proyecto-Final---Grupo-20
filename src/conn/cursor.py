from db_conn import connect_to_mysql

# Conectarse a la base de datos
conn = connect_to_mysql()

if conn and conn.is_connected():  # Verifica que conn no sea None y que esté conectado
    cursor = conn.cursor()

    # Consulta SQL
    queries = [
        "SELECT * FROM inversores",
        "SELECT * FROM cotizaciones",
        "SELECT * FROM acciones",
        "SELECT * FROM transacciones",
    ]

    try:
        for query in queries:
            cursor.execute(query)  # Ejecuta la consulta
            results = cursor.fetchall()  # Obtiene los resultados

            # Iterar sobre las filas obtenidas
            for fila in results:
                print(
                    f"Consulta: {query}, Datos: {fila}"
                )  # Imprime el resultado de cada consulta

    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()
else:
    print("No se pudo conectar a la base de datos")

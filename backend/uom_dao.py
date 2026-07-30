from sql_connection import get_sql_connection


def get_uom(connection):
    cursor = connection.cursor()

    try:
        query = "SELECT uom_id, uom_name FROM uom"
        cursor.execute(query)

        response = []

        for uom_id, uom_name in cursor.fetchall():
            response.append({
                "uom_id": uom_id,
                "uom_name": uom_name
            })

        return response

    except Exception as e:
        print("Error while fetching UOMs:", e)
        return []

    finally:
        cursor.close()


if __name__ == "__main__":
    connection = get_sql_connection()

    try:
        print(get_uoms(connection))
    finally:
        connection.close()
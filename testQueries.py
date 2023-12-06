import psycopg2

## asks the user for danceability and liveness and finds the 5 closest songs
def connect():
    conn = None
    try:

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="s-l112.engr.uiowa.edu",
            database="mdb_student19",
            user="mdb_student19",
            password="Rebel778")
		
        cur = conn.cursor()
        danceability = float(input("Enter danceability (0-1): "))
        liveness = float(input("Enter liveness(0-1): "))
        
        query = f"SELECT track_name FROM final.finalproject ORDER BY ABS(danceability - {danceability}) + ABS(liveness-{liveness}) LIMIT 5;"
        cur.execute(query)

        db_version = cur.fetchall()
        print(db_version)
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
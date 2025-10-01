import pymysql

def insert_test_report(scenario_name, result, test_time, description, case_type):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='admin123',
        db='giftian_report',
        charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO test_report (scenario_name, result, test_time, description, case_type)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (scenario_name, result, test_time, description, case_type))
        conn.commit()
    finally:
        conn.close()

import os
import sshtunnel
import pymysql

def query(q):
    with sshtunnel.SSHTunnelForwarder(
        ('bluenose.cs.dal.ca', 22),
        ssh_username=os.environ['SSH_USER'],
        ssh_password=os.environ['SSH_PASS'],
        remote_bind_address=('db.cs.dal.ca', 3306),
        local_bind_address=('127.0.0.1', 3307)
    ) as tunnel:
        conv = pymysql.converters.conversions.copy()
        conv[246]=float    # convert decimals to floats
        connection = pymysql.connect(host='127.0.0.1',
                                     port=3307,
                                     user=os.environ['MYSQL_USER'],
                                     password=os.environ['MYSQL_PASS'],
                                     db='csci4140_group8',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     conv=conv)

        try:
            with connection.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

def getHeatmap():
    statement = """
        SELECT dw_location.latitude AS lat, dw_location.longitude AS lng, SUM(dw_detections_fact.count) AS count
        FROM dw_detections_fact
        JOIN dw_location ON dw_detections_fact.location_id = dw_location.location_id
        GROUP BY lat, lng
    """

    return query(statement)

def getProjectBoundaries():
    pass

def getPlatforms():
    pass

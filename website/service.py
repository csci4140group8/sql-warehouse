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
        conv[246] = float    # convert decimals to floats
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

def getHeatmap(scale = None, value = None):
    where = "WHERE dw_time.%s = '%s'" % (scale, value) if scale else ""
    statement = """
        SELECT dw_location.latitude AS lat, dw_location.longitude AS lng, SUM(dw_detections_fact.count) AS count
        FROM dw_detections_fact
        JOIN dw_location ON dw_detections_fact.location_id = dw_location.location_id
        JOIN dw_time ON dw_detections_fact.time_id = dw_time.time_id
        %s
        GROUP BY lat, lng
    """ % (where)

    return query(statement)

def getTimeSteps(time_scale):
    statement = """
        SELECT DISTINCT dw_time.%s
        FROM dw_time
        ORDER BY dw_time.%s
    """ % (time_scale, time_scale)

    result = query(statement)
    arr = []

    for entry in result:
        arr.append(entry[time_scale])

    return arr

def getProjectBoundaries(project_id):
    where = "WHERE dw_projects.project_id = '%s'" % (project_id) if project_id else ""
    statement = """
        SELECT dw_projects.project_id, dw_projects.geospatial_lat_max AS lat_max, dw_projects.geospatial_lat_min AS lat_min, dw_projects.geospatial_lon_max AS lng_max, dw_projects.geospatial_lon_min AS lng_min
        FROM dw_projects
        %s;
    """ % (where)
    
    return query(statement)

def getProjects():
    statement = """
        SELECT project_id, name AS 'project_name'
        FROM dw_projects;
    """

    return query(statement)

def getPlatforms(project_id):
    where = "WHERE dw_platform_fact.project_id = '%s'" % (project_id) if project_id else ""
    statement = """
        SELECT dw_location.latitude AS lat, dw_location.longitude AS lng, SUM(dw_platform_fact.count) AS count
        FROM dw_platform_fact
        JOIN dw_location ON dw_platform_fact.location_id = dw_location.location_id
        %s
        GROUP BY lat, lng;
    """ % (where)
    
    return query(statement)

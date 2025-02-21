import logging
import json
from DB_manager import DatabaseManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        conn = DatabaseManager.get_db_connection()

        try:
            # Get query string parameters instead of body
            query_params = event.get('queryStringParameters', {})

            staff_id = query_params.get('staffId')
            department_id = query_params.get('departmentId')

            if not staff_id and not department_id:
                logger.error("Both 'staffId' and 'departmentId' are missing.")
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json",
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                        "statusCode": 400,
                        "responseMessage": "FAILURE",
                        "response": "Either 'staffId' or 'departmentId' is required."
                    })
                }

            if staff_id:  
                logger.info("Fetching staff with staffId: %s", staff_id)
                select_staff_query = '''
                    SELECT staffId, name, email, departmentId, status, createdAt, updatedAt
                    FROM STAFF
                    WHERE staffId = %s
                '''
                with conn.cursor() as cur:
                    cur.execute(select_staff_query, (staff_id,))
                    result = cur.fetchone()

                    if result:
                        staff_details = {
                            "staffId": result[0],
                            "name": result[1],
                            "email": result[2],
                            "departmentId": result[3],
                            "status": result[4],
                            "createdAt": result[5],
                            "updatedAt": result[6]
                        }
                        logger.info("Fetched staff details: %s", staff_details)
                        return {
                            "statusCode": 200,
                            "headers": {
                                "Content-Type": "application/json",
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                            },
                            "body": json.dumps({
                                "statusCode": 200,
                                "responseMessage": "SUCCESS",
                                "response": staff_details
                            }, default=str)
                        }
                    else:
                        logger.error("Staff not found for staffId: %s", staff_id)
                        return {
                            "statusCode": 404,
                            "headers": {
                                "Content-Type": "application/json",
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                            },
                            "body": json.dumps({
                                "statusCode": 404,
                                "responseMessage": "STAFF NOT FOUND",
                                "response": "No staff found with the provided staffId."
                            })
                        }

            elif department_id:  
                logger.info("Fetching staff for departmentId: %s", department_id)
                select_department_query = '''
                    SELECT staffId, name, email, departmentId, status, createdAt, updatedAt
                    FROM STAFF
                    WHERE departmentId = %s
                '''
                with conn.cursor() as cur:
                    cur.execute(select_department_query, (department_id,))
                    results = cur.fetchall()

                    if results:
                        staff_list = []
                        for result in results:
                            staff_list.append({
                                "staffId": result[0],
                                "name": result[1],
                                "email": result[2],
                                "departmentId": result[3],
                                "status": result[4],
                                "createdAt": result[5],
                                "updatedAt": result[6]
                            })
                        logger.info("Fetched staff details for department: %s", staff_list)
                        return {
                            "statusCode": 200,
                            "headers": {
                                "Content-Type": "application/json",
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                            },
                            "body": json.dumps({
                                "statusCode": 200,
                                "responseMessage": "SUCCESS",
                                "response": staff_list
                            }, default=str)
                        }
                    else:
                        logger.error("No staff found for departmentId: %s", department_id)
                        return {
                            "statusCode": 404,
                            "headers": {
                                "Content-Type": "application/json",
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                            },
                            "body": json.dumps({
                                "statusCode": 404,
                                "responseMessage": "STAFF NOT FOUND",
                                "response": "No staff found for the provided departmentId."
                            })
                        }

        except Exception as ex:
            logger.error("Error processing request: %s", str(ex))
            return {
                "statusCode": 502,
                "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                },
                "body": json.dumps({
                    "statusCode": 502,
                    "responseMessage": "FAILURE",
                    "response": str(ex)
                })
            }

        finally:
            if conn:
                conn.close()

    except Exception as ex:
        logger.error("Database connection error: %s", str(ex))
        return {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            "body": json.dumps({
                "statusCode": 502,
                "responseMessage": "FAILURE",
                "response": str(ex)
            })
        }

if __name__ == "__main__":
    event = {
        "queryStringParameters": {
            "staffId": "2"
        }
    }
    response = lambda_handler(event, None)
    print(response)

import logging
import json
from DB_manager import DatabaseManager
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        conn = DatabaseManager.get_db_connection()

        try:
            query_params = event.get('queryStringParameters', {})
            staff_id = query_params.get('staffId')

            if not staff_id:
                logger.error("staffId is missing or invalid")
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
                        "response": "staffId is required."
                    })
                }

            delete_staff_query = '''
                DELETE FROM STAFF 
                WHERE staffId = %s
            '''

            with conn.cursor() as cur:
                cur.execute(delete_staff_query, (staff_id,))
                conn.commit()

                if cur.rowcount > 0:
                    logger.info("Successfully deleted staff record for staffId: %s", staff_id)
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
                            "response": f"Staff record with staffId {staff_id} has been successfully deleted."
                        })
                    }
                else:
                    logger.error("Staff not found with staffId: %s", staff_id)
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
                            "response": f"No staff found with the provided staffId {staff_id}."
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
                }, default=str)
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
            }, default=str)
        }

if __name__ == "__main__":
    event = {
        "queryStringParameters": {
            "staffId": "8"  
        }
    }
    response = lambda_handler(event, None)
    print(response)

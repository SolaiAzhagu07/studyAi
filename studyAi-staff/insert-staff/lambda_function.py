import hashlib
import logging
import json
from DB_manager import DatabaseManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hash_password(password):
    """Hashes the password using SHA1"""
    return hashlib.sha1(password.encode()).hexdigest()

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        conn = DatabaseManager.get_db_connection()

        try:
            staff_details = json.loads(event['body'])
            logger.info("Staff details: %s", staff_details)

            status_value = staff_details['status']
            raw_password = staff_details['password']

            # Hash the password using SHA1 before storing it
            hashed_password = hash_password(raw_password)

            insert_staff_query = '''
                INSERT INTO STAFF (name, email, departmentId, status, createdAt, updatedAt, password)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s)
            '''

            staff_data = [
                staff_details['name'],
                staff_details['email'],
                staff_details['departmentId'],
                status_value,
                hashed_password  # Store SHA1 hashed password
            ]

            with conn.cursor() as cur:
                cur.execute(insert_staff_query, staff_data)
                conn.commit()

                logger.info("Inserted staff with ID: %s", cur.lastrowid)

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
                        "response": {
                            "name": staff_details['name'],
                            "email": staff_details['email'],
                            "departmentId": staff_details['departmentId'],
                            "status": staff_details['status']
                        }
                    }, default=str)
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
        "body": json.dumps({
            "name": "saravanan",
            "email": "staff@gmail.com",
            "departmentId": "1",
            "status": 1,
            "password": "staff@123"
        })
    }
    response = lambda_handler(event, None)
    print(response)

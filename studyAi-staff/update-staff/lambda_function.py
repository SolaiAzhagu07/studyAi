import logging
import json
import hashlib
from DB_manager import DatabaseManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def hash_password(password):
    """Hashes the password using SHA-1"""
    return hashlib.sha1(password.encode()).hexdigest()

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        conn = DatabaseManager.get_db_connection()

        try:
            staff_details = json.loads(event['body'])
            logger.info("Staff details: %s", staff_details)

            # Check if staff exists
            check_query = "SELECT COUNT(*) FROM STAFF WHERE staffId = %s"
            with conn.cursor() as cur:
                cur.execute(check_query, (staff_details['staffId'],))
                (staff_count,) = cur.fetchone()

            if staff_count == 0:
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
                        "responseMessage": "FAILURE",
                        "errorMessage": "Staff not found"
                    })
                }

            # Prepare update query dynamically
            update_fields = []
            update_values = []

            if "name" in staff_details:
                update_fields.append("name = %s")
                update_values.append(staff_details["name"])

            if "roleId" in staff_details:
                update_fields.append("roleId = %s")
                update_values.append(staff_details["roleId"])

            if "email" in staff_details:
                update_fields.append("email = %s")
                update_values.append(staff_details["email"])

            if "departmentId" in staff_details:
                update_fields.append("departmentId = %s")
                update_values.append(staff_details["departmentId"])

            if "totalTokens" in staff_details:
                update_fields.append("totalTokens = %s")
                update_values.append(staff_details["totalTokens"])

            if "usedTokens" in staff_details:
                update_fields.append("usedTokens = %s")
                update_values.append(staff_details["usedTokens"])

            if "status" in staff_details:
                update_fields.append("status = %s")
                update_values.append(staff_details["status"])

            if "mobileNumber" in staff_details:
                update_fields.append("mobileNumber = %s")
                update_values.append(staff_details["mobileNumber"])

            if "password" in staff_details and staff_details["password"]:
                hashed_password = hash_password(staff_details["password"])
                update_fields.append("password = %s")
                update_values.append(hashed_password)

            if not update_fields:
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
                        "errorMessage": "No valid fields provided for update"
                    })
                }

            update_values.append(staff_details["staffId"])
            update_query = f"UPDATE STAFF SET {', '.join(update_fields)} WHERE staffId = %s"

            with conn.cursor() as cur:
                cur.execute(update_query, update_values)
                conn.commit()

            logger.info("Updated staff with staffId: %s", staff_details["staffId"])

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
                    "staffId": staff_details["staffId"]
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
                    "errorMessage": str(ex)
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
                "errorMessage": str(ex)
            })
        }

if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "staffId": 1,
            "name": "John Doe",
            "roleId": 2,
            "email": "johndoe@example.com",
            "departmentId": 5,
            "totalTokens": 100,
            "usedTokens": 50,
            "status": 1,
            "mobileNumber": "9876543210",
            "password": "securepassword123"
        })
    }
    response = lambda_handler(event, None)
    print(response)

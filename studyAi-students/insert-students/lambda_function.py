import logging
from DB_manager import DatabaseManager
import pymysql
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        conn = DatabaseManager.get_db_connection()
        try:
            logger.info("Received event: %s", event)
            product_detail = json.loads(event['body'])
            # Ensure the table name is updated to 'prod_purchase'
            insert_product_query = '''INSERT INTO purchase.product (item_name, quantity, product_price, tax, total_amount) 
                                        VALUES (%s, %s, %s, %s, %s)'''
            product_data = [
                product_detail['item_name'],
                product_detail['quantity'],
                product_detail['product_price'],
                product_detail['tax'],
                product_detail['total_amount']
            ]
            # Log the query and data to verify correctness
            logger.info("Executing query: %s with data: %s", insert_product_query, product_data)
            with conn.cursor() as cur:
                cur.execute(insert_product_query, product_data)
                conn.commit()
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
                },
                "body": json.dumps({
                    "statusCode": 200,
                    "responseMessage": "SUCCESS",
                    "response": product_detail
                }, default=str)
            }
        except Exception as ex:
            logger.error("Error during product insertion: %s", ex)
            return {
                "statusCode": 502,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
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
        logger.error("Database connection error: %s", ex)
        return {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE"
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
            "item_name": "Sample Product",
            "quantity": 10,
            "product_price": 50.75,
            "tax": 5.25,
            "total_amount": 56.00
        })
    }
    print(lambda_handler(event, None))

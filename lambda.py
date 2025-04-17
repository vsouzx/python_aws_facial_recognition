import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

try:
    # Tentar obter o valor da variável de ambiente
    table_name = os.environ['DYNAMODB_TABLE']
except KeyError:
    # Lançar uma exceção personalizada se a variável não estiver configurada
    raise EnvironmentError("A variável de ambiente 'DYNAMODB_TABLE' não está configurada.")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    return "lambda ok"

#decimal utils
def decimal_default(obj):
    if isinstance(obj, Decimal):
        try:
            return int(obj) 
        except (ValueError, OverflowError):
            return float(obj) 
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

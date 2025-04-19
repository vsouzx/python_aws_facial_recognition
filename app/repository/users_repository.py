import boto3
import os
from boto3.dynamodb.conditions import Attr

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

try:
    # Tentar obter o valor da variável de ambiente
    table_name = os.environ['DYNAMODB_TABLE']
    bucket_name = os.environ['BUCKET_NAME']
except KeyError:
    # Lançar uma exceção personalizada se a variável não estiver configurada
    raise EnvironmentError("A variável de ambiente não está configurada.")

table = dynamodb.Table(table_name)

def save_item(item):
    table.put_item(Item=item)


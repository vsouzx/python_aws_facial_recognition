import boto3
import os
from boto3.dynamodb.conditions import Attr

try:
    # Tentar obter o valor da variável de ambiente
    table_name = os.environ['DYNAMODB_TABLE']
except KeyError:
    # Lançar uma exceção personalizada se a variável não estiver configurada
    raise EnvironmentError("A variável de ambiente 'DYNAMODB_TABLE' não está configurada.")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
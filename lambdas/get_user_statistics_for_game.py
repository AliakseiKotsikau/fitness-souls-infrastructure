import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table_name = os.environ.get('TABLE_NAME')

dynamodb = boto3.resource('dynamodb')
fitnessSoulsTable = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


def lambda_handler(event, context):
    user = event['user']
    game = event['game']

    user_equals = Key("user").eq(user)
    game_equals = Key("game").begins_with(f'{game}')

    response = fitnessSoulsTable.query(
        KeyConditionExpression=user_equals & game_equals,
        ProjectionExpression='bosses, currentBoss, exercises, exerciseStats, worldDeathCount'
    )

    mapped_response = {}

    for item in response['Items']:
        first_key = next(iter(item))
        first_value = item[first_key]
        mapped_response[first_key] = first_value

    return json.dumps(mapped_response, cls=DecimalEncoder)

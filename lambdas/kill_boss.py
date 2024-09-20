import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

table_name = os.environ.get('TABLE_NAME', 'fitness_souls')

dynamodb = boto3.resource('dynamodb')
fitness_souls_table = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


def lambda_handler(event, context):
    user = event['user']
    game = event['game']
    boss = event['boss']

    user_equals = Key("user").eq(user)
    game_equals = Key("game").begins_with(f'{game}')

    bosses_response = fitness_souls_table.query(
        KeyConditionExpression=user_equals & game_equals,
        ProjectionExpression='bosses'
    )['Items'][0]['bosses']

    order_numbers = list(map(lambda x: bosses_response[x]['orderNumber'], bosses_response))
    last_order_number = max(order_numbers)

    response = fitness_souls_table.update_item(
        Key={
            'user': user,
            'game': f'{game}#bossDeaths'
        },
        UpdateExpression='SET bosses.#boss.beaten = :beaten, bosses.#boss.orderNumber = :orderNumber',
        ExpressionAttributeNames={
            '#boss': boss
        },
        ExpressionAttributeValues={
            ':beaten': True,
            ':orderNumber': Decimal(str(last_order_number + 1))
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
    }

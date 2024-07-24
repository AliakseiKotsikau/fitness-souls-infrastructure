import json
import boto3
import os
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
    boss = event['boss']

    response = fitnessSoulsTable.update_item(
        Key={
            'user': user,
            'game': f'{game}#bossDeaths'
        },
        UpdateExpression='SET bosses.#boss.deathCount = bosses.#boss.deathCount + :increment',
        ExpressionAttributeNames={
            '#boss': boss
        },
        ExpressionAttributeValues={
            ':increment': Decimal(str(1))
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response, cls=DecimalEncoder)
    }


print(lambda_handler({'user': 'kotsial', 'game': 'DarkSouls1', "boss": "Artorias"}, None))

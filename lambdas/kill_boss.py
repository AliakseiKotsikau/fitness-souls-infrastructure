import json
import boto3
import os
from decimal import Decimal

table_name = os.environ.get('TABLE_NAME')

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

    item_key = {'user': user, 'game': game + '#bossDeaths'}

    bosses_response = fitness_souls_table.get_item(Key=item_key)['Item']['bosses']

    beaten_numbers = list(map(lambda x: bosses_response[x]['beatenNumber'], bosses_response))
    last_beaten_number = max(beaten_numbers)

    response = fitness_souls_table.update_item(
        Key={
            'user': user,
            'game': f'{game}#bossDeaths'
        },
        UpdateExpression='SET bosses.#boss.beaten = :beaten, bosses.#boss.beatenNumber = :beatenNumber',
        ExpressionAttributeNames={
            '#boss': boss
        },
        ExpressionAttributeValues={
            ':beaten': True,
            ':beatenNumber': Decimal(str(last_beaten_number + 1))
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
    }

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
    exercise = event['exercise']

    response = fitnessSoulsTable.update_item(
        Key={
            'user': user,
            'game': f'{game}#exercises'
        },
        UpdateExpression='SET exercises.#exercise.minReps = :minReps, exercises.#exercise.maxReps = :maxReps, '
                         'exercises.#exercise.active = :active',
        ExpressionAttributeNames={
            '#exercise': exercise
        },
        ExpressionAttributeValues={
            ':minReps': event['minReps'],
            ':maxReps': event['maxReps'],
            ':active': event['active'],
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
    }
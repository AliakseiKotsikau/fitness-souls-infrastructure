import json
import boto3
import os
from decimal import Decimal

from botocore.exceptions import ClientError

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
    increment = event['quantity']

    try:
        response = fitnessSoulsTable.update_item(
            Key={
                'user': user,
                'game': f'{game}#exerciseStats'
            },
            UpdateExpression='SET exerciseStats.#exercise.quantity = exerciseStats.#exercise.quantity + :increment',
            ExpressionAttributeNames={
                '#exercise': exercise
            },
            ConditionExpression='attribute_exists(exerciseStats.#exercise)',
            ExpressionAttributeValues={
                ':increment': Decimal(increment)
            },
            ReturnValues="UPDATED_NEW"
        )
        print('Exercise exists and was updated.')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Exercise does not exist. Add new exercise')
            response = fitnessSoulsTable.update_item(
                Key={
                    'user': user,
                    'game': f'{game}#exerciseStats'
                },
                UpdateExpression='SET exerciseStats.#exercise = :newExercise',
                ExpressionAttributeNames={
                    '#exercise': exercise
                },
                ConditionExpression='attribute_not_exists(exerciseStats.#exercise)',
                ExpressionAttributeValues={
                    ':newExercise': {
                        'quantity': Decimal(increment)
                    }
                },
                ReturnValues="UPDATED_NEW"
            )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
    }

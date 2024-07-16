import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal

boto3.setup_default_session(profile_name='kotsial')

table_name = os.environ.get('TABLE_NAME', 'fitness_souls')

dynamodb = boto3.resource('dynamodb')
fitnessSoulsTable = dynamodb.Table(table_name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

def lambda_handler(event, context):
    # TODO implement
    user = event['user']
    game = event['game']

    #userEquals = Key("user").eq(user)
    #gameEquals = Key("game").begins_with(f'{game}#deaths')

    boss_string = u'{ "Asylum Demon": {"orderNumber": 1, "deathCount": 0}, "Taurus Demon": {"orderNumber": 2, "deathCount": 3}, "Belfry Gargoyles": {"orderNumber": 2, "deathCount": 5}, "Moonlight Butterfly": {"orderNumber": 2, "deathCount": 1}, "Capra Demon": {"orderNumber": 2, "deathCount": 0}, "Gaping Dragon": {"orderNumber": 2, "deathCount": 1}, "Quelaag": {"orderNumber": 2, "deathCount": 2}, "Iron Golem": {"orderNumber": 2, "deathCount": 0}, "Stray Demon": {"orderNumber": 2, "deathCount": 0}, "Priscilla": {"orderNumber": 2, "deathCount": 0}, "Ornstein & Smough": {"orderNumber": 2, "deathCount": 0}, "Gwyndolin": {"orderNumber": 2, "deathCount": 0}, "Sif": {"orderNumber": 2, "deathCount": 0}, "Four Kings": {"orderNumber": 2, "deathCount": 0}, "Pinwheel": {"orderNumber": 2, "deathCount": 0}, "Gravelord Nito": {"orderNumber": 2, "deathCount": 0}, "Seath the Scaleless": {"orderNumber": 2, "deathCount": 0}, "Ceaseless Discharge": {"orderNumber": 2, "deathCount": 0}, "Firesage Demon": {"orderNumber": 2, "deathCount": 0}, "Centipede Demon": {"orderNumber": 2, "deathCount": 0}, "Bed of Chaos": {"orderNumber": 2, "deathCount": 0}, "Sanctuary Guardian": {"orderNumber": 2, "deathCount": 0}, "Artorias": {"orderNumber": 2, "deathCount": 0}, "Manus": {"orderNumber": 2, "deathCount": 0}, "Kalameet": {"orderNumber": 2, "deathCount": 0}, "Gwyn": {"orderNumber": 2, "deathCount": 0}}'

    #response = fitnessSoulsTable.query(KeyConditionExpression=userEquals & gameEquals )

    fitnessSoulsTable.put_item( Item={'user': user, 'game': f'{game}#bossDeaths', "bosses": json.loads(boss_string)})

    return {
        'statusCode': 200,
        #'body': json.dumps(response, cls=DecimalEncoder)
    }

print(lambda_handler({'user': 'kotsial', 'game': 'DarkSouls1'}, None))
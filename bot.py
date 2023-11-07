from flask import Flask, requests
import stickers
import services

bot = Flask(__name__)

@bot.route('/webhook', methods=['GET'])
def Verify_Token():
    try:
        token = requests.args.get('hub.verify_token')
        challlenge = requests.arges.get('hub_challenge')

        if token == stickers.token and challlenge != None:
            return challlenge
        else:
            return 'Token incorrecto', 403
    except Exception as e:
        return e, 403
    
@bot.route('/webhook', methods=['POST'])
def Get_Messages():
    try:
        body = requests.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['Id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.Get_Message_Wpp(message)

        services.Bot_Manager(text, number, messageId, name)
        return 'Enviado'
    except Exception as e:
        return 'No enviado ' + str(e)
    
if __name__ == '__main__':
    bot.run()
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from services.challenges import search_challenges
from services.trivia import search_trivia

import time, openpyxl

account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'

#Todo: support multiple users
phone_number = 'YOUR_NUMBER'


client = Client(account_sid, auth_token)

challenge_time = '12:50'
trivia_time = '14:50'

def send_challenge(user_number):
    challenge = search_challenges()

    wb = openpyxl.load_workbook('current_challenge.xlsx')
    sheet = wb['Sheet1']
    sheet['A' + '1'].value = challenge['challenge']
    sheet['B' + '1'].value = challenge['carbon']
    sheet['C' + '1'].value = challenge['water']
    sheet['D' + '1'].value = challenge['money']
    wb.save('current_challenge.xlsx')
            
    message = client.messages.create(
                              body=challenge['challenge'],
                              from_='whatsapp:+' + user_number,
                              to='whatsapp:+' + user_number
                          )
    print(message.sid)

def send_trivia(user_number):
    question = search_trivia()

    wb = openpyxl.load_workbook('current_trivia.xlsx')
    sheet = wb['Sheet1']
    sheet['A' + '1'].value = question['question']
    sheet['B' + '1'].value = question['solution']
    sheet['C' + '1'].value = question['explanation']
    wb.save('current_trivia.xlsx')

    text = 'Trivia Question of the Day!\n' + question['question']
            
    message = client.messages.create(
                              body=text,
                              from_='whatsapp:+' + user_number,
                              to='whatsapp:+' + user_number
                          )
    print(message.sid)

def get_message(usermessage):
    if usermessage == 'stats' or usermessage == 'lifetime stats':
        file = open('lifetime_stats.txt', 'r')
        lifetime = file.readlines()
        file.close()

        if len(lifetime) == 0:
            message = 'Your Lifetime Stats: \nCarbon Saved: %slb \nWater Saved: %s litres \nMoney Saved: $%s' %(0, 0, 0)
        else:
            message = 'Your Lifetime Stats: \nCarbon Saved: %slb \nWater Saved: %s litres \nMoney Saved: $%s' %(lifetime[0], lifetime[1], lifetime[2])
            
    elif usermessage == 'daily stats':
        file = open('daily_stats.txt', 'r')
        daily = file.readlines()
        file.close()

        if len(daily) == 0:
            message = 'Your Daily Stats: \nCarbon Saved: %slb \nWater Saved: %s litres \nMoney Saved: $%s' %(0, 0, 0)
        else:
            message = 'Your Daily Stats: \nCarbon Saved: %slb \nWater Saved: %s litres \nMoney Saved: $%s' %(daily[0], daily[1], daily[2])
            
    elif usermessage == 'done':
        wb = openpyxl.load_workbook('current_challenge.xlsx')
        sheet = wb['Sheet1']
        challenge = sheet['A' + '1'].value
        carbon = sheet['B' + '1'].value
        water = sheet['C' + '1'].value
        money = sheet['D' + '1'].value

        if challenge == None:
            message = 'You do not have an ongoing challenge'
        else:
            message = 'Congratulations! You have saved %slb of carbon, %s litres of water, and $%s! Your impact means a lot :)' %(carbon, water, money)
            
            file = open('daily_stats.txt', 'r')
            daily = file.readlines()
            file.close()

            file = open('daily_stats.txt','w')
            if len(daily) == 0:
                file.write('%s\n%s\n%s'%(carbon, water, money))
            else:
                file.write('%s\n%s\n%s'%(float(carbon)+float(daily[0]), float(water)+float(daily[1]), float(money)+float(daily[2])))
            file.close()

            file = open('lifetime_stats.txt', 'r')
            lifetime = file.readlines()
            file.close()

            file = open('lifetime_stats.txt','w')
            if len(lifetime) == 0:
                file.write('%s\n%s\n%s'%(carbon, water, money))
            else:
                file.write('%s\n%s\n%s'%(float(carbon)+float(lifetime[0]), float(water)+float(lifetime[1]), float(money)+float(lifetime[2])))
            file.close()

            wb = openpyxl.load_workbook('current_challenge.xlsx')
            sheet = wb['Sheet1']
            sheet['A' + '1'].value = None
            sheet['B' + '1'].value = None
            sheet['C' + '1'].value = None
            sheet['D' + '1'].value = None
            wb.save('current_challenge.xlsx')
            
    elif usermessage == 'a' or usermessage == 'b' or usermessage == 'c' or usermessage == 'd':
        wb = openpyxl.load_workbook('current_trivia.xlsx')
        sheet = wb['Sheet1']
        question = sheet['A' + '1'].value
        solution = sheet['B' + '1'].value
        explanation = sheet['C' + '1'].value

        if question == None:
            message = 'You do not have an ongoing trivia question'
        else:
            if usermessage == solution.lower():
                message = 'That is correct! ' + explanation
            else:
                message = 'That is incorrect. ' + explanation

            wb = openpyxl.load_workbook('current_trivia.xlsx')
            sheet = wb['Sheet1']
            sheet['A' + '1'].value = None
            sheet['B' + '1'].value = None
            sheet['C' + '1'].value = None
            wb.save('current_trivia.xlsx')
        
    elif usermessage == 'new':
        message = 'Tada! This new challenge has replaced your previous challenge, if you had one ongoing'
        send_challenge(phone_number)
    elif usermessage == 'help':
        message = 'Lifetime Stats: View lifetime stats\nDaily Stats: View Daily Stats\nDone: Complete current challenge\nNew: Get new challenge'
    else:
        message = "Sorry, I did not understand that. Please type 'help' for help"

    return message


app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello World!'

@app.route('/whatsapp', methods=['POST'])

def reply():
    usermessage = request.values.get('Body')
    usermessage = usermessage.lower()

    message = get_message(usermessage)
 
    response = MessagingResponse()
    response.message(message)
    print('Message sent')
    return str(response)

# Todo: implement cron scheduling
current_time = time.strftime("%H:%M", time.localtime())
send_challenge(phone_number)

if __name__ == '__main__':
    app.run()

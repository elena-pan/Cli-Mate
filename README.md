<h1 align="center">
  <br>
  <img src="https://user-images.githubusercontent.com/52430997/104131835-52f41780-5336-11eb-8c94-116511d35f72.png" alt="Cli-Mate" width="200">
  <br>
  Cli-Mate
  <br>
</h1>

<h4 align="center">A Sustainability Phone Buddy</h4>

<p align="center">
  <a href="#overview">Overview</a> • <a href="#screenshots">Screenshots</a> • <a href="#installation">Installation</a> • <a href="#authors">Authors</a>
</p>

## Overview

Cli-Mate is a WhatsApp buddy designed to promote sustainable living habits and boost knowledge on climate change. The server responds to user messages and sends daily challenges via WhatsApp. It then tracks the amount of carbon, water, and money saved by completing these challenges. There is also a trivia question of the day, which allows users to learn more about climate change and how they can help. The server is built in Flask and integrates with Twilio's WhatsApp API.

This project was built for the 2020 Calgary Youth Hackathon and won the Best Technology Award.

## Screenshots

<p align="center">
  <img src="https://user-images.githubusercontent.com/52430997/104131406-4fab5c80-5333-11eb-8ccf-df4d12592bd4.png" alt="Screenshot 1" width="300px">
  <img src="https://user-images.githubusercontent.com/52430997/104131416-5fc33c00-5333-11eb-93da-b00687c3ae35.png" alt="Screenshot 2" width="300px">
</p>

## Installation

### Server

Setup your Twilio account and Twilio WhatsApp sandbox via the instructions [here](https://www.twilio.com/docs/whatsapp/sandbox). This allows you to run a development build while you wait for Twilio to approve your production number, which you can do [here](https://www.twilio.com/whatsapp/request-access). Once you have your Twilio account, add your server url to your Twilio account.

Cli-Mate requires Python 3.7+ installed on the server. Begin by installing and starting the server:

```cmd
# Clone this repository
$ git clone https://github.com/elena-pan/Cli-Mate.git

# Install Python dependencies
$ python3 -m pip install -r requirements.txt

# Put in your Twilio account ID and auth token
# Replace the account_sid and auth_token variable strings on lines 10-11 of app.py with your account details.
# Replace phone number on line 14 of app.py with your phone number.

# Run the server
$ python -m flask run
```


## Authors

* [Elena Pan](https://github.com/elena-pan), [Dhananjay Patki](https://github.com/dpatki), and Jenny Wu

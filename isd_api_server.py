from flask import Flask
from flask import request
from flask import redirect
import boto3
import logging
import os

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

aws_region = os.environ['SNS_TOPIC'].split(':')[3]


def write_to_sns(user_name, user_email, subject_line, message):
    client = boto3.client('sns', region_name=aws_region)
    response = client.publish(
        TopicArn=os.environ['SNS_TOPIC'],
        Message=message,
        Subject=subject_line,
        MessageStructure='string',
        MessageAttributes=dict(user_name={
            'DataType': 'string',
            'StringValue': user_name
        }, user_email={
            'DataType': 'string',
            'StringValue': user_email
        })
    )

    return response


@app.route('/api/message', methods=['POST'])
def handle_message():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    logging.info("Message from {} ({}) Subject='{}' Message='{}'".format(name, email, subject, message))

    orig_url = request.referrer.split('?')[0]
    if name == "" or email == "" or subject == "" or message == "":
        logging.warning("One or more fields were empty, not sending message to topic.")
        return redirect(orig_url + "?messagesub=false" or "ERROR")

    if write_to_sns(name, email, subject, message) == dict:
        logging.debug("Wrote to SNS topic. redirect to {}".format(orig_url + "?messagesub=true"))
        return redirect(orig_url + "?messagesub=true" or "OK")
    else:
        logging.error("Error writing to SNS topic")
        return redirect(orig_url + "?messagesub=false" or "ERROR")


@app.route('/api/heartbeat', methods=['GET'])
def heartbeat():
    return "OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask
from flask import request
from flask import redirect
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def write_to_sns_topic(user_name, user_email, subject_line, message):
    #client = boto3.client('sns')
    #d = {'contact_name': user_name, 'contact_email': user_email, 'contact_subject': subject_line, 'contact_message': message}
    # response = client.publish(
    #     TopicArn=os.env['asdsad'],
    #     Message=json.dumps(d),
    #     Subject=subject_line,
    #     MessageStructure='string',
    #     MessageAttributes={
    #         'string': {
    #             'DataType': 'string',
    #             'StringValue': 'string',
    #             'BinaryValue': b'bytes'
    #         }
    #     }
    #)
    return True


@app.route('/api/message', methods=['POST'])
def handle_message():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    logging.debug("Got message from {} ({}) Subject={} Message={}".format(name, email, subject, message))

    orig_url = request.referrer.split('?')[0]
    if name == "" or email == "" or subject == "" or message == "":
        logging.debug("One or more fields were empty, not sending message to topic.")
        return redirect(orig_url + "?messagesub=false" or "ERROR")

    if write_to_sns_topic(name, email, subject, message):
        logging.debug("Sucessfully wrote to SNS topic")
        return redirect(orig_url + "?messagesub=true" or "OK")
    else:
        logging.error("Error writing to SNS topic")
        return redirect(orig_url + "?messagesub=false" or "ERROR")


@app.route('/api/healthcheck', methods=['GET'])
def heartbeat():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
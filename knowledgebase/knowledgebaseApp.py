import http.client
import json
import sys
from config.config_reader import ConfigReader
from logger.logger import Log
import ast



class KnowledgeBase():
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.kb_host = self.configuration['KB_HOST']
        self.kb_endpoint = self.configuration['KB_ENDPOINT']
        self.kb_route = ''

        self.log = Log()

    def get_answer_from_kb(self, kb_details, question_from_user):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.kb_route = self.configuration[kb_details]

        question_to_kb = {}
        question_to_kb.update({'question': question_from_user})


        headers = {
            'Authorization': 'EndpointKey ' + self.kb_endpoint,
            'Content-Type': 'application/json'
        }

        try:
            self.log.write_log(sessionID='session1', log_message="question " + str(question_to_kb))
            self.conn = http.client.HTTPSConnection(self.kb_host, port=443)
            self.conn.request("POST", self.kb_route, str(question_to_kb), headers)
            self.response = self.conn.getresponse()
            self.answer = self.response.read()

            #this code is written to fetch the actual answer provided by the knowlegemaker

            answer_in_str = str(json.loads(self.answer))
            answer_in_dict = ast.literal_eval(answer_in_str)
            answer_return = answer_in_dict['answers'][0]['answer']

            self.log.write_log(sessionID='session1', log_message="question " + str(answer_return))
            return answer_return

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])

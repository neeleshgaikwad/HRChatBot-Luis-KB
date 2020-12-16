from botbuilder.core import TurnContext, ActivityHandler, RecognizerResult
from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
import json
from config.config_reader import ConfigReader
from logger.logger import Log
from knowledgebase.knowledgebaseApp import KnowledgeBase
import ast

class LuisConnect(ActivityHandler):
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.luis_app_id = self.configuration['LUIS_APP_ID']
        self.luis_endpoint_key = self.configuration['LUIS_ENDPOINT_KEY']
        self.luis_endpoint = self.configuration['LUIS_ENDPOINT']
        self.luis_app = LuisApplication(self.luis_app_id, self.luis_endpoint_key, self.luis_endpoint)
        self.luis_options = LuisPredictionOptions(include_all_intents=True, include_instance_data=True)
        self.luis_recognizer = LuisRecognizer(application=self.luis_app, prediction_options=self.luis_options,
                                              include_api_results=True)
        self.log = Log()

    async def on_message_activity(self, turn_context: TurnContext):
        knowledgebase = KnowledgeBase()

        luis_result = await self.luis_recognizer.recognize(turn_context)
        result = luis_result.properties["luisResult"]
        top_intent = self.top_intent(luis_result)

        user_query = turn_context.activity.text

        kb_answer = knowledgebase.get_answer_from_kb(top_intent, user_query)
        self.log.write_log(sessionID='session1', log_message="Answer from KB is : " + str(kb_answer))
        await turn_context.send_activity(f"{kb_answer}")

    @staticmethod
    def top_intent(results: RecognizerResult, default_intent: str = "None", min_score: float = 0.0) -> str:
        if results is None:
            raise TypeError("LuisRecognizer.top_intent(): results cannot be None.")

        top_intent: str = None
        top_score: float = -1.0
        if results.intents:
            for intent_name, intent_score in results.intents.items():
                score = intent_score.score
                if score > top_score and score >= min_score:
                    top_intent = intent_name
                    top_score = score

        return top_intent or default_intent



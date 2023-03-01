# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import json
import random
import requests
import ask_sdk_core.utils as ask_utils
import tempfile

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


checkanswer= {}
aplquestion={}

def getQuestions(category,difficulty, player_count):
    counter = 0
    questions = {}
    amm = 5
    #if(difficulty not in ["1","2","3"]) and (difficulty not in ["easy","medium","hard"]) :
    #   raise ArgumentError().message("difficulty must either be one of ['1','2','3'] or ['easy','medium','hard']")

    url = buildUrl(amm,category,difficulty, player_count)
    resp = requests.get(url).json()

    if resp["response_code"] != 0:
        return

    for entry in resp['results']:
        i_a = []
        q = entry['question']
        if "&quot;" in q:
            q = q.replace("&quot;", "'")
        if "&amp;" in q:
            q = q.replace("&amp;", "&")
        if "&eacute;" in q:
            q = q.replace("&eacute;", "e")
        c_a = entry['correct_answer']
        if "&quot;" in c_a:
            c_a = c_a.replace("&quot;", "'")
        if "&amp;" in c_a:
            c_a = c_a.replace("&amp;", "&")
        if "&eacute;" in c_a:
            c_a = c_a.replace("&eacute;", "e")
        for answ in entry['incorrect_answers']:
            if "&quot;" in answ:
                answ = answ.replace("&quot;", "'")
            if "&amp;" in answ:
                answ = answ.replace("&amp;", "&")
            if "&eacute;" in answ:
                answ = answ.replace("&eacute;", "e")
            i_a.append(answ)
        qdict = dict(question = q, correct_answer = c_a, incorrect_answers = i_a)
        name = "question" +str(counter)
        questions[name]= qdict
        checkanswer.update(questions)
        counter += 1
        

    return questions

def buildUrl(amount: int,category: str,difficulty: str or int, player_count):
    comp = []
    category = category.lower()

    #Typ
    comp.append("type=multiple")
        

    # Categories
    #comp.append("category="+str(category))
    categorylist = []
    if category == "science":
        categorylist.append("category=17")
        categorylist.append("category=18")
        categorylist.append("category=19")
        categorylist.append("category=30")

            
    if category == "art":
        categorylist.append("category=25")

    if category == "sport and hobbies":
        categorylist.append("category=28")
        categorylist.append("category=21")

    if category == "entertainment":
        categorylist.append("category=10")
        categorylist.append("category=11")
        categorylist.append("category=12")
        categorylist.append("category=13")
        categorylist.append("category=14")
        categorylist.append("category=15")
        categorylist.append("category=16")
        categorylist.append("category=29")
        categorylist.append("category=31")
        categorylist.append("category=32")

    if category == "history":
        categorylist.append("category=23")

    if category == "geography":
        categorylist.append("category=22")
        
        


    ri= random.randint(0,len(categorylist))
    if ri < 1:
        ri = 1
    cat = categorylist[ri-1]
    comp.append(cat)


    # Difficulty
    if "str" in str(type(difficulty)):
        difficulty = "difficulty="+difficulty
    else:
        if difficulty == 1:
            difficulty = "difficulty=easy" 
        elif difficulty == 2:
            difficulty = "difficulty=medium"
        elif difficulty == 3:
            difficulty == "difficulty=hard"
    comp.append(difficulty)

    c_resp = requests.get("https://opentdb.com/api_count.php?"+str(cat)).json()
    # Amount
    string = "total_"+difficulty.split("=")[1]+"_question_count"
    if amount > c_resp["category_question_count"][string]:
        amount = c_resp["category_question_count"][string]-2
    while not amount % player_count == 0:
        amount -= 1
    
    amount = str(amount)
    comp.append("amount="+amount)
         


    url = "https://opentdb.com/api.php?"+( "&".join(comp))
    return url

def selectQuestion():
    answers = []
    length = len(checkanswer) - 1
    q = checkanswer[f"question"+str(length)]["question"]
    answers.append(checkanswer[f"question"+str(length)]["correct_answer"])
    for answ in  checkanswer[f"question"+str(length)]["incorrect_answers"]:
        answers.append(answ)
    question = {}
    question.update(id = length, cquestion = q, answ = answers )
    random.shuffle(answers)
    aplquestion.update(question = question)


def currentcolor(color):
    if color == "green":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_green.png"
        aplquestion["question"].update(link = _link)

    if color == "grey":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_grey.png"
        aplquestion["question"].update(link = _link)

    if color == "lightblue":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_lightblue.png"
        aplquestion["question"].update(link = _link)

    if color == "purple":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_purple.png"
        aplquestion["question"].update(link = _link)

    if color == "pink":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_pink.png"
        aplquestion["question"].update(link = _link)

    if color == "red":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_red.png"
        aplquestion["question"].update(link = _link)

    if color == "yellow":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_yellow.png"
        aplquestion["question"].update(link = _link)

    if color == "blue":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_blue.png"
        aplquestion["question"].update(link = _link)

    if color == "orange":
        _link = "https://dsatrivialpursuit.blob.core.windows.net/png/player_card_orange.png"
        aplquestion["question"].update(link = _link)





class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to our trivia gameshow. Would you like to start a game?"
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        #if ("state" in _session_attr) and (_session_attr["state"] == "introduced"):
        _session_attr["playerCount"] = 0
        _session_attr["max_q_per_player"] = 5
        _session_attr["state"] = "waitingForPlayerCount"
        speak_output = "Thats cool! How many players are you?"
        return (handler_input.response_builder.speak(speak_output).ask(speak_output).response)


class NumberOfPlayersIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        _session_attr = handler_input.attributes_manager.session_attributes
        return ("state" in _session_attr) and (_session_attr["state"] == "waitingForPlayerCount") and ask_utils.is_intent_name("NumberOfPlayersIntent")(handler_input)
        
    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        playerCount = int(handler_input.request_envelope.request.intent.slots["count"].value)
        _session_attr["playerCount"] = playerCount
        self.launch_screen(handler_input)
        if playerCount > 1:
            speak_output = "Okay. Player one, which color do you want?"
        else:
            speak_output = "Okay. Which color do you want?"
        reprompt = "Which color do you want?"
        _session_attr["state"] = "waitingForPlayerColor"
        return (handler_input.response_builder.speak(speak_output).ask(reprompt).response)


    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = ask_utils.get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None

    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="colorToken",
                    document={
                        "type": "Link",
                        "src": "doc://alexa/apl/documents/Color"
                    }
                )
            )


class AddPlayerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        _session_attr = handler_input.attributes_manager.session_attributes
        return ("state" in _session_attr) and (_session_attr["state"] == "waitingForPlayerColor") and ask_utils.is_intent_name("AddPlayerIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        playerColor = handler_input.request_envelope.request.intent.slots["color"].resolutions.resolutions_per_authority[0].values[0].value.name
        if not ("player" in _session_attr):                      # If no players are added yet, the first one gets added
            _i = 0
            _session_attr["aktPlayer"] = 0
            _session_attr["player"] = {
                "0": {
                    "color": playerColor,
                    "score": 0,
                },
            }
        else:
            _i = len(_session_attr["player"])                    # if at least one player is added yet, the next one gets added
            _session_attr["player"][str(_i)] = {
                "color": playerColor,
                "score": 0,
            }
        if _i == (_session_attr["playerCount"] - 1):             # If all players are added now
            _session_attr["state"] = "waitingForDifficulty"
            speak_output = "Okay! Now that we are ready, on which difficulty do you want to play? You can choose between easy, medium and hard."
            reprompt = "On which difficulty do you want to play? You can select either easy,medium or hard."
        else:
            speak_output = ("Okay! Player "+ str(_i+2) +" which color do you want?")
            reprompt = ("Player "+ str(_i+2) +" which color do you want?")
        return(handler_input.response_builder.speak(speak_output).ask(reprompt).response)


class SetDifficultyIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        _session_attr = handler_input.attributes_manager.session_attributes
        return ("state" in _session_attr) and (_session_attr["state"] == "waitingForDifficulty") and ask_utils.is_intent_name("SetDifficultyIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        _difficulty = handler_input.request_envelope.request.intent.slots["difficulty"].resolutions.resolutions_per_authority[0].values[0].value.name
        _session_attr["difficulty"] = _difficulty
        self.launch_screen(handler_input)
        speak_output = f"The difficulty has been set to {_difficulty}. Which categories do you want to use? You can choose between Geography, History, Sports and Hobbies, Art, Entertainment and Science."
        reprompt = "Which categories do you want to use? You can pick between Geography, History, Sports and Hobbies, Art, Entertainment and Science."
        _session_attr["state"] = "waitingForCategory"
        return(handler_input.response_builder.speak(speak_output).ask(reprompt).response)

    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = ask_utils.get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None

    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="catToken",
                    document={
                        "type": "Link",
                        "src": "doc://alexa/apl/documents/Categories"
                    }
                )
            )


class SelectCategoryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        _session_attr = handler_input.attributes_manager.session_attributes
        return ("state" in _session_attr) and ask_utils.is_intent_name("SelectCategoryIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        _categories = handler_input.request_envelope.request.intent.slots["categoryname"].resolutions.resolutions_per_authority[0].values[0].value.name
        _session_attr["categories"] = _categories
        getQuestions(category=_session_attr["categories"], difficulty=str(_session_attr["difficulty"]), player_count = _session_attr["playerCount"])
        length = len(checkanswer) - 1
        _session_attr["numQ"] = length
        _session_attr["currQ"] = 1
        speak_output = "The game is ready to start. Say 'Ready' if you are ready."
        return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)

    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = ask_utils.get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None

    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            print(aplquestion)
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="questToken",
                    document={
                        "type": "Link",
                        "src": "doc://alexa/apl/documents/Questions"
                    },
                    datasources=aplquestion
                )
            )
            
class ReadyIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        
        return ask_utils.is_intent_name("ready")(handler_input)
    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        aktPlayerNr = int(_session_attr["aktPlayer"])
        aktPlayerColor = _session_attr["player"][str(aktPlayerNr)]["color"]
        
        
        if _session_attr["numQ"] < 2:
            getQuestions(category=_session_attr["categories"], difficulty=str(_session_attr["difficulty"]), player_count = _session_attr["playerCount"])
        selectQuestion()
        currentcolor(aktPlayerColor)
        self.launch_screen(handler_input)
        if _session_attr["state"] == "question1":
            speak_output = f"The Game starts now! Please answer each question with A, B, C or D.  Here is your first question {aktPlayerColor} : {aplquestion['question']['cquestion']}., A: {aplquestion['question']['answ'][0]}. B: {aplquestion['question']['answ'][1]}. C: {aplquestion['question']['answ'][2]}. and D: {aplquestion['question']['answ'][3]}"
            
        else:
            speak_output = f"Player {aktPlayerColor} , here is your question : {aplquestion['question']['cquestion']}., A: {aplquestion['question']['answ'][0]}. B: {aplquestion['question']['answ'][1]}. C: {aplquestion['question']['answ'][2]}. and D: {aplquestion['question']['answ'][3]}"
        
        print("Schbeak = "+speak_output)
        _session_attr["currQ"] = _session_attr["currQ"] +1
        _session_attr["state"] = "question" + str(_session_attr["currQ"])
        
        return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)
        
    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = ask_utils.get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None

    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            print(aplquestion)
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="questToken",
                    document={
                        "type": "Link",
                        "src": "doc://alexa/apl/documents/Questions"
                    },
                    datasources=aplquestion
                )
            )
        


class LastQuestionAnswerIntentHandler(AbstractRequestHandler): 
    def can_handle(self, handler_input: HandlerInput) -> bool:
        _session_attr = handler_input.attributes_manager.session_attributes
        return ask_utils.is_intent_name("AnswerIntent")(handler_input) and (((_session_attr["currQ"] -1) / _session_attr["playerCount"]) >= _session_attr["max_q_per_player"])

    def handle(self, handler_input: HandlerInput) -> Response:
        _alexa = handler_input.response_builder
        _session_attr = handler_input.attributes_manager.session_attributes
        _answerHandle = handler_input.request_envelope.request.intent.slots["answerSlot"].resolutions.resolutions_per_authority[0].values[0].value.name

        if _answerHandle == "A":
            _answer = aplquestion["question"]["answ"][0]
        if _answerHandle == "B":
            _answer = aplquestion["question"]["answ"][1]
        if _answerHandle == "C":
            _answer = aplquestion["question"]["answ"][2]
        if _answerHandle == "D":
            _answer = aplquestion["question"]["answ"][3]
        print(_answer)
        quest = "question" + str(aplquestion["question"]["id"])
        aktPlayerNr = str(_session_attr["aktPlayer"])
        for entry in checkanswer.keys():
            print(quest)
            print(entry)
            if quest == entry:
                correct = checkanswer[entry]["correct_answer"]
                if correct == _answer:
                    speak_output = "That is correct! "
                    _session_attr["player"][aktPlayerNr]["score"] += 1
                    #return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)
                else:
                    speak_output = f"That is wrong! {correct} was correct. "
                    #return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)
        checkanswer.popitem()
        highscore = {}
        highscore.update(points = 0, color = "")
        playerCount = _session_attr["playerCount"]
        print(highscore)
        for i in range(0,playerCount):
            playerScore = _session_attr["player"][str(i)]["score"]
            playerColor = _session_attr["player"][str(i)]["color"]
            if playerScore > highscore["points"]:
                highscore["points"] = playerScore
                highscore.update(color = playerColor)
                print(highscore)
            elif playerScore == highscore["points"] and highscore["color"] != playerColor:
                lcolor = []
                lcolor.append(playerColor)
                lcolor.append(highscore["color"])
                highscore.update(points = playerScore, color = lcolor)
                print(highscore)
        if type(highscore["points"]) == list:
            speak_output = f"The Game is now over. The winners are {highscore['color']['0']} and {highscore['color']['1']} with {highscore['points']}"
        else:
            speak_output = f"The Game is now over. The winner is {highscore['color']} with {highscore['points']}"
        _session_attr["numQ"] = _session_attr["numQ"] - 1  
        aktPlayerNr = int(_session_attr["aktPlayer"])
        aktPlayerColor = _session_attr["player"][str(aktPlayerNr)]["color"]
        aktPlayerScore = _session_attr["player"][str(aktPlayerNr)]["score"]
        currentcolor(aktPlayerColor)
        return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)
    
    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = ask_utils.get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None

    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            print(aplquestion)
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="endToken",
                    document={
                        "type": "Link",
                        "src": "doc://alexa/apl/documents/Winner"
                    },
                    datasources=aplquestion
                )
            )
        
        
        
class QuestionAnswerIntentHandler(AbstractRequestHandler): 
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        _session_attr = handler_input.attributes_manager.session_attributes
        _answerHandle = handler_input.request_envelope.request.intent.slots["answerSlot"].resolutions.resolutions_per_authority[0].values[0].value.name
        print("checkanswer = "+str(checkanswer))
        if _answerHandle == "A":
            _answer = aplquestion["question"]["answ"][0]
        if _answerHandle == "B":
            _answer = aplquestion["question"]["answ"][1]
        if _answerHandle == "C":
            _answer = aplquestion["question"]["answ"][2]
        if _answerHandle == "D":
            _answer = aplquestion["question"]["answ"][3]
        print(_answer)
        quest = "question" + str(aplquestion["question"]["id"])
        for entry in checkanswer.keys():
            print(quest)
            print(entry)
            if quest == entry:
                correct = checkanswer[entry]["correct_answer"]
                print(correct)
                if correct == _answer:
                    speak_output = "That is correct! Say ready if you are ready for the next question"
                    aktPlayerNr = str(_session_attr["aktPlayer"])
                    print(aktPlayerNr)
                    _session_attr["player"][aktPlayerNr]["score"] =  _session_attr["player"][aktPlayerNr]["score"] + 1
                    print("ciao correct")
                    checkanswer.popitem()
                    _session_attr["numQ"] = _session_attr["numQ"] - 1
                    aktPlayerNr = int(aktPlayerNr)
                    aktPlayerNr += 1
                    if aktPlayerNr > int(_session_attr["playerCount"]) - 1:
                        aktPlayerNr = 0
                    aktPlayerNr = str(aktPlayerNr)
                    _session_attr["aktPlayer"] = aktPlayerNr
                    return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)
                else:
                    speak_output = f"That is wrong! {correct} was correct. Say ready if you are ready for the next question"
                    print("ciao wrong")
                    checkanswer.popitem()
                    _session_attr["numQ"] = _session_attr["numQ"] - 1
                    aktPlayerNr = int(_session_attr["aktPlayer"])
                    aktPlayerNr += 1
                    if aktPlayerNr > int(_session_attr["playerCount"]) - 1:
                        aktPlayerNr = 0
                    aktPlayerNr = str(aktPlayerNr)
                    _session_attr["aktPlayer"] = aktPlayerNr
                    return(handler_input.response_builder.speak(speak_output).ask(speak_output).response)



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "This is a trivia game. First you will get asked how many players want to play the game and everyone can choose a color. Then you can choose the category and the difficulty. You can answer the questions with A, B, C and D. Between each Question you have to say ready. If you currently have no ongoing game, you can answer with yes to start one now"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "See you next time! Thank you for playing our game."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NumberOfPlayersIntentHandler())
sb.add_request_handler(AddPlayerIntentHandler())
sb.add_request_handler(SetDifficultyIntentHandler())
sb.add_request_handler(SelectCategoryIntentHandler())
sb.add_request_handler(LastQuestionAnswerIntentHandler())
sb.add_request_handler(QuestionAnswerIntentHandler())
sb.add_request_handler(ReadyIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
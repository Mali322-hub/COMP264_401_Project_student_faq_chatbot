from chalice import Chalice
import boto3

app = Chalice(app_name='student_faq_chatbot')

AWS_REGION = 'us-east-1'
BOT_ID = 'your_bot_id'
BOT_ALIAS_ID = 'your_alias_id'
LOCALE_ID = 'en_US'

lex_client = boto3.client('lexv2-runtime', region_name=AWS_REGION)
comprehend_client = boto3.client('comprehend', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table('StudentFAQ')


@app.route('/')
def index():
    return {'message': 'Student FAQ Chatbot backend is running'}


@app.route('/chat', methods=['POST'], cors=True)
def chat():
    request = app.current_request
    body = request.json_body

    if not body:
        return {'answer': 'No data received.', 'key_phrases': []}

    question = body.get('question', '').strip()

    if not question:
        return {'answer': 'Please type a question.', 'key_phrases': []}

    try:
        # Step 1: Send question to Lex
        lex_response = lex_client.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS_ID,
            localeId=LOCALE_ID,
            sessionId='student-session-1',
            text=question
        )

        # Step 2: Get matched intent name
        session_state = lex_response.get('sessionState', {})
        intent = session_state.get('intent', {})
        intent_name = intent.get('name')

        if not intent_name:
            return {
                'answer': 'Sorry, I could not understand your question.',
                'key_phrases': []
            }

        # Step 3: Read answer from DynamoDB
        db_response = table.get_item(Key={'question': intent_name})

        if 'Item' in db_response:
            answer_text = db_response['Item']['answer']
        else:
            answer_text = f'I understood the intent "{intent_name}", but no answer was found in DynamoDB.'

        # Step 4: Detect key phrases with Comprehend
        comprehend_response = comprehend_client.detect_key_phrases(
            Text=question,
            LanguageCode='en'
        )

        key_phrases = []
        seen = set()

        for item in comprehend_response.get('KeyPhrases', []):
            phrase = item.get('Text', '').strip()
            if phrase and phrase.lower() not in seen:
                key_phrases.append(phrase)
                seen.add(phrase.lower())

        return {
            'answer': answer_text,
            'key_phrases': key_phrases[:5]
        }

    except Exception as e:
        return {
            'answer': 'System error: ' + str(e),
            'key_phrases': []
        }

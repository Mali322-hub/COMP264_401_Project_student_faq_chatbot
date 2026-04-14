# COMP264_401_Project_student_faq_chatbot
This project is a backend chatbot service built with AWS Chalice.

## Technologies used
- Python
- Chalice
- Boto3
- Amazon Lex V2 Runtime
- Amazon Comprehend
- Amazon DynamoDB

## Files
- `app.py` — main backend code
- `requirements.txt` — Python dependencies

## Requirements
```txt
chalice
boto3

Run commands on Linux:
Create virtual environment: python3 -m venv venv
Activate it: source venv/bin/activate
Install dependencies: pip install -r requirements.txt
Configure AWS: aws configure
 (Use: region: us-east-1
output: json) 
Update Lex settings in app.py

Replace:

BOT_ID = 'your_bot_id'
BOT_ALIAS_ID = 'your_alias_id'

Make sure DynamoDB table exists
The table name must be:

StudentFAQ

Each item should contain:
question
answer
The question must match the Lex intent name

Run the project: chalice local


import json
from openai import OpenAI
import os
import sqlite3

print("Running db_bot.py (interactive mode)!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):
    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # populate data

def runSql(query):
    return sqliteCursor.execute(query).fetchall()

# OPENAI
configPath = getPath("config.json")
print("Using config:", configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key=config["openaiKey"])

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)
    return "".join(responseList)

# Helper: strip ```sql ... ```
def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]
    return value.strip()

# Prompt prefix (keeps it focused on SQL only)
commonSqlOnlyRequest = (
    setupSqlScript +
    " Give me a sqlite select statement that answers the question. " +
    "Only respond with sqlite syntax. Do not explain."
)

print("============================================================")
print("INTERACTIVE MODE")
print("Type your questions (or 'quit' to exit)")
print("============================================================")

while True:
    question = input("\nYour question: ")
    if question.lower() in ["quit", "exit", "q"]:
        break

    try:
        print("============================================================")
        print(f"QUESTION: {question}")
        print("STRATEGY: few-shot")

        # Step 1: generate SQL
        getSqlFromQuestion = commonSqlOnlyRequest + " " + question
        sqlSyntaxResponse = getChatGptResponse(getSqlFromQuestion)
        sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
        print("\nStep 1: Generating SQL query...")
        print("GENERATED SQL:")
        print(sqlSyntaxResponse)

        # Step 2: execute SQL
        print("\nStep 2: Executing query...")
        queryRawResponse = str(runSql(sqlSyntaxResponse))
        print("Retrieved", queryRawResponse)

        # Step 3: friendly response
        print("\nStep 3: Generating natural language response...")
        friendlyResultsPrompt = (
            f'I asked: "{question}" and the database returned: {queryRawResponse}. '
            "Please give a short, friendly answer using just this data."
        )
        friendlyResponse = getChatGptResponse(friendlyResultsPrompt)

        print("\nRESPONSE:")
        print(friendlyResponse)

    except Exception as err:
        print("❌ ERROR:", str(err))

sqliteCursor.close()
sqliteCon.close()
print("Done!")


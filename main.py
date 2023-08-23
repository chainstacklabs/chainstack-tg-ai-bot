from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os

load_dotenv()

TOKEN = os.getenv('CHAINSTACK_BOT_TOKEN')
BOT_USERNAME = os.getenv('CHAINSTACK_BOT_USERNAME')

# Initialize environment variables
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')

# Initialize components
embeddings = OpenAIEmbeddings(disallowed_special=())
deep_lake = DeepLake(
    dataset_path=os.getenv('DATASET_PATH'),
    read_only=True,
    embedding=embeddings,
)
retriever = deep_lake.as_retriever()
retriever.search_kwargs.update({
    'distance_metric': 'cos',
    'fetch_k': 100,
    'maximal_marginal_relevance': True,
    'k': 10,
})
model = ChatOpenAI(streaming=False, callbacks=[StreamingStdOutCallbackHandler()], model_name=os.getenv('LANGUAGE_MODEL'), temperature=0.0)
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, return_source_documents=True)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I am Chainstack AI; ask me anything about the Chainstack documentation.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I have access to the Chainstack documentation. You can ask anything about it, where to find information, if there is a guide about a topic you need, or even ask what method you need to get blockchain data.')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom command here.')

# Responses
def handle_response(text: str) -> str:
    question = text
    result = qa({"question": question, "chat_history": []})

    answer = result['answer']

    # Take the first source to display
    first_document = result['source_documents'][0]
   
    metadata = first_document.metadata

    source = metadata['source']

    bot_answer = answer + '\n \n' + f'Source: {source}'
    
    return bot_answer

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_id = update.message.chat.id
    user_data = update.message.chat
    print(f'User {user_id} in {message_type} asks: {text}')
    print(user_data)
    if message_type == 'group' or message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    #print('Bot response:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused this error: {context.error}')

if __name__ == '__main__':
    print('Starting Chainstack bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands 
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Check for new messages every 2 seconds
    print('Polling new messages...')
    app.run_polling(poll_interval=2)    # Seconds

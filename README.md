# Chainstack AI Telegram bot

AI-powered Telegram bot all knowing about Chainstack docs. It uses GPT 3.5/4 and context stored using [Actvieloop's Deep Lake](https://app.activeloop.ai/) as a vector database.

- `index.py` is run to index the data from the docs.
- `main.py` is the bot script itself.

## Quickstart

- Clone the repo

```sh
git clone https://github.com/soos3d/chainstack-tg-ai-bot.git
```

- Create a new Python virtual environment

```sh
python3 -m venv chainstack-ai-tg
```

- Activate the virtual environment

```sh
source chainstack-ai-tg/bin/activate
```

- Install dependencies

```sh
pip install -r requirements.txt
```

- Add Telegram bot token and username, API keys, and Deep Lake account path to `.env.example` and rename `.env`

```env
# Bot config
CHAINSTACK_BOT_TOKEN="BOT_TOKEN_FROM_BOTFATHER" # Chainstack_AI_bot token
CHAINSTACK_BOT_USERNAME="@USERNAME"

# OpenAI
OPENAI_API_KEY="OPENAI_KEY"
EMBEDDINGS_MODEL="text-embedding-ada-002"
LANGUAGE_MODEL="gpt-3.5-turbo" # gpt-4 gpt-3.5-turbo-0613

# Scrape settings
SITE_MAP="https://docs.chainstack.com/sitemap.xml"
URLS_FILTER="https://docs.chainstack.com/reference/"

# Deeplake vector DB
ACTIVELOOP_TOKEN="ACTIVELOOP_TOKEN"
DATASET_PATH="hub://USER_ID/custom_dataset" # "./local_chainstack_docs_db"  # Edit with your user ID if you want to use the cloud db. or use the `./` for a local instance.
```

- Run the index file to scrape the docs and store them

```sh
python3 index.py
```

- Run the main file to start the bot

```sh
python3 main.py
```

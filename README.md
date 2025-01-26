# Roast me Dobby

A cute little chatbot that uses Sentient's Dobby unhinged model to roast you...

and when your feelings get too hurt, you can just switch it to nice mode :)


## Setup

```bash
git clone git@github.com:awiteckzb/roast-me-dobby.git
cd roast-me-dobby
python -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements.txt
cp .env.example .env
```

Populate the `.env` file with your API keys.

From there to launch, just run

```bash
streamlit run app/frontend/chat_app.py
```
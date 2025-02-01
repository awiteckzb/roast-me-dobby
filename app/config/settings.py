import os
import dotenv

dotenv.load_dotenv()


class Settings:
    FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DOBBY_UNHINGED = (
        "accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b"
    )


settings = Settings()

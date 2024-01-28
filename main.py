from moviepy.editor import *
from openai import OpenAI
import googleapipythonclient


def main():
    title = input("Video title: ")
    main_theme = input("Video main theme: ")
    plataform = input('Short Content Plataform  ("Shorts", "Reels", "TikTok") :')

    


    client = OpenAI(
    api_key=os.environ.get("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"),
    )
    

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}]
    )


























if __name__ == __main__:
    main()

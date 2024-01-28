from moviepy.editor import *
from openai import OpenAI
import googleapiclient
from gtts import gTTS
import os


def main():
    while True:
        title = input("Video title: ")
        main_theme = input("Video main theme: ")
        music_prompt = input("Music Prompt: ")
        plataform = input('Short Content Plataform  ("Shorts", "Reels", "TikTok") :')
        script_default = input("Special Script or Default? ")
        word_amount = input("Amount of words: ")

        video_file = video_formation(title, main_theme, script_default, word_amount, music_prompt)   
        uploading(video_file, plataform)


        again = input("Again? (yes, no)" )
        if again == "no":
            break




def video_formation(title, main_theme, script_default, word_amount, music_prompt):
    music = music_generation(music_prompt)
    full_text = text_generation(title, main_theme, script_default, word_amount)
    text = ""
    for i in full_text:
        if i == '.':
            break
            

    background = background_generation(text)




def uploading(filename, plataform):
    review = input("Preview video first? (yes, no)")
    if review == "yes":
        clip = VideoFileClip(filename) 
        clip.preview(fps = 20) 

    title = input("Video title: ")
    description = input("Video description: ")
    keywords = input("Video Keywords: ")
    privacy = input("Video privacy status: (private, public)")
    category = "22"



def music_generation():
    pass

def text_generation():
    pass

def background_generation():
    pass
    

    
    


    client = OpenAI(
    api_key=os.environ.get("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"),
    )
    

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}]
    )


























if __name__ == __main__:
    main()

from moviepy.editor import *
from openai import OpenAI
import googleapiclient
from gtts import gTTS


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
    texts = full_text.split('.')


    frames = []
    for text in texts:
        background = background_generation(text)
        speech = text_to_speech(text)
        clip = VideoFileClip(background)  
        txt_clip = TextClip(text, fontsize = 75, color = 'black') 
        clipe = CompositeVideoClip([clip, txt_clip])
        audioclip = AudioFileClip(speech)
        frame = clip.set_audio(audioclip) 

        frames.append(frame)  

    
    final_clip = concatenate_videoclips(frames)
    music_audio = AudioFileClip(music)

    final_video = final_clip.set_audio(music_audio)
    final_video.write_videofile("output_video.mp4", codec="libx264", fps=24)



def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "speech.mp3"
    tts.save(filename)
    return filename






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



def music_generation(music_prompt):
    pass

def text_generation(title, main_theme, script_default, word_amount):
    pass

def background_generation(text):
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

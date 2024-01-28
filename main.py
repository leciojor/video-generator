from moviepy.editor import *
from openai import OpenAI
import googleapiclient
from gtts import gTTS


def main():
    while True:
        title = input("Video title: ")
        main_theme = input("Video main theme: ")
        music_prompt = input("Music Prompt: ")
        plataform = input('Short Content Plataform  (OPTIONS: Shorts, Reels, TikTok) :')
        script_default = input("Special Script or Default? (OPTIONS: script, default)")
        openai_key = input("Insert OpenAi key: ")
        if script_default == "script":
            script = input("Please give your desired narrative structure: ")
        word_amount = input("Amount of words: ")

        video_file = video_formation(title, main_theme, script_default, word_amount, music_prompt, script, openai_key)   
        uploading(video_file, plataform)


        again = input("Again? (OPTIONS: yes, no)" )
        if again == "no":
            break




def video_formation(title, main_theme, script_default, word_amount, music_prompt, script, openai_key):
    music = music_generation(music_prompt)
    full_text = text_generation(title, main_theme, script_default, word_amount, script, openai_key)
    texts = full_text.split('.')
    texts = [title] + texts


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
    final_video.write_videofile("final_video.mp4", codec="libx264", fps=24)
    filename = "final_video.mp4"
    return filename




def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "speech.mp3"
    tts.save(filename)
    return filename






def uploading(filename, plataform):
    review = input("Preview video first? (OPTIONS: yes, no)")
    if review == "yes":
        clip = VideoFileClip(filename) 
        clip.preview(fps = 20) 

    title = input("Video title: ")
    description = input("Video description: ")
    keywords = input("Video Keywords: ")
    privacy = input("Video privacy status: (private, public)")
    category = "22"
    if plataform == "Shorts":
        pass


    elif plataform == "Reels":
        print("Reels is not an available plataform yet")
    elif plataform == "TikTok":
        print("TikTok is not an available plataform yet")




def music_generation(music_prompt):
    pass

def text_generation(title, main_theme, script_default, word_amount, script, openai_key):
    client = OpenAI(
    api_key=os.environ.get(openai_key),
    )
    
    if script_default == "default":
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
        {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
        {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure. You cannot say more than {word_amount} words"},
        ]
        )
    else:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
        {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
        {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure. You cannot say more than {word_amount} words"},
        ]
        )

    return response['choices'][0]['message']['content']


def background_generation(text):
    pass
    

    
    


    


























if __name__ == __main__:
    main()

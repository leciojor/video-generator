from moviepy.editor import *
from openai import OpenAI
import googleapiclient
from gtts import gTTS

#debug
#finish youtube API
#implement music generation
#implement rest of random mode (not having to answer all the other questions (just apis's, mode and word amoutn))
#remove test keys


def main():
    while True:
        while True:
            mode = input("Choose mode: (OPTIONS: Random, Manual)")
            if mode != "Random" and mode != "Manual":
                print("Invalid option")
            else:
                break
        title = input("Video title: ")
        main_theme = input("Video main theme: ")
        music_prompt = input("Music Prompt: ")
        while True:
            plataform = input('Short Content Plataform  (OPTIONS: Shorts, Reels, TikTok) : ')
            if plataform != "Shorts" and plataform != "Reels" and plataform != "TikTok":
                print("Invalid option")
            else:
                break
        while True:
            script_default = input("Special Script or Default? (OPTIONS: script, default) : ")
            if script_default != "script" and script_default != "default":
                print("Invalid option")
            else:
                break
        openai_key = input("Insert OpenAi key: ")
        script = ""
        if script_default == "script":
            script = input("Please give your desired narrative structure: ")
        word_amount = input("Amount of words: (ONLY ACCEPTS INTEGERS) : ")

        video_file = video_formation(title, main_theme, script_default, word_amount, music_prompt, script, openai_key, mode)   
        uploading(video_file, plataform)


        
        while True:
            again = input("Again? (OPTIONS: yes, no) : " )
            if again != "yes" and again != "no":
                print("Invalid option")
            else:
                break
        if again == "no":
            break





def video_formation(title, main_theme, script_default, word_amount, music_prompt, script, openai_key, mode):
    music = music_generation(music_prompt)
    full_text = text_generation(title, main_theme, script_default, word_amount, script, openai_key, mode)
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
    while True:
        review = input("Preview video first? (OPTIONS: yes, no) : ")
        if review != "yes" and review != "no":
            print("Invalid option")
        else:
            break
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





def text_generation(title, main_theme, script_default, word_amount, script, openai_key, mode):
    client = OpenAI(
        #api_key=os.environ.get(openai_key)
    api_key=os.environ.get("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")
    )

    


    if mode == "Random":
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
        {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
        {"role": "user", "content": f"Please make a video about a random topic but just give your lines without any script structure element. You cannot say more than {word_amount} words"},
        ]
        )
    elif script_default == "default":
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
        {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
        {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words"},
        ]
        )
    else:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
        {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
        {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words. Also, please follow the following structure: {script}"},
        ]
        )

    return response['choices'][0]['message']['content']


def background_generation(text):

    client = OpenAI(
        #api_key=os.environ.get(openai_key)
    api_key=os.environ.get("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")
    )

    response = client.images.generate(
    model="dall-e-3",
    prompt= text,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    
    


    





















if __name__ == "__main__":
    main()

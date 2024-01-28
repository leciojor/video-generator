from moviepy.editor import *
from openai import OpenAI
import googleapiclient
from gtts import gTTS
from pydub import AudioSegment


#debug
#finish youtube API
#implement music generation
#add voice specifications
#add frame amount specification for each individual video unit


def main():
    while True:
        while True:
            mode = input("Choose mode: (OPTIONS: Random, Manual) : ")
            if mode != "Random" and mode != "Manual":
                print("Invalid option")
            else:
                break
        if mode != "Random":
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
            if video_file is not None:
                uploading(video_file, plataform_ = plataform)


            
            while True:
                again = input("Again? (OPTIONS: yes, no) : " )
                if again != "yes" and again != "no":
                    print("Invalid option")
                else:
                    break
            if again == "no":
                break
        else:
            openai_key = input("Insert OpenAi key: ")
            plataform = input('Short Content Plataform  (OPTIONS: Shorts, Reels, TikTok) : ')
            video_file = video_formation(key = openai_key, mode_ = mode)
            if video_file is not None:
                uploading(video_file, plataform_ = plataform)
            while True:
                again = input("Again? (OPTIONS: yes, no) : ")
                if again != "yes" and again != "no":
                    print("Invalid option")
                else:
                    break
            if again == "no":
                break





def video_formation(title = '', main_theme = '', script_default = '', word_amount = 0, music_prompt = '', script = '', key = '', mode_ = ''):
    music = music_generation(music_prompt)
    full_text = text_generation(title, main_theme, script_default, word_amount, script, key, mode_)
    if full_text == None:
        return None
    texts = full_text.split('.')
    texts = [title] + texts


    frames = []
    for text in texts:
        speech = text_to_speech(text)
        speech_duration = get_audio_duration(speech)
        background = background_generation(text, key, speech_duration)
        if background == None:
            return None
        clip = VideoFileClip(background)  
        txt_clip = TextClip(text, fontsize = 75, color = 'black') 
        clip = CompositeVideoClip([clip, txt_clip])
        audioclip = AudioFileClip(speech)
        frame = clip.set_audio(audioclip) 

        frames.append(frame)  

    
    final_clip = concatenate_videoclips(frames)
    #music_audio = AudioFileClip(music)

    #final_clip = final_clip.set_audio(music_audio)
    final_clip.write_videofile("final_video.mp4", codec="libx264", fps=24)
    filename = "final_video.mp4"
    return filename



def get_audio_duration(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    duration_in_seconds = len(audio) / 1000.0  
    return duration_in_seconds





def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "speech.mp3"
    tts.save(filename)
    return filename






def uploading(filename, plataform = ''):
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
        api_key=openai_key
    )

    try:

        if mode == "Random":
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about a random topic but just give your lines without any script structure element. You cannot say more than {word_amount} words and should start with a main title"},
            ]
            )
        elif script_default == "default":
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words"},
            ]
            )
        else:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words. Also, please follow the following structure: {script}"},
            ]
            )

    except OpenAI.RateLimitError as limit:
        print("You have insufficient OpenAI credits for generating this video. Please add more at https://platform.openai.com/usage")
        return None

    return response['choices'][0]['message']['content']


def background_generation(text, key, duration):

    try:

        model = "dall-e-3"
        prompt = text
        size = "1024x768"
        quality = "standard"
        num_frames = 10


        client = OpenAI(
            api_key = key
        )


        response = client.images.generate(
        model=model,
        prompt = f"Generate {num_frames} images of {prompt}, but as the same image, but in different positions (like video frames)"
        size=size,
        quality=quality,
        n=num_frames,
        )
        
        images_data = response['data']

        images = [image_info['image'] for image_info in images_data]

    except OpenAI.RateLimitError as limit:
        print("You have insufficient OpenAI credits for generating this video. Please add more at https://platform.openai.com/usage")
        return None
    
    
    return video_file













if __name__ == "__main__":
    main()

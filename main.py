from moviepy.editor import *
from openai import OpenAI
from openai import RateLimitError
import cv2
import googleapiclient
from gtts import gTTS
from PIL import Image
import io
import os
import numpy as np
import subprocess




#finish youtube API
#implement music generation
#add voice specifications - maybe
#add exception handling for when user gives wrong datatype
#implement text over video
#setup google's API input


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
            fps = int(input("Please give your desired fps (Please have in mind this will affect the video final price) : "))
            word_amount = float(input(f" Average word - price ratio: {((fps * (0.6)) * 0.018) + 0.02} dollar per word \n Amount of words: (ONLY ACCEPTS INTEGERS) : " ))
            average_price = (((fps * (0.6)) * 0.018) + 0.02)*word_amount


            price = average_price
            while True:
                proceed = input(f"Average cost for video will be {price}. Proceed? (OPTIONS: yes, no) : ")
                if proceed != "yes" and proceed != "no":
                    print("Invalid option")
                else:
                    break

            if proceed == "yes":

                video_file = video_formation(title, main_theme, script_default, word_amount, music_prompt, script, openai_key, mode, fps)   
                if video_file is not None:
                    uploading(video_file, plataform_ = plataform, fps_ = fps)
                    while True:
                        again = input("Again? (OPTIONS: yes, no) : " )
                        if again != "yes" and again != "no":
                            print("Invalid option")
                        else:
                            break

            else:
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
            while True:
                plataform = input('Short Content Plataform  (OPTIONS: Shorts, Reels, TikTok) : ')
                if plataform != "Shorts" and plataform != "Reels" and plataform != "TikTok":
                    print("Invalid option")
                else:
                    break
            
            fps = int(input("Please give your desired fps (Limited range from 1 to 4) (Please have in mind this will affect the video final price) : "))
            word_amount = int(input(f" Average word - price ratio: {((fps * (0.6)) * 0.018) + 0.02} dollar per word \n Amount of words: (ONLY ACCEPTS INTEGERS) : " ))
            average_price = (((fps * (0.6)) * 0.018) + 0.02)*float(word_amount)



            price = average_price
            while True:
                proceed = input(f"Average cost for video will be {price}. Proceed? (OPTIONS: yes, no) : ")
                if proceed != "yes" and proceed != "no":
                    print("Invalid option")
                else:
                    break

            if proceed == "yes":

                video_file = video_formation(key = openai_key, mode_ = mode, word_amount_= word_amount, fps_ = fps)
                if video_file is not None:
                    uploading(video_file, plataform_ = plataform, fps_ = fps)
                    while True:
                        again = input("Again? (OPTIONS: yes, no) : " )
                        if again != "yes" and again != "no":
                            print("Invalid option")
                        else:
                            break
                if again == "no":
                    break
                    
            else:
                while True:
                    again = input("Again? (OPTIONS: yes, no) : " )
                    if again != "yes" and again != "no":
                        print("Invalid option")
                    else:
                        break
                if again == "no":
                    break




def video_formation(title = '', main_theme = '', script_default = '', word_amount_ = 0, music_prompt = '', script = '', key = '', mode_ = '', fps_ = 0):
    music = music_generation(music_prompt)
    full_text = text_generation(title, main_theme, script_default, word_amount_, script, key, mode_)
    if full_text == None:
        return None
    texts = full_text.split('.')
    if title != '':
        texts = [title] + texts
    else:
        texts = texts


    frames = []
    for text in texts:
        speech = text_to_speech(text)
        speech_duration = get_audio_duration(speech)
        background = background_generation( text, key, speech_duration, fps_)
        if background == None:
            return None
        clip = VideoFileClip(background)  
        #txt_clip = TextClip(text, fontsize = 75, color = 'black') 
        #clip = CompositeVideoClip([clip, txt_clip])
        audioclip = AudioFileClip(speech)
        frame = clip.set_audio(audioclip) 

        frames.append(frame)  

    
    final_clip = concatenate_videoclips(frames)
    #music_audio = AudioFileClip(music)

    #final_clip = final_clip.set_audio(music_audio)
    final_clip.write_videofile("final_video.mp4", codec="libx264", fps=fps_)
    filename = "final_video.mp4"
    return filename



def get_audio_duration(file_path):
    audio_clip = AudioFileClip(file_path)

    duration_seconds = audio_clip.duration

    return int(duration_seconds)






def text_to_speech(text_):
    tts = gTTS(text=text_, lang='en')
    filename = "speech.mp3"
    tts.save(filename)
    file_path = os.path.abspath("speech.mp3")
    return file_path






def uploading(filename, plataform_ = '', fps_ = 0):
    while True:
        review = input("Preview video first? (OPTIONS: yes, no) : ")
        if review != "yes" and review != "no":
            print("Invalid option")
        else:
            break
    if review == "yes":
        clip = VideoFileClip(filename) 
        clip.preview(fps = fps_) 


    if plataform_ == "Shorts":
        title = input("Video title: ")
        description = input("Video description: ")
        keywords = input("Video Keywords: ")
        privacy = input("Video privacy status: (private, public)")
        category = "22"
        command = ["python", "upload_video.py",
           f"--file={filename}",
           f"--title={title}",
           f"--description={description}",
           f"--keywords={keywords}",
           f"--category={category}",
           f"--privacyStatus={privacy}"]

        subprocess.run(command)



    elif plataform_ == "Reels":
        print("Reels is not an available plataform yet")
    elif plataform_ == "TikTok":
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
            max_tokens=int(word_amount),  
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about a random topic but just give your lines without any script structure element. You cannot say more than {word_amount} words"},
            ]
            )
        elif script_default == "default":
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            max_tokens=int(word_amount),
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words"},
            ]
            )
        else:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            max_tokens=int(word_amount),
            messages=[
            {"role": "system", "content": "You are a short content youtuber talking about" + main_theme},
            {"role": "user", "content": f"Please make a video about {main_theme} but just give your lines without any script structure element. You cannot say more than {word_amount} words. Also, please follow the following structure: {script}"},
            ]
            )

        final_response = response.choices[0].message.content
        print("Script text: ")
        print(final_response)

        return final_response
    
    except RateLimitError as limit:
        print("You have insufficient OpenAI credits for generating this video. Please add more at https://platform.openai.com/usage")
        return None



def background_generation(text, key, duration, fps):

    try:

        model = "dall-e-2"
        prompt = text
        size = "512x512"
        quality = "standard"
        num_frames = int(fps * duration)


        client = OpenAI(
            api_key = key
        )


        response = client.images.generate(
        model=model,
        prompt = f"Generate {num_frames} images of {prompt}, but as the same image, but in different positions (like video frames)", 
        size=size,
        quality=quality,
        n=num_frames,
        )
        
        images_data = response.data

        images = [ image_info.url for image_info in images_data]

    except RateLimitError as limit:
        print("You have insufficient OpenAI credits for generating this video. Please add more at https://platform.openai.com/usage")
        return None
    


    base_video = ColorClip(size=(512, 512), color=(255, 255, 255), duration=duration)
    base_video.write_videofile("blank_video.mp4", codec="libx264", fps=fps)
    for image in images:
        image_clip = ImageClip(image, duration=duration/num_frames)
        base_video = concatenate_videoclips([image_clip, base_video])

    base_video.write_videofile("output_video.mp4", codec="libx264", fps=fps)

    video_file = "output_video.mp4"
    
    
    return video_file













if __name__ == "__main__":
    main()

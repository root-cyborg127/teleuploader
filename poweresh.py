import os
import asyncio
import hashlib
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.error import TelegramError
from colorama import Fore, Style, init
from pymongo import MongoClient
import time

# Initialize colorama
init(autoreset=True)

# MongoDB setup
client = MongoClient('mongodb+srv://heheboiii:Prachi1419@cluster0.ola2n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['video_upload_db']
videos_collection = db['uploaded_videos']

# Global variable to keep track of the number of upload attempts
uploaded_videos_count = 0

# Function to generate a unique ID for a video based on its name
def generate_video_id(video_name):
    return hashlib.md5(video_name.encode()).hexdigest()

# ASCII art banner with upload count and custom text
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before printing the banner
    print(Fore.LIGHTCYAN_EX + """
███████████    ████                           █████  █████       ████                      
░█░░░███░░░█   ░░███                          ░░███  ░░███       ░░███                    
░   ░███  ██████░███  ██████                   ░███   ░███████████░███  ██████ ██████   ███████  ██████ ████████  
    ░███ ███░░██░███ ███░░███    ██████████    ░███   ░██░███░░██░███ ███░░██░░░░░███ ███░░███ ███░░██░░███░░███ 
    ░███░███████░███░███████    ░░░░░░░░░░     ░███   ░███░███ ░██░███░███ ░██████████░███ ░███░███████ ░███ ░░░  
    ░███░███░░░ ░███░███░░░                    ░███   ░███░███ ░██░███░███ ░█████░░███░███ ░███░███░░░  ░███      
    ████░░██████████░░██████                   ░░████████ ░███████████░░█████░░███████░░███████░░██████ █████   
   ░░░░░ ░░░░░░░░░░░ ░░░░░░                     ░░░░░░░░  ░███░░░░░░░░ ░░░░░░ ░░░░░░░░ ░░░░░░░░ ░░░░░░ ░░░░░    
                                                          ░███                                                   
                                                          █████                                                  

                                                         ░░░░░                                                  

    """ + Style.BRIGHT + Fore.YELLOW + f"     Uploaded Videos: {uploaded_videos_count}\n" + Style.RESET_ALL)
    print(developed_by)

# Developed by message
developed_by = f"{Fore.LIGHTGREEN_EX}Developed by: {Fore.LIGHTCYAN_EX}VISHWAJITH SHAIJUKUMAR {Fore.LIGHTGREEN_EX}@root-cyborg127{Style.RESET_ALL}"

# Function to check if the video is already logged in the database
def is_video_logged(video_name):
    video_id = generate_video_id(video_name)
    return videos_collection.find_one({"video_id": video_id}) is not None

# Function to log the uploaded video to the database
def log_uploaded_video(video_name):
    video_id = generate_video_id(video_name)
    videos_collection.insert_one({"video_id": video_id, "video_name": video_name})
    print(Fore.WHITE + f"\nInfo of {Fore.LIGHTGREEN_EX}{video_name}{Fore.WHITE} uploaded to the database!")

async def send_video(bot, chat_id, video_path, caption=None):
    """Asynchronous function to send a video to Telegram."""
    global uploaded_videos_count
    video_name = os.path.basename(video_path)

    # Check if the video is already in the database
    if is_video_logged(video_name):
        print(Fore.YELLOW + f"\nVideo {Fore.LIGHTGREEN_EX}{video_name}{Fore.YELLOW} is already logged in the database. Skipping upload.")
        return  # Skip the upload if already in the database

    try:
        with open(video_path, 'rb') as video_file:
            print(Fore.CYAN + f"\nUploading {video_name}...")
            await bot.send_video(chat_id=chat_id, video=video_file, caption=caption or video_name)
            print(Fore.GREEN + f"\nUploaded {video_name} successfully!")
    except TelegramError as e:
        print(Fore.RED + f"\nFailed to upload {video_name}: {e}")
    except Exception as e:
        print(Fore.RED + f"\nAn error occurred with file '{video_name}': {e}")
    finally:
        log_uploaded_video(video_name)  # Log the video to the database regardless of success or failure
        uploaded_videos_count += 1  # Increment the count regardless of success or failure
        print_banner()  # Update the banner after each upload attempt

async def read_video_files(folder_path):
    """Read video files from a folder."""
    return [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]

async def send_videos_from_folder(bot_tokens, chat_id, folder_path, caption=None):
    """Function to send all videos from a folder using multiple bots."""
    video_files = await read_video_files(folder_path)

    if not video_files:
        print(Fore.YELLOW + "No video files found in the folder.")
        return

    tasks = []
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        # Create a task for each bot to upload the video
        for bot_token in bot_tokens:
            bot = Bot(token=bot_token)
            tasks.append(send_video(bot, chat_id, video_path, caption))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

async def handle_start(update: Update, context):
    """Handle the /start command and send the audio file."""
    chat_id = update.message.chat_id
    audio_url = 'https://audio.jukehost.co.uk/F0B0aVSbrVNdeXZWCtvLyLBzIuQC1sEp'
    
    # Send the audio file
    await context.bot.send_audio(chat_id=chat_id, audio=audio_url)
    await update.message.reply_text(f"Hello! Here is your welcome audio 🎶.")

# Main function to run the bot
async def main():
    bot_tokens = [
        '8192317893:AAEgrAWaF_ps8Nqtw4b5grqlB9QpasKYliE',  # Your first bot's token
        '8039681654:AAFw2_Nrw5d1N-C1cJ8AeBPz8OmqCMamXYY',
        '7825838222:AAFosoYnXOaDcQ03q4-ch51uqb21boQ8J-w',
        '8144289061:AAGz9xIm_LHMeVTV05fU5RGSeazy3776uUU',
        '8132374686:AAGB7DHuiEFN2HaqDGwlMYpCiHj4rr6HKuc',  # Add more bot tokens here
        # ...
    ]
    chat_id = '-1002421938077'  # Your group chat ID
    folder_path = 'D:\\TeraBoxDownload\\10-10-2024 indian'  # Your video folder path
    caption = f'@Thankkanchettan_bot 👨‍💻'  # Optional caption for each video

    # Create the Application (telegram bot handler)
    application = Application.builder().token(bot_tokens[0]).build()

    # Add command handler for /start
    application.add_handler(CommandHandler('start', handle_start))

    # Initialize the application before starting it
    await application.initialize()

    # Start the bot
    await application.start()

    # Print the initial banner
    print_banner()

    while True:
        # Start uploading videos
        await send_videos_from_folder(bot_tokens, chat_id, folder_path, caption)

        # Sleep for a while before checking for new videos again
        await asyncio.sleep(60)  # Check for new videos every 60 seconds

    # Block until the user stops the bot
    await application.stop()

if __name__ == '__main__':
    # Run the async main function using asyncio
    asyncio.run(main())

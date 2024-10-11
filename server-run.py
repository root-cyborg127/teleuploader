import os
import asyncio
import hashlib
from telegram import Bot
from telegram.error import TelegramError
from colorama import Fore, Style, init
from pymongo import MongoClient

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
    ░███ ███░░██░███ ███░░███    ██████████    ░███   ░██░░███░░██░███ ███░░██░░░░░███ ███░░███ ███░░██░░███░░███ 
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
    print(Fore.WHITE + f"\nInfo of {Fore.LIGHTGREEN_EX}{video_name}{Fore.WHITE} uploaded to the database !")

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

async def send_videos_from_folder(bot_token, chat_id, folder_path, caption=None):
    """Function to send all videos from a folder one by one with delays."""
    bot = Bot(token=bot_token)

    # Directly await the video files reading
    video_files = await read_video_files(folder_path)

    if not video_files:
        print(Fore.YELLOW + "No video files found in the folder.")
        return

    # Upload videos one by one with delay
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        await send_video(bot, chat_id, video_path, caption)
        await asyncio.sleep(15)  # Delay of 15 seconds between each video upload

# Main function to run the bot
async def main():
    bot_token = '8192317893:AAEgrAWaF_ps8Nqtw4b5grqlB9QpasKYliE'  # Your bot's token
    chat_id = '-1002421938077'  # Your group chat ID
    folder_path = 'D:\\TeraBoxDownload\\10-10-2024 indian'  # Your video folder path
    caption = f'@Thankkanchettan_bot 👨‍💻'  # Optional caption for each video

    # Print the initial banner
    print_banner()

    # Start uploading videos
    await send_videos_from_folder(bot_token, chat_id, folder_path, caption)

if __name__ == '__main__':
    # Run the async main function using asyncio
    asyncio.run(main())

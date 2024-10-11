import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global variable to keep track of the number of upload attempts
uploaded_videos_count = 0

# ASCII art banner with upload count and custom text
def print_banner():
    print(Fore.LIGHTCYAN_EX + """
███████████    ████                           █████  █████       ████                     █████                 
░█░░░███░░░█   ░░███                          ░░███  ░░███       ░░███                    ░░███                  
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
# Developed by message
developed_by = f"{Fore.LIGHTGREEN_EX}Developed by: {Fore.LIGHTCYAN_EX}VISHWAJITH SHAIJUKUMAR {Fore.LIGHTGREEN_EX}@root-cyborg127{Style.RESET_ALL}"
print(developed_by)  # Print the developed by message

async def send_video(bot, chat_id, video_path, caption=None):
    """Asynchronous function to send a video to Telegram."""
    global uploaded_videos_count
    try:
        with open(video_path, 'rb') as video_file:
            print(Fore.CYAN + f"Uploading {os.path.basename(video_path)}...")
            await bot.send_video(chat_id=chat_id, video=video_file, caption=caption or os.path.basename(video_path))

            print(Fore.GREEN + f"Uploaded {os.path.basename(video_path)} successfully!")
    except TelegramError as e:
        print(Fore.RED + f"Failed to upload {os.path.basename(video_path)}: {e}")
    except Exception as e:
        print(Fore.RED + f"An error occurred with file '{os.path.basename(video_path)}': {e}")
    finally:
        uploaded_videos_count += 1  # Increment the count regardless of success or failure
        print_banner()  # Update the banner after each upload attempt

async def send_videos_from_folder(bot_token, chat_id, folder_path, caption=None):
    """Function to send all videos from a folder one at a time with delays."""
    bot = Bot(token=bot_token)

    # Get the list of all video files in the folder
    try:
        video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.mov', '.avi', '.mkv'))]

        if not video_files:
            print(Fore.YELLOW + "No video files found in the folder.")
            return

        # Upload videos one by one with delay
        for video_file in video_files:
            video_path = os.path.join(folder_path, video_file)
            await send_video(bot, chat_id, video_path, caption)
            await asyncio.sleep(15)  # Delay of 15 seconds between each video upload

    except Exception as e:
        print(Fore.RED + f"An error occurred while reading the folder: {e}")

async def send_upload_status(bot_token, chat_id):
    """Function to send status updates every 10 minutes."""
    bot = Bot(token=bot_token)
    global uploaded_videos_count
    while True:
        await asyncio.sleep(600)  # Wait for 10 minutes (600 seconds)
        try:
            status_message = f"Uploaded {uploaded_videos_count} videos so far."
            await bot.send_message(chat_id=chat_id, text=status_message)
            print(Fore.CYAN + "Status update sent.")
        except TelegramError as e:
            print(Fore.RED + f"Failed to send status update: {e}")

# Main function to run the bot
async def main():
    bot_token = '8192317893:AAEgrAWaF_ps8Nqtw4b5grqlB9QpasKYliE'  # Your bot's token
    chat_id = '-1002421938077'  # Your group chat ID
    folder_path = 'c:\\Users\\Admin\\Downloads\\Telegram Desktop\\ChatExport_2024-10-11 (2)\\instagram viral\\videos'  # Your video folder path
    caption = '@Thankkanchettan_bot 👨‍💻'  # Optional caption for each video

    # Print the initial banner
    print_banner()

    # Start the status update task
    status_task = asyncio.create_task(send_upload_status(bot_token, chat_id))

    # Start uploading videos
    await send_videos_from_folder(bot_token, chat_id, folder_path, caption)

    # Keep the program running (in case there are no more tasks to run)
    await status_task

if __name__ == '__main__':
    # Run the async main function using asyncio
    asyncio.run(main())

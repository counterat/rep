
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
import cloudinary.uploader

cloudinary.config(cloud_name = 'du73oow82', api_key = '776475952999713', api_secret='ZsEgGp0xgT1wmuBc3rB7KSZLen8')

api_id = 28840087
api_hash = '6a265aad5106ab6bad02c5e5044e73d1'
app = Client('my_account', api_id= api_id, api_hash=api_hash)

def get_random_members_of_chat(chat_id):
    with app:
        members = app.get_chat_members(chat_id)
        i=0
        members_and_avatars = {}
        for member in members:
            i += 1 
            if not member.user.is_bot:
                try:
                    file_id = (member.user.photo.small_file_id)
                    
                    
                    app.download_media(file_id, f'{i}.png')
                    upload_result = cloudinary.uploader.upload(f'downloads/{i}.png')
            
                    image_url = upload_result['secure_url']
                    username = member.user.first_name
                    members_and_avatars[username] = image_url
                except Exception as ex:
                    print(ex)
    return members_and_avatars

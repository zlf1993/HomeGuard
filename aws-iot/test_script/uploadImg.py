from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

path="/home/pi/Documents/aws-iot/Image/"
folderId='12ilLCJvXGdoMvSJ6pWSf7PLjaDSnKizI'

assert os.path.exists(path)
assert os.path.isdir(path)
imageList = os.listdir(path)
lenList= len(imageList)

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

f = drive.CreateFile({'title': imageList[lenList-1],
                      'mimeType': 'image/jpeg',
                      'parents': [{'kind': 'drive#filelink', 'id':folderId}]})

            

f.SetContentFile(path+imageList[lenList-1])
f.Upload()
os.remove(path+imageList[lenList-1])
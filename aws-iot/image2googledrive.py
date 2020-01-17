from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import os

class Image2GoogleDrive:
    def __init__(self, path="/home/pi/Documents/aws-iot/Image/", folderId='12ilLCJvXGdoMvSJ6pWSf7PLjaDSnKizI'):
        
        self.path = path
        self.folderId = folderId
        assert os.path.exists(path)
        assert os.path.isdir(path)
        self.imageList = os.listdir(path)
        self.lenList= len(self.imageList)
        
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("googleDriveCreds.txt")
        if gauth.credentials is None:
            gauth.CommandLineAuth()
            
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        
        gauth.SaveCredentialsFile("googleDriveCreds.txt")
        self.drive = GoogleDrive(gauth)
    
    def upload(self):
        f = self.drive.CreateFile({'title': self.imageList[self.lenList-1],
                      'mimeType': 'image/jpeg',
                      'parents': [{'kind': 'drive#filelink', 'id':self.folderId}]})

            

        f.SetContentFile(self.path+self.imageList[self.lenList-1])
        f.Upload()
        # os.remove(path+imageList[lenList-1])
    
if __name__ == "__main__":
    imgupload = Image2GoogleDrive()
    imgupload.upload()

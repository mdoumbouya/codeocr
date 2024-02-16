from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Load client secrets from your key file 
gauth.LoadClientConfigFile('credentials.json')

drive = GoogleDrive(gauth)

# "1a2B3c4D5e6F" is the file id of the image file 
file6 = drive.CreateFile({'id': '14sO8HMcVUnQ6zr5IpC9Sj_aCKciElZc9'}) 

# This will replace the existing file with your file
file6.GetContentFile('images/image1.jpg', mimetype='image/jpg') 
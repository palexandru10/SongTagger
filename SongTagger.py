import eyed3
import os
import re

class Tagger:
    def __init__(self,folderPath) -> None:
        self.files= {}
        self.folderPath=folderPath
        self.separators = [",", "&", "vs", 'ft.' , ' x ']
        self.pattern = '|'.join(map(re.escape, self.separators))
        self.songsInfo={}

    def readSongs(self):
        fileNames = os.listdir(self.folderPath)
        for songName in fileNames:
            self.files[songName]= {'artists':[], 'songTitle':[], 'album':[]}
        
    def processSongData(self):
        for songName in self.files:
            artists=[]
            songTitle=[]
            #split the artists and the song title
            artistsRaw,titleRaw=songName.split(' - ')
            temp= re.split(self.pattern, artistsRaw)
            for artist in temp:
                artists.append(artist.strip())

            titleRaw = titleRaw.split('.mp3')[0]
            if 'Live' in titleRaw:
                    pattern = '|'.join(map(re.escape, ["(",")"]))
                    titleRaw= re.split(pattern, titleRaw)[0]

            if "(" in titleRaw:
                if "ft." in titleRaw:
                    pattern = '|'.join(map(re.escape, ["(",")"]))
                    featuresString= re.split(pattern, titleRaw)
                    additionalArtists = featuresString[1]
                    pattern = '|'.join(map(re.escape, ["ft.",",","Remix", "&", "Edit", "Acoustic","Flip", "Mashup"])) # check what should happen if its both a ft and a remix/edit
                    additionalArtists = [elem.strip() for elem in re.split(pattern, additionalArtists) if elem]
                    if "Edit" in titleRaw or 'Flip' in titleRaw or 'Remix' in titleRaw:
                        songTitle=titleRaw
                    else:
                        songTitle= featuresString[0]
                    if(len(additionalArtists)):
                        for artist in additionalArtists:
                            if artist not in artists:
                                artists.append(artist)

                else:
                    songTitle=titleRaw

                    pattern = '|'.join(map(re.escape, ["(",")"]))
                    featuresString= re.split(pattern, titleRaw)
                    additionalArtists = featuresString[1]
                    pattern = '|'.join(map(re.escape, ["ft.",",","Remix", "&", "Edit", "Bootleg" , "Mashup", "Cover", "Nightcore", "Acoustic","Flip"])) # check what should happen if its both a ft and a remix/edit
                    additionalArtists = [elem.strip() for elem in re.split(pattern, additionalArtists) if elem]
                    songTitle= titleRaw
                    if(len(additionalArtists)):
                        for artist in additionalArtists:
                            if artist not in artists:
                                artists.append(artist)
            else:
                songTitle=titleRaw

            if 'Earth' in artists and 'Wind' in artists and 'Fire' in artists:
                artists.remove('Earth')
                artists.remove('Wind')
                artists.remove('Fire')
                artists.append('Earth, Wind & Fire')
            self.songsInfo[songName]=[artists,songTitle.strip()]

    def writeMetadata(self):
        fileNames = os.listdir(self.folderPath)
        for songName in fileNames:
            fullSongPath=self.folderPath+"\\"+songName
            songFile=eyed3.load(fullSongPath)
            if songFile.tag is None:
                songFile.initTag()

            songFile.tag.artist = '; '.join(self.songsInfo[songName][0])
            songFile.tag.title = self.songsInfo[songName][1]
            songFile.tag.save()
            
            self.files[songName]= {'artists':[], 'songTitle':[], 'album':[]}


            


tagger= Tagger(r'C:\Users\popai\Desktop\SongTagger\MP3s For Alecs')
tagger.readSongs()
tagger.processSongData()
tagger.writeMetadata()
        
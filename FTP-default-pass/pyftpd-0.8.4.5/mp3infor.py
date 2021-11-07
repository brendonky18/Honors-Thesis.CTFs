#
#   Python MPEG Information Module
#
#   (c)Eduardo Roldan, Under the GPL License
#   e-mail: trazor@adinet.com.uy
#
#   Check the included README.TXT for instructions (no many '#' comments here)

import string

info = 'v 0.2 291099'

mpeg_strings = ['2.5', '', '2', '1']
layers = ['', 'III', 'II', 'I']
bitrates_mpeg1 = [ [],
                   [-1, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
                   [-1, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
                   [-1, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448]
                 ]
                  # !! -1 = free bitrate
bitrates_mpeg2 = [ [],
                   [-1, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
                   [-1, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
                   [-1, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256]
                 ]
frequency_strings = [ [11025, 12000, 8000],
                      [],
                      [22050, 24000, 16000,],
                      [44100, 48000, 32000,]
                    ]
channel_mode_strings= ['Stereo', 'Joint Stereo', 'Dual Channel', 'Single Channel']

InvalidHeaderError = 'Can\'t read an invalid header'
NoHeaderError = 'No header present'
NoTagError = 'No id3 tag present'

#Extracted from mpg123 0.59q
genre_list = [
              "Blues", "Classic Rock", "Country", "Dance", "Disco", "Funk", "Grunge", "Hip-Hop",
              "Jazz", "Metal", "New Age", "Oldies", "Other", "Pop", "R&B", "Rap", "Reggae", "Rock",
              "Techno", "Industrial", "Alternative", "Ska", "Death Metal", "Pranks", "Soundtrack",
              "Euro-Techno", "Ambient", "Trip-Hop", "Vocal", "Jazz+Funk", "Fusion", "Trance",
              "Classical", "Instrumental", "Acid", "House", "Game", "Sound Clip", "Gospel", "Noise",
              "Alt", "Bass", "Soul", "Punk", "Space", "Meditative", "Instrumental Pop",
              "Instrumental Rock", "Ethnic", "Gothic", "Darkwave", "Techno-Industrial",
              "Electronic", "Pop-Folk", "Eurodance", "Dream", "Southern Rock", "Comedy", "Cult",
              "Gangsta Rap", "Top 40", "Christian Rap", "Pop/Funk", "Jungle", "Native American",
              "Cabaret", "New Wave", "Psychedelic", "Rave", "Showtunes", "Trailer", "Lo-Fi",
              "Tribal", "Acid Punk", "Acid Jazz", "Polka", "Retro", "Musical", "Rock & Roll",
              "Hard Rock", "Folk", "Folk/Rock", "National Folk", "Swing", "Fast-Fusion", "Bebob",
              "Latin", "Revival", "Celtic", "Bluegrass", "Avantgarde", "Gothic Rock",
              "Progressive Rock", "Psychedelic Rock", "Symphonic Rock", "Slow Rock", "Big Band",
              "Chorus", "Easy Listening", "Acoustic", "Humour", "Speech", "Chanson", "Opera",
              "Chamber Music", "Sonata", "Symphony", "Booty Bass", "Primus", "Porn Groove",
              "Satire", "Slow Jam", "Club", "Tango", "Samba", "Folklore", "Ballad", "Power Ballad",
              "Rhythmic Soul", "Freestyle", "Duet", "Punk Rock", "Drum Solo", "A Cappella",
              "Euro-House", "Dance Hall", "Goa", "Drum & Bass", "Club-House", "Hardcore", "Terror",
              "Indie", "BritPop", "Negerpunk", "Polsk Punk", "Beat", "Christian Gangsta Rap",
              "Heavy Metal", "Black Metal", "Crossover", "Contemporary Christian",
              "Christian Rock", "Merengue", "Salsa", "Thrash Metal", "Anime", "JPop", "Synthpop"
             ]


class open_mp3:
       genre_no = 0
       bitrate = 0

       ### Id3 ###

       def __init__(self, file_to_open):
            if type(file_to_open) == type(''):
                self.file = open(file_to_open)
            else:
                 self.file = file_to_open
            self.file.seek(0, 2)
            self.filesize = self.file.tell()

       def __del__(self):
            self.file.close()

       def __call__(self):
            self.sync_read_header(0, 1024)
            mpeg = self.get_mpeg_version()
            layer = self.get_layer()
            protection = self.get_protection()
            bitrate = `self.get_bitrate()`
            frequency = `self.get_frequency()`
            channel_mode = self.get_channel_mode()
            copyright = self.get_copyright()
            original = self.get_original()
            length = string.zfill(self.get_length()[1], 2) + ':' + string.zfill(self.get_length()[2], 2)
            framelength = `self.get_framelength()`

            try:
                self.read_tag()
                genre = self.get_genre()
                songname = self.songname
                artist = self.artist
                album = self.album
                year = self.year
                comment = self.comment
            except NoTagError:
                    genre = songname = artist = album = year = comment = ''

            return {'mpeg':mpeg, 'layer':layer, 'protection':protection,
                    'bitrate':bitrate, 'frequency':frequency,
                    'channel_mode':channel_mode, 'copyright':copyright,
                    'original':original, 'length':length,
                    'framelength':framelength,
                    'genre':genre, 'songname':songname, 'artist':artist,
                    'album':album, 'year':year, 'comment':comment,
                    'filesize':self.filesize}


       def read_tag(self):
            if self.filesize <= 128:
                raise NoTagError
            self.file.seek(-128, 2)
            if self.file.read(3) == 'TAG':
                self.songname = self.file.read(30)
                self.artist = self.file.read(30)
                self.album = self.file.read(30)
                self.year = self.file.read(4)
                self.comment = self.file.read(30)
                self.genre_no = ord(self.file.read(1))
                return 1
                
            else:
                 raise NoTagError

       def get_genre(self):
            try:
                return genre_list[self.genre_no]
            except IndexError:
                return 'Unknown'

       ### Header ###

       def sync_read_header(self, offset = 0, depth = 0):

            if depth == 0 or depth > self.filesize:
                depth = self.filesize

            self.file.seek(offset, 0)

            while 1:
                    while self.file.tell() < depth:

                           if ord(self.file.read(1)) != 0xff:
                               break

                           second_byte = ord(self.file.read(1))
                           if second_byte >> 5 != 0x07:
                               self.file.seek(-1, 1)
                               break

                           self.sync_byte = 255
                           self.mpeg_version = (second_byte & 0x18) >> 3  # B
                           self.layer = (second_byte & 0x06) >> 1         # C
                           third_byte = ord(self.file.read(1))
                           self.bitrate = (third_byte & 0xf0) >> 4        # E
                           self.frequency = (third_byte & 0x0c) >> 2      # F
                           self.padding = (third_byte & 0x02) >> 1        # G
                           fourth_byte = ord(self.file.read(1))
                           self.emphasis = (fourth_byte & 0x03)           # M

                           try:
                               self.check_header()
                           except InvalidHeaderError:
                                   self.file.seek(-3, 1)
                                   break
                           ctuple1 = self.mpeg_version, self.layer, self.frequency, self.emphasis
                           step_1_ = self.get_framelength()
                           self.file.seek(step_1_-4, 1)


                           try:
                               self.read_header(self.file.tell())
                           except InvalidHeaderError:
                                   self.file.seek(-(step_1_+3), 1)
                                   break
                           ctuple2 = self.mpeg_version, self.layer, self.frequency, self.emphasis

                           if ctuple1 == ctuple2:
                               return self.file.tell() - (step_1_+4)
                           else:
                                self.file.seek(-(step_1_+3), 1)
                                break
                    else:
                         raise NoHeaderError

       def read_header(self, offset = 0):

            # AAAAAAAA AAABBCCD EEEEFFGH IIJJKLMM

            self.file.seek(offset, 0)

            self.sync_byte = ord(self.file.read(1))
            
            second_byte = ord(self.file.read(1))
            self.mpeg_version = (second_byte & 0x18) >> 3        # B
            self.layer = (second_byte & 0x06) >> 1               # C
            self.protection = (second_byte & 0x01)               # D

            third_byte = ord(self.file.read(1))
            self.bitrate = (third_byte & 0xf0) >> 4           # E
            self.frequency = (third_byte & 0x0c) >> 2         # F
            self.padding = (third_byte & 0x02) >> 1           # G
            self.private = (third_byte & 0x01)                # H

            fourth_byte = ord(self.file.read(1))
            self.channel_mode = (fourth_byte & 0xc0) >> 6     # I
            self.mode_ext = (fourth_byte & 0x30) >> 4         # J
            self.copyright = (fourth_byte & 0x08) >> 3        # K
            self.original = (fourth_byte & 0x04) >> 2         # L
            self.emphasis = (fourth_byte & 0x03)              # M

            self.check_header()
            return 1

       def check_header(self):
            if self.sync_byte != 255 or self.mpeg_version == 1 or self.layer == 0\
            or self.bitrate == 15 or self.frequency == 3 or self.emphasis == 2 :
               raise InvalidHeaderError

       def get_mpeg_version(self):
            return mpeg_strings[self.mpeg_version]

       def get_layer(self):
            return layers[self.layer]

       def get_protection(self):
            if self.protection:
                return 'No'
            else:
                 return 'Yes'

       def get_bitrate(self):
            if self.mpeg_version == 3:
                  return bitrates_mpeg1[self.layer][self.bitrate]
            elif self.mpeg_version == 2 or self.mpeg_version == 0:
                  return bitrates_mpeg2[self.layer][self.bitrate]

       def get_frequency(self):
            return frequency_strings[self.mpeg_version][self.frequency]

       def get_channel_mode(self):
            return channel_mode_strings[self.channel_mode]

       def get_copyright(self):
            if self.copyright:
                return 'Yes'
            else:
                 return 'No'

       def get_original(self):
            if self.original:
                return 'Yes'
            else:
                 return 'No'

       def get_length(self):
            if self.bitrate == 0:
                return 0, 0, 0
            else:
                 const = self.get_bitrate() * 125
                 seconds = self.filesize / const
                 minutes = seconds / 60
                 seconds_part = seconds % 60
                 return seconds, minutes, seconds_part

       def get_framelength(self):
            if self.layer == 1  or self.layer == 2:
                return 144 * self.get_bitrate() * 1000 / self.get_frequency() + self.padding
            else:
                 return 12 * self.get_bitrate() * 1000 / self.get_frequency() + self.padding
                 


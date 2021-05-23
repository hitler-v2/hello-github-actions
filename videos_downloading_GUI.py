
from kivy.clock import Clock
import pytube

import os
from threading import Thread

from os import path
from kivy.core.window import Window

from threading import Thread
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder  # noqa
from kivymd.app import MDApp  # noqa
from kivymd_extensions.akivymd.uix.statusbarcolor import (  # noqa
    change_statusbar_color,
)

KV = """
#:import MDFillRoundFlatIconButton kivymd.uix.button.MDFillRoundFlatIconButton
FloatLayout:
    padding: "10dp"
    MDLabel:
        markup :True
        text: "[color=#e60000][size=20]Download from Youtube[/size][/color]"
        pos_hint: {"center_x":0.68,"center_y":0.95}
        bold: True

    MDIconButton:
        icon: 'youtube'
        theme_text_color: "Error"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x": .1 , "center_y": 0.95}

    AsyncImage:
        id: thumbnail
        pos_hint: {"center_y":0.75, "center_x":0.5}
        size_hint: [1.9, 0.3]
        source: ''

    Label:
        id: title
        text: "video title".title()
        size_hint: [None, None]
        size: self.texture_size
        pos_hint: {"center_y":0.57, "center_x":0.5}
        font_size: "20"
        bold: True
        color: [0,0,0,1]
    MDTextField:
        id: txt_input
        pos_hint: {"center_y":0.5, "center_x":0.5}
        bold: True
        font_size: "20sp"
        hint_text: "Link"
        required: True
        helper_text_mode: "on_error"
        helper_text: "Enter Link of video from youtube"

    AKProgressbutton:
        id: progressbutton_success
        pos_hint: {"center_x": .5, "center_y": .35}
        button: MDFillRoundFlatIconButton(text="Download  Mp3", on_release=app.downmp3 , icon="music")
        # on_release=root.success
        #on_press:
         #   app.download_video(txt_input.text)
    MDLabel:
        text:"or"
        pos_hint: {"center_x": .6, "center_y": .3}
        
    AKProgressbutton:
        id: progressbutton_failure
        pos_hint: {"center_x": .5, "center_y": .25}
        button: MDFillRoundFlatIconButton(text="Download Video", on_release=app.success , icon="video-vintage")
        # on_release=root.success
        #on_press:
         #   app.download_video(txt_input.text)

    AKRating:
        pos_hint: {'center_x': .5, 'center_y': .1}
        on_rate: print(self.get_rate())


"""

class MyApp(MDApp):
    image_loaded = False

    def build(self):
        Window.fullscreen = False
        Window.size = [360, 600]
        return Builder.load_string(KV)
    
    def success(self, *args):
        t = Thread(target=self.start_success)
        t.start()
    

    def start_success(self, *args):
        self.download_video(self.root.ids.txt_input.text)
        return self.root.ids.progressbutton_failure.success()
        


    def set_assets(self, thumbnail, title):
        self.root.ids.thumbnail.source = thumbnail
        self.root.ids.title.text = title

    def get_video(self, stream):
        if self.image_loaded == True:
            stream.download('~/Downloads')
        
        # kivymd.toast("video is downloading...", 1)

    def download_video(self, url):
        yt = pytube.YouTube(url)
        self.set_assets(yt.thumbnail_url, yt.title)
        self.image_loaded = True
        Clock.schedule_once(lambda x: self.get_video(yt.streams.first()), 4)

#####################################___mp3___######################

    def downmp3(self, *args):
        t = Thread(target=self.start_down)
        t.start()
    

    def start_down(self, *args):
        self.download_video_audio(self.root.ids.txt_input.text)
        
        return self.root.ids.progressbutton_success.success()
        


    def set_assets_audio(self, thumbnail, title):
        self.root.ids.thumbnail.source = thumbnail
        self.root.ids.title.text = title

    def get_video_audio(self, stream):
        if self.image_loaded == True:
            self.out_file = stream.download('~/Downloads')                
            # save the file
            self.base, self.ext = os.path.splitext(self.out_file)
            self.new_file = self.base + '.mp3'
            os.rename(self.out_file, self.new_file)
        
        # kivymd.toast("video is downloading...", 1)

    def download_video_audio(self, url):
        yt = pytube.YouTube(url)
        self.set_assets_audio(yt.thumbnail_url, yt.title)
        self.image_loaded = True
        Clock.schedule_once(lambda x: self.get_video_audio(yt.streams.filter(only_audio=True).first()), 4)

##############################################


if __name__ == "__main__":
    app = MyApp()
    app.run()
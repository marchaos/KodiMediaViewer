import time
import xbmc, xbmcgui, xbmcaddon

class MediaIterator:
    def __init__(self):
        pass

    def forward(self):
        pass

    def back(self):
        pass

    def getCurrUrl(self):
        pass

    def isCurrVideo(self):
        pass

    def getVideoUrl(self):
        pass


class MediaWindow(xbmcgui.WindowXMLDialog):
    def __new__(cls):
        return super(MediaWindow, cls).__new__(cls, "ViewerWindow.xml", xbmcaddon.Addon(id='script.module.mediaviewer').getAddonInfo('path'))

    def __init__(self):
        self.img = None
        # Stops the menus showing through whilst images are loading
        self.blackOverlay = None
        self.playButton = None
        self.iterator = None
        self.player = MediaWindowPlayer(self)
        self.isVideoPlaying = False

    def onInit(self):
        self.blackOverlay = self.getControl(1)
        self.img = self.getControl(2)
        self.playButton = self.getControl(3)
        self.setContent()

    def setMediaIterator(self, iterator):
        self.iterator = iterator

    def onAction(self, action):

        if action == xbmcgui.ACTION_MOVE_LEFT:
            self.iterator.back()
            self.setContent()
        elif action == xbmcgui.ACTION_MOVE_RIGHT:
            self.iterator.forward()
            self.setContent()
        elif action == xbmcgui.ACTION_SELECT_ITEM or action == xbmcgui.ACTION_ENTER or action == xbmcgui.ACTION_PLAY:
            self.playVideo()
        elif action == xbmcgui.ACTION_STOP \
                or action == xbmcgui.ACTION_PREVIOUS_MENU or action == xbmcgui.ACTION_NAV_BACK:
            if self.isVideoPlaying:
                self.stopVideo()
            else:
                self.close()

    def playVideo(self):
        if self.iterator.isCurrVideo():
            self.playButton.setVisible(False)
            self.player.play(item=self.iterator.getVideoUrl())

    def stopVideo(self):
        self.player.stop()

    def onPlayBackStarted(self):
        # This sleep prevents seeing the main background.
        time.sleep(0.1)
        self.blackOverlay.setVisible(False)
        self.img.setVisible(False)
        self.isVideoPlaying = True

    def onPlayBackStopped(self):
        self.isVideoPlaying = False
        self.playButton.setVisible(True)
        self.img.setVisible(True)
        self.blackOverlay.setVisible(True)

    def setContent(self):
        self.img.setImage(self.iterator.getCurrUrl(), True)

        if self.iterator.isCurrVideo():
            self.playButton.setVisible(True)
        else:
            self.playButton.setVisible(False)


# Class to capture callbacks for when video has started / stopped
class MediaWindowPlayer(xbmc.Player):

    def __new__(cls, *args, **kwargs):
        return super(MediaWindowPlayer, cls).__new__(cls)

    def __init__(self, mediaWindow, *args, **kwargs):
        self.mediaWindow = mediaWindow
        super(MediaWindowPlayer, self).__init__(*args, **kwargs)

    def onPlayBackStarted(self):
        self.mediaWindow.onPlayBackStarted()

    def onPlayBackStopped(self):
        self.mediaWindow.onPlayBackStopped()

    def onPlayBackEnded(self):
        self.mediaWindow.onPlayBackStopped()


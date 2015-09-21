# KodiMediaViewer

The current built-in slideshow viewer in Kodi suffers from an issue where it attempts to read all images in a
directory before presenting them. This can be extremely time consuming and can take more tahn 30 seconds in some cases, depending on the directory size. 

KodiMediaViewer improves on this by only loading 1 image or video at a time, which means slideshows load instantly. This is especially useful for addons that integrate with online image sites like Flickr, Google+ etc. 

Futhermore it allows for slideshows to load images from additional pages so that a whole photo set of images can be viewed without having go to another directory fisrt and starting the slideshow again. 

# How to use

Implement you own MediaIterator

```
class FlickrMediaIterator(mediaviewer.MediaIterator):

    def __init__(self, photoset, index):
      self.photoset = photoset
      self.currIndex = index

    def forward(self):
        self.currIndex += 1
        # load next page if necessary

    def back(self):
        self.currIndex -= 1
        # load previous page if necessary

    def getCurrUrl(self):
        return MyPhotoAPI.getImageURL(self.photoset, self.currIndex)

    def isCurrVideo(self):
        return MyPhotoAPI.isImage(self.photoset, self.currIndex)

    def getVideoUrl(self):
        return MyPhotoAPI.getVideoURL(self.photoset, self.currIndex)
```

Create a MediaWindow when an directory item is clicked

```
photoset = args[0]
index = args[1]
window = MediaWindow(MyPhotoIterator(photoset, index))
window.doModal()
```

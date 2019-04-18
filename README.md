# pixabay-py
A simple Python 3 Wrapper Around The PixaBay Api.

The [Pixabay API](https://pixabay.com/api) is a free api that allows developers free access to pixabay's database of free stock images.
The API itself is pretty easy to use, however there are _quite_ a lot of parameters that need filling in and it may be quite tiresome and frankly time-consuming sometimes to have to fill everything in over and over again.

This is where this wrapper comes in, prettty simple to use, and has most of the defaults set for you.So you mostly don't have to do the work.
In addition to giving you access to the pixabay database, this wrapper also contains functions to download the images in different sizes.

Do give it a try and hopefully contribute to the project, pull requests are welcome :)

# Example Usage

```
from pyxabay.pixabay import PixaBay
import os

key = 'YOUR_API_KEY'\#Get one for free here: https://pixabay.com/api

bay = PixaBay(key=key)
imgs = bay.get_images(search='cats and dogs')
```
This will return 20 images associated with 'cats and dogs'
The `get_images` function accepts quite a number of arguments. For the full list of arguments and their corresponding accepted values, visit [pixabay](https://pixabay.com/api)

## Download All Image Results
```
save_path = os.getenv('HOME')
imgs.download_hits(save_path)
```
This will download all the images returned and save them toyour `HOME` folder

## Download An Image At Random

```
imgs.download_random(save_path)
```
This will pick an image at random from the returned list and download it to your `HOME` folder
## Get Image Data

```
img = imgs.get_img(0)
img.get_img_attr('user')
```
This will get the first image on the results list and return the artist who uploaded the image

## Download an image

```
img.download(save_path, size='large')
```
Downloads the image to your `HOME` folder.
The param `size` should be one of 'large', 'preview', 'web', 'default'

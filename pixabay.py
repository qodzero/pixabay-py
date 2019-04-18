import requests as req
from os.path import join
from random import randint
import sys

class PixaBay(object):
    '''
        PixaBay - python wrapper to query the pixabay website
        
        ``desc``:
                takes in an api key from pixabay and allows you
                to search for photos
        ``param``:
                key<str> - the api key used by the developer
                visit https://pixabay.com/api/ to get one, it's free
        ``Method``:
            get_images(self,search, **) - query pixabay and return all images
            matching your search
    '''
    def __init__(self, key):
        
        self.base_url = 'https://pixabay.com/api/'
        self.key = key
        
    def get_images(self, search,per_page=20,image_type='photo',pretty='false',category='backgrounds',minWidth=64,minHeight=64,orientation='horizontal',safesearch='true',page=1,order='popular',lang='en',editors_choice='false'):
        '''
            get_images(self, search,per_page=20,image_type='photo',pretty='false',category='backgrounds',minWidth=64,minHeight=64,orientation='horizontal',safesearch='true',page=1,order='popular',lang='en',editors_choice='false') --> PixaCollection

            ``param``:
                    search<str> - your search terms e.g 'woman using laptop'
            ``param``:
                    The rest of the params are not required but if you'd
                    like to know more about them visit https://pixabay.com/api/

            ``Example``:
                    images = bay.get_images(search='tiger hd background')#returns a PixaCollection instance
                    images.download_hits('./')#will download all the image results 
        '''
        search = search.replace(' ','+')
        url = '?'.join([self.base_url,'key=%s&q=%s&image_type=%s&pretty=%s&category=%s&minWidth=%s&minHeight=%s&orientation=%s&safesearch=%s&order=%s&page=%s&per_page=%s&lang=%s&editors_choice=%s'%(self.key,search,image_type,pretty,category,minWidth,minHeight,orientation,safesearch,order,page,per_page,lang,editors_choice)])

        r = req.get(url).json()
        import pickle
        with open('test.pb', 'wb') as f:
            pickle.dump(r, f)

        return PixaCollection(r)
    
class PixaCollection(object):
    '''
        PixaCollection - the class returned by `PixaBay`` class.
                    One should never have to use this class explicitly
                    -The class will contain all data you need to work
                    with the pixabay results as well as some utility functions
                    to help you do popular tasks easily
        ``param``:
                image_data - data returned by PixaBay().get_images()
        
        ``Methods``:
            download_hits(self, path) - download all the images
            
            download_random(self, path) - download a single image at random
            
            get_img(self, img_no) - return all information pertaining 
            to a specific image
    '''
    def __init__(self, image_data):
        self.image_data = image_data

        self.total_hits = self.image_data['totalHits']
        self.total = self.image_data['total']
        self.hits = self.image_data['hits']

    def download_hits(self, path):
        '''
            download_hits(self, path)
            download all the images returned by the PixaBay.get_images() function

            ``param``:
                    path<str> - the path where the images will be saved
            ``example``:
                    images = bay.get_images()
                    images.download_hits('path/to/save_folder')
        '''
        
        for i,hit in enumerate(self.hits):
            tgt_img = hit['largeImageURL']
            ext = tgt_img[tgt_img.rfind('.'):]
            tags = hit['tags'].split(',')
            name = '_'.join([hit['user'], tags[0], str(i)])+ext
            image = req.get(tgt_img).content

            with open(join(path,name), 'wb') as img_base:
                img_base.write(image)


    def download_random(self, path):
        '''
            download_random(self, path)

            download a random image from the returned results
            Downloads only one image from the list, useful for testing or
            when you just need a quick image to work with

            ``param``:
                path<str> - the path to save the image to
            ``example``:
                    images = bay.get_images()
                    images.download_random('path/to/save_folder')
        '''
        tgt_idx = randint(0,len(self.hits))
        hit = self.hits[tgt_idx]

        tgt_img = hit['largeImageURL']
        ext = tgt_img[tgt_img.rfind('.'):]
        tags = hit['tags'].split(',')
        name = '_'.join([hit['user'], tags[0], str(i)])+ext
        image = req.get(tgt_img).content

        with open(join(path,name), 'wb') as img_base:
            img_base.write(image)

    def get_img(self, img_no):
        '''
            get_img(self, img_no) --> PixaImage

            get an image from the api call results and
            return all the info for that image.

            ``param``:
                img_no<int> - the index of the image to get
                Should be between 0 - len(returned_results) 
        '''
        try:
            tgt_img = self.hits[img_no]
        except Exception as e:
            print('Image Index Should Be Within 0 - %s: \n%s'%(len(self.hits),e))
            sys.exit()
        
        return PixaImage(tgt_img)

class PixaImage(object):
    '''
        PixaImage - the class contains all the data of an image
        exposed by the api

        ``param``:
            img_data<str> - all the data of the image 
            as returned by PixaCollection.get_img()

        ``Methods``:
            get_img_attr(self, attr='id') - returns an attribute of an image 

            download(self, path, size='default') - download this image   
    '''
    def __init__(self, img_data):

        self.img_data = img_data

    def get_img_attr(self, attr='id'):
        '''
            get_img_attr(self, attr='id')

            Get an image's attribute provided by the pixabay api
            Make sure you query an attribute that exists in the api website
            
            ``example``:
                uploaded_by = get_img_attr('user')#returns the photographer
        '''
        try:
            return self.img_data[attr]
        except Exception as e:
            print("Attribute Doesn't Exist, Should be one of:")
            for k in self.image_data.keys():
                print(k)
            print(e)
    
    def download(self, path, size='default'):
        '''
            download(self, path, size='default')

            download the image to tyour disk

            ``param``:
                path<str> - the path to save the file to
            ``param``:
                size<size> - the size to download the image in.
                Should be one of default,preview,web,large
        '''
        if size == 'large':
            s = 'largeImageURL'
        elif size == 'preview':
            s = 'previewURL'
        elif size == 'web':
            s = 'webformatURL'
        elif size == 'default':
            s = 'imageURL'
        else:
            sys.exit('Invalid Size Option, should be one of:\n largeImageURL, previewURL, webformatURL, imageURL')
        
        tgt_img = self.image_data[s]
        ext = tgt_img[tgt_img.rfind('.'):]
        tags = self.image_data['tags'].split(',')
        name = '_'.join([self.image_data['user'], tags[0], str(i)])+ext
        image = req.get(tgt_img).content

        with open(join(path,name), 'wb') as img_base:
            img_base.write(image)

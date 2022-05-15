import logging

from model import Model
from scrape import get_next_url, scrape_apple_music, get_image
from twitter import send_tweet

def main():
    model = Model() # instantiate resnet50 model

    url = get_next_url() # retrieve random url from csv
    album = scrape_apple_music(url) # scrape apple music for title and cover
    album_title = album.album_title
    img = get_image(album.image_url) # get image for prediction and download for tweeting

    model_result = model.img_predict(img) # pass image through model
    prediction = model_result.prediction
    confidence = model_result.confidence
    formatted = f'{album_title} \nImage prediction: {prediction} \nConfidence: {confidence}' # format tweet    

    send_tweet(formatted)
    logging.info(f"Tweet sent for {album_title}, {prediction}")


if __name__ == '__main__':
    main()

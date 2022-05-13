from prediction import Model
from scraping import get_next_url, scrape_apple_music, get_image

def prediction_pipeline():
    model = Model()

    url = get_next_url()
    album = scrape_apple_music(url)
    album_title = album.album_title
    img = get_image(album.image_url)

    model_result = model.img_predict(img)
    prediction = model_result.prediction
    confidence = model_result.confidence

    return album_title, prediction, confidence

def format_tweet(album_title: str, prediction: str, confidence: str):
    pass

print(prediction_pipeline())
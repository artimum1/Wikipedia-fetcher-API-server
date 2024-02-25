# from flask import Flask, jsonify
# import requests
# from bs4 import BeautifulSoup
# from apscheduler.schedulers.background import BackgroundScheduler

# app = Flask(__name__)

# def scrape_wikipedia():
#     response = requests.get("https://en.wikipedia.org/wiki/Main_Page")
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')

#     def find_text(element_id):
#         element = soup.find('div', {'id': element_id})
#         return element.text.strip() if element else 'Not found'

#     featured_picture = find_text('mp-upper')
#     featured_list = find_text('mp-upper')
#     on_this_day = find_text('mp-upper')
#     did_you_know = find_text('mp-upper')
#     in_the_news = find_text('mp-upper')
#     featured_article = find_text('mp-upper')

#     scraped_data = {
#         'featured_picture': featured_picture,
#         'featured_list': featured_list,
#         'on_this_day': on_this_day,
#         'did_you_know': did_you_know,
#         'in_the_news': in_the_news,
#         'featured_article': featured_article
#     }

#     return scraped_data

# scheduler = BackgroundScheduler()
# scheduler.add_job(scrape_wikipedia, 'cron', hour=8)
# scheduler.start()

# @app.route('/get_wikipedia_data', methods=['GET'])
# def get_wikipedia_data():
#     data = scrape_wikipedia()
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def scrape_wikipedia():
    response = requests.get("https://en.wikipedia.org/wiki/Main_Page")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    def find_text(element_id):
        element = soup.find('div', {'id': element_id})
        return element.text.strip() if element else 'Not found'

    def find_image_src(element_id):
        element = soup.find('div', {'id': element_id})
        image = element.find('img') if element else None
        return image['src'] if image and 'src' in image.attrs else 'Image not found'

    left = find_text('mp-left')
    right = find_text('mp-right')
    lower = find_text('mp-lower')

    leftimg = find_image_src('mp-left')
    rightimg = find_image_src('mp-right')
    lowerimg = find_image_src('mp-lower')

    scraped_data = {
        'featured_article': {
            'text': left,
            'image_src': "https:"+leftimg
        },
        'in_the_news': {
            "text":right,
            "image_src": "https:"+rightimg
            },

        'on_this_day': {
            "text":lower,
            "image_src": "https:"+lowerimg
            },

    }

    return scraped_data

scheduler = BackgroundScheduler()
scheduler.add_job(scrape_wikipedia, 'cron', hour=8)
scheduler.start()

@app.route('/get_wikipedia_data', methods=['GET'])
def get_wikipedia_data():
    data = scrape_wikipedia()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

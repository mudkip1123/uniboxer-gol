from mastodon import Mastodon
from uni import GameOfLife

import configparser
import os
import urllib.request

config = configparser.ConfigParser()
config.read(['config.ini', 'config.priv.ini'])

Mastodon.create_app(
    "Uniboxer's Game of Life",
    api_base_url="https://botsin.space",
    scopes=['read', 'write', 'follow'],
    to_file="tok.to")

mastodon = Mastodon(
    client_id=config['MASTO']['CLIENT_ID'],
    client_secret=config['MASTO']['CLIENT_SECRET'],
    api_base_url="https://botsin.space")

mastodon.log_in(
    username=config['MASTO']['USERNAME'],
    password=config['MASTO']['PASSWORD'],
    to_file="tok.to",
    scopes=['read', 'write', 'follow'])

post = mastodon.account_statuses(config['MASTO']['UNIBOXER'], limit=1)[0]
url = post['media_attachments'][0]['url']
postid = post['id']

mastodon.status_favourite(postid)

urllib.request.urlretrieve(url, filename="src.PNG")
print("Downloaded latest image")


game = GameOfLife(N=350, T=200, img="src.PNG")
print("Beginning simulation...")
game.play()

print("Simulation complete. saving GIF")
os.system("convert -loop 0 -delay 5 *.Png out.gif")
os.system("rm *.Png")
print(":toot:")

media = mastodon.media_post("out.gif")['id']
print("gif uploaded to servers")


toot = mastodon.status_post("@uniboxer@botsin.space", in_reply_to_id=postid, media_ids=[media], spoiler_text="flashing colors")
mastodon.status_reblog(toot['id'])
print("toot'd and boost'd. gg.")

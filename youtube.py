from socialreaper import Youtube

ytb = Youtube("AIzaSyCctLOAXjNrWNtK1HPrm2gJhiI0XbFXO0o")

channel_id = ytb.api.guess_channel_id("altered")[0]['id']

# comments = ytb.channel_video_comments(channel_id, video_count=500, 
#     comment_count=100000, comment_text=["prize", "giveaway"], 
#     comment_format="plainText") 
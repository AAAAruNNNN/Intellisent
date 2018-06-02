from socialreaper import Facebook

fbk = Facebook("EAACEdEose0cBAFNz2yFhu8rGiVLuP6bpoFWsrkkrEl6cunlcJY1HLOoOGUuOjDl5dDibv85gL5Y1vZCjhgDZB4rjkDZCm3lO1uRtNNYGruDYZAk6nZBLKb6Pjrx3hy2HZA3fVDZApi2MaosJXxPZBFRdRgNi2mRQDYq7pZAl04wfHshyk0mJNDuzqHkKbmK5IGDIZD")

comments = fbk.page_posts_comments("altcarb", post_count=10, 
    comment_count=100000)

for comment in comments:
    print(comment['message'])

    

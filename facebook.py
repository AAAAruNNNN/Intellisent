from socialreaper import Facebook

fbk = Facebook("EAACEdEose0cBANzavhusw5QbxOdv6kAaZCobVDZBQEhzNZC68ptBMPQrrPLDHDe5ZAaF7iZBkbjDFH3XQD9hr8xUzO8uCZByuFRrpnoeyPy25rZC9cZADuInR222XguUuvSlwoRrSNoizDtRC0Jz7qXvfratNR1RQZCaTNU13SfdBzxVKpsVyzMLzDDhBwtGIlaXYbSxKzZAfnSgZDZD")

comments = fbk.page_posts_comments("altcarb", post_count=10, 
    comment_count=100000)

for comment in comments:
    print(comment['message'])

    
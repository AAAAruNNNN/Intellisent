import asyncio
from Twper import Query


async def main():
    # Example 1: A simple search using Query
    q = Query('Breaking Bad', limit=200)
    async for tw in q.get_tweets():
        # Process data
        print(tw.text)
        print(tw.tweet_id)
        print("\n\n\n\n")


# This actually runs the main function
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()
# walpyrss
A program that sets your wallpaper (wal), written in Python (py), from an 
image from a subreddit RSS feed (rss).

## Dependencies
- `feedparser` for paring through the RSS feed
- `beautifulsoup` for finding the image url from the RSS entry
- `feh` to set background

## Notes
- DOES NOT SORT BY NSFW POSTS. BE WARNED.
- Currently this pulls from r/moescape/top by month. Chanage the url under 
`RSSURL` to what subreddit you want.
    - Default: `https://www.reddit.com/r/[subreddit]/.rss`
    - Default with sorting: `https://www.reddit.com/r/[subreddit]/[hot/top/new].rss`
    - Specified duration, top sorting: 
      `https://www.reddit.com/r/[subreddit]/top.rss?t=[day/week/month/year/all]`
    - In general, you want to put `.rss` immediately before any query 
      (question mark). For example, `https://www.reddit.com/r/animewallpaper/search/.rss?sort=top&restrict_sr=on&q=flair%3ADesktop&t=month`
- There is a filter to take out any images that do not at least fit the 
specified `WIDTH` and `HEIGHT`, as well as not square or horizontal. 
Feel free to specifiy your screen size.
- The program does nothing if it can't find a suitable image (i.e. all 
vertical/mobile wallpapers if you specify horizontal).

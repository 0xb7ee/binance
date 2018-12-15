import pytumblr

client = pytumblr.TumblrRestClient(
    'pPCzriMygZj7MywIcJT3volNTgZTLmxrVqdDcgID7e8FTcQ5Yh',
    'HXiMtidPIYyQQ0BgeTaUwTLghV1xn8uQtL403faSbSJBvw2vgr',
    'Zi0L34qA7UIrnGtxVVW8ncROFl2NoohSV82FUD3dAokWKydL5s',
    'H1IeTmja6ndLHvgKBbcndjObxqLSfOc9ytNVyiURX2l0ObAels'
)
# client.dashboard()
client.follow("barebodylover")

client = pytumblr.TumblrRestClient('pPCzriMygZj7MywIcJT3volNTgZTLmxrVqdDcgID7e8FTcQ5Yh')

# Make the request
client.blog_likes('barebodylover.tumblr.com')

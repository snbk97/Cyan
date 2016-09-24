from pyshorteners import Shortener

google_urlshort_key = 'AIzaSyDLsKSMZOPqNsVk23gEZk0MbattLYWmiSc'


def urlShort(url):
    shortener = Shortener('Google', api_key=google_urlshort_key)
    return shortener.short(url)

print urlShort('https://developers.google.com/url-shortener/v1/getting_started#shorten')

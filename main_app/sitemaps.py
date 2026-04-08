from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Hum sirf un pages ko dikhayenge jahan customer ja sakta hai
        # 'create_order' ya 'delete' jaise pages sitemap mein nahi hote
        return ['home', 'about', 'shop', 'order', 'signup']

    def location(self, item):
        return reverse(item)
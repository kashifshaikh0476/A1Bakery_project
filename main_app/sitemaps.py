from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Yahan 'home' aur 'order' tere urls.py ke 'name' hone chahiye
        return ['home', 'order', 'shop', 'about'] 

    def location(self, item):
        return reverse(item)
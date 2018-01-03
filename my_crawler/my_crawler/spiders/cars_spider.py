import scrapy

DEALERS = []


class CarsSpider(scrapy.Spider):
    name = 'cars'

    def start_requests(self):
        urls = [
            'https://www.otomoto.pl/osobowe/poznan/?search%5Bprivate_business%5D=business&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=50&search%5Bcountry%5D=',  # noqa
        ]

        for i in range(2, 11):
            urls.append('{url}&page={number}'.format(url=urls[0], number=i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'cars-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        dealers = response.css(
            'a.offer-item__link-seller::attr(href)').extract()
        dealers = list(set(dealers))
        for dealer in dealers:
            if dealer not in DEALERS:
                DEALERS.append(dealer)

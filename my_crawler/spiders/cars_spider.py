import os.path
import json
import scrapy


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
        with open('dealers.txt', 'a') as dealers_file:
            for dealer in dealers:
                dealers_file.write('{}\n'.format(dealer))


class OffersSpider(scrapy.Spider):
    name = 'offers'

    def start_requests(self):
        urls = []
        dealers = open('dealers.txt', 'r').readlines()
        dealers = list(set(dealers))
        dealers_list = []
        for dealer in dealers:
            dealer = dealer.rstrip()
            dealers_list.append(dealer)
        for dealer in dealers_list:
            urls.append(dealer)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'offers-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        if os.path.isfile('offers.json'):
            offers = json.load(open('offers.json'))
        else:
            offers = json.load(open('offers_empty_pattern.json'))
        offer_urls = response.css(
            'a.offer-item__photo-link::attr(href)').extract()
        car_names = response.css('a.offer-title__link::attr(title)').extract()
        dealer_names = response.css('div.dealer-title::text').extract()
        dealer_names = [name.strip() for name in dealer_names]

        # TODO collected_datetimes
        # TODO sold_datetimes
        prices = response.css('span.offer-price__number::text').extract()
        prices = [price.strip() for price in prices]
        prices = list(filter(None, prices))
        offers_number = len(offer_urls)
        # Add dealer entry to dealers list
        offers['dealers'].append({
            'dealer_name': dealer_names[0],
            'offers': [],
        })
        # Add offers list to dealer entry
        for i in range(offers_number):
            offers['dealers'][-1]['offers'].append({
                'offer_url': offer_urls[i],
                'car_name': car_names[i],
                'price': prices[i],
            })
        # Save data to json file
        with open('offers.json', 'w') as offers_file:
            json.dump(offers, offers_file)

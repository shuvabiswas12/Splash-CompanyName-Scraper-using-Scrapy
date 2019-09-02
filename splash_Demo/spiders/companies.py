# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

# assert(splash:runjs('document.querySelector("#id a").click()'))
script = '''
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    splash:set_viewport_full()
    return {
        html = splash:html()
    }
end
'''


class CompaniesSpider(scrapy.Spider):
    name = 'companies'
    allowed_domains = ['checkpointspot.asia']

    def start_requests(self):
        url = 'http://www.checkpointspot.asia/'
        yield SplashRequest(url=url, callback=self.parse,
                            endpoint='execute',
                            cache_args=['lua_source'],
                            args={'lua_source': script},
                            headers={'X-My-Header': 'value'},
                            )

    def parse(self, response):
        for events_row in response.xpath('//div[@id="cphContents_secUpcomingEvent_divNewEvent"]//div[@class="row"]'):
            names = events_row.xpath(
                '//div[@class="events-item"]//h5//strong//text()').extract()
            for name in names:
                yield {
                    'name': name
                }

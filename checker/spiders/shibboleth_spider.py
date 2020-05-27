import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ShibbolethSpider(scrapy.Spider):
	name = "shibboleth_spider"
	handle_httpstatus_list = [400,401,403,404,405,406,407,408,410,429,451,500,501,502,503,504,505]

	start_urls = ['https://www.clarin.eu/content/easy-access-protected-resources']

	def parse(self, response):
		
		page = response.url.split("/")[-1]
		for url in response.xpath('//td/a[not(starts-with(@href, "#"))]/@href'):
			link = url.get()
			#yield scrapy.Request(l, callback=self.checkStatus)
			# add some category via https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request.meta
			yield response.follow(link, self.checkStatus, method='HEAD', meta={'origin':page}, errback=self.errback_report)
   
        
	def checkStatus(self, response):
			
		# second chance with GET instead of HEAD for problem cases
		if (response.status != 200 and response.request.method == 'HEAD'):
			yield response.follow(response.url, self.checkStatus, method='GET', meta=response.meta)
		else:
			if 'redirect_urls' in response.meta:
				startUrl = response.meta['redirect_urls'][0]
			else:
				startUrl = response.url
			
			outcome = dict()
			outcome['status'] = response.status
			outcome['starturl'] = startUrl
			outcome['origin'] = response.meta['origin']
			yield outcome
    	
	def errback_report(self, failure):
		outcome = dict()
		outcome['starturl'] = failure.request.url
		outcome['origin'] = failure.request.meta['origin']

		if failure.check(DNSLookupError):
			outcome['status'] = 'DNS failure'						
			yield outcome
			
		elif failure.check(TimeoutError, TCPTimedOutError):
			outcome['status'] = 'TCP Timeout'
			yield outcome
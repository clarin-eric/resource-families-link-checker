import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class QuotesSpider(scrapy.Spider):
	name = "resfam"
	handle_httpstatus_list = [400,401,403,404,405,406,407,408,410,429,451,500,501,502,503,504,505]

	start_urls = ['https://www.clarin.eu/resource-families/cmc-corpora',
	'https://www.clarin.eu/resource-families/manually-annotated-corpora', 
	'https://www.clarin.eu/resource-families/historical-corpora', 
	'https://www.clarin.eu/resource-families/L2-corpora', 
	'https://www.clarin.eu/resource-families/newspaper-corpora', 
	'https://www.clarin.eu/resource-families/parallel-corpora', 
	'https://www.clarin.eu/resource-families/parliamentary-corpora', 
	'https://www.clarin.eu/resource-families/spoken-corpora']
	
	new_urls = ['https://www.clarin.eu/resource-families/corpora-academic-texts',
	'https://www.clarin.eu/resource-families/literary-corpora',
	'https://www.clarin.eu/resource-families/lexical-resources-lexica',
	'https://www.clarin.eu/resource-families/lexical-resources-dictionaries',
	'https://www.clarin.eu/resource-families/lexical-resources-conceptual-resources',
	'https://www.clarin.eu/resource-families/lexical-resources-glossaries',
	'https://www.clarin.eu/resource-families/lexical-resources-wordlists',
	'https://www.clarin.eu/resource-families/tools-normalization',
	'https://www.clarin.eu/resource-families/tools-named-entity-recognition',
	'https://www.clarin.eu/resource-families/tools-part-speech-tagging-and-lemmatization'
	]
	
	start_urls += new_urls

	#start_urls = ['https://dev-www.clarin.eu/content/testlinks']

	def parse(self, response):
		GET_list = ['https://kontext.korpus.cz/', 'https://lindat.mff.cuni.cz/services/kontext/']	
		page = response.url.split("/")[-1]
		# extract relevant URLs from webpage
		for url in response.xpath('//div[@class="region region-content"]//a[not(starts-with(@href, "#") or starts-with(@href, "mailto"))]/@href'):
			link = url.get()
			http_method = 'HEAD'
			for GET_link in GET_list:
				if link.startswith(GET_link):
					http_method = 'GET'
			# yield scrapy.Request(l, callback=self.checkStatus)
			# now add the URL to the checking queue, and remember from which page it orginated
			yield response.follow(link, self.checkStatus, method=http_method, meta={'origin':page}, errback=self.errback_report)
   
        
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

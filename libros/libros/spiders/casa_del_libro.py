import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from libros.items import LibrosItem

class CasaDelLibroSpider(CrawlSpider):
    name = 'casa_del_libro'
    allowed_domains = ['www.casadellibro.com']
    start_urls = ["https://www.casadellibro.com/libros/ciencias-politicas-y-sociales/politica/p%d"
                  % i for i in range(1, 150)]

    item_count = 0

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//*[contains(@class, 'col col-10')]/a")),
             callback='parse', follow=False)
    }

    def parse(self, response):
        libro = LibrosItem()
        libro['title'] = response.xpath('normalize-space(//h1/text())').get()
        libro['author'] = response.xpath('//*[contains(@class, "author")]/div/a/span/text()').get()
        libro['image'] = response.xpath('//*[contains(@class, "product-image")]/@src').get()
        
        #trim tags
        tags = response.xpath('//*[contains(@class, "my-2")]/a/span/text()').getall()
        new_tags = []
        for i in tags:
           new_tags.append(i.strip())
           
        libro['tags'] = new_tags
        libro['sinopsis'] = response.xpath('//*[contains(@class, "text-container")]/div/p/text()').get()
        
        #los precios están dentro de un script y los extraemos mediante regex
        script_text = response.xpath('//*[contains(text(),"seoPrice")]').get()
        
        seoPrice = re.findall('seoPrice:"[0-9]+.[0-9]+', script_text)
        price = re.findall('[0-9]+.[0-9]+', seoPrice[0])
        
        seoCurrentPrice = re.findall('seoCurrentPrice:"[0-9]+.[0-9]+', script_text)
        real_price = re.findall('[0-9]+.[0-9]+', seoCurrentPrice[0])
        
        libro['price'] = price
        
        libro['real_price'] = real_price
        
        #los atributos no siempre son los mismos y solo podemos acceder a ellos mediante indice
        #solución: crear un diccionario con los atributos y despues asignaremos por clave si existen a los item
        att = response.xpath('//*[contains(@class,"hidden-sm-and-down")]/div/div/span/strong/text()').getall()
        val = response.xpath('//*[contains(@class,"hidden-sm-and-down")]/div/div/span/text()').getall()

        diccio = {}
        for i in range(0,len(att)):
            diccio[att[i]] = val[i]

        if 'Nº de páginas:' in att:
             libro['n_pages'] = diccio['Nº de páginas:']
        if 'Editorial:' in att:
             libro['editorial'] = diccio['Editorial:']
        if 'Idioma:' in att:
            libro['lang'] = diccio['Idioma:']
        if 'Encuadernación:' in att:
            libro['encuadernacion'] = diccio['Encuadernación:']
        if 'ISBN:' in att:
            libro['ISBN'] = diccio['ISBN:']
        if 'Año de edición:' in att:
            libro['year'] = diccio['Año de edición:']
        if 'Fecha de lanzamiento:' in att:
            libro['date'] = diccio['Fecha de lanzamiento:']

        #self.item_count += 1
        #if self.item_count > 31:
        #    raise CloseSpider('item_exceeded')
        yield libro


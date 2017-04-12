from django.shortcuts import render
from cms_barrapunto.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request

# Create your views here.


class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = ""
        self.link = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        global response

        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = "Title: " + self.theContent + "."
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                response += "<a href=" + self.theContent + ">" + \
                            self.title + "</a><br>"
                self.inContent = False
                self.theContent = ""
                self.title = ""
                self.link = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def show(request):
    global response

    content = Pages.objects.all()
    response = "Contenido de la base de datos:<br>"
    for entry in content:
        response = response + entry.name + " => " + entry.page + "<br>"

    barrapunto()
    return HttpResponse(response)


@csrf_exempt
def entry(request, identifier):
    global response

    if request.method == "POST":
        content = Pages(name=request.POST['nombre'],
                        page=request.POST['pagina'])
        content.save()
    elif request.method == "PUT":
        # Form of data in the body: name='<nombre>'&page='<pagina>'
        body = request.body.decode('utf-8')
        [parsed_name, parsed_page] = body.split("&")
        content = Pages(id=identifier, name=parsed_name, page=parsed_page)
        content.save()
    try:
        entry = Pages.objects.get(id=identifier)
        response = "La pagina solicitada es:" + "<br>" + entry.name + \
                   " => " + entry.page + "<br>"
    except Pages.DoesNotExist:
        response = "No existe en la base de datos. Creala:<br><br>"
        response += "<form action='' method = 'POST'>" + \
                    "Nombre:<br> <input type='text' name='nombre'><br>" + \
                    "Pagina:<br> <input type='text' name='pagina'><br><br>" + \
                    "<input type='submit' value='Enviar'><br>"

    barrapunto()
    return HttpResponse(response)


def error(request):
    global response

    response = "La pagina solicitada no se encuentra disponible <br>"

    barrapunto()
    return HttpResponse(response)


def barrapunto():
    global response

    response += "<br>"
    response += "Titulares de Barrapunto:<br>"

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(xmlFile)

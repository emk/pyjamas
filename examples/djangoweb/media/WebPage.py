import pyjd

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HTML import HTML

from pyjamas.JSONService import JSONProxy

from pyjamas import Window
from pyjamas import History
from pyjamas import log
from pyjamas import DOM
from pyjamas import Factory
from __pyjamas__ import doc


from WebPageEdit import WebPageEdit
from HTMLLinkPanel import HTMLLinkPanel

import Email # don't do anything with it - just import it and use factory

class WebApp:
    def onModuleLoad(self):

        self.remote = DataService()

        #Show the initial screen.
        initToken = History.getToken()
        if initToken and len(initToken):
            if initToken == 'admin':
                RootPanel().add(WebPageEdit(self))
                return
        else:
            initToken = 'index'

        self.dock = DockPanel()
        self.dock.setWidth("100%")
        self.pages = {}
        self.current_page = None
        RootPanel().add(self.dock)

        History.addHistoryListener(self)
        self.onHistoryChanged(initToken)

    def createPage(self, ref, html, title):
        htp = HTMLLinkPanel(self, html, title)
        htp.replaceLinks()
        htp.setWidth("100%")
        self.pages[ref] = htp

    def onHistoryChanged(self, token):
        #log.writebr("onHistoryChanged %s" % token)
        if self.pages.has_key(token):
            self.setPage(token)
            return
        self.remote.getPageByName(token, self)

    def setPage(self, ref):
        
        htp = self.pages[ref]
        if htp == self.current_page:
            return
        Window.setTitle(htp.title)
        if self.current_page:
            self.dock.remove(self.current_page)
        self.dock.add(htp, DockPanel.CENTER)
        self.current_page = htp

    def onRemoteResponse(self, response, request_info):
        if (request_info.method == 'getPageByName' or
           request_info.method == 'getPage'):
            item = response[0]
            html = item['fields']['text']
            token = item['fields']['name']
            self.createPage(token, html, token)
            self.setPage(token)

    def onRemoteError(self, code, message, request_info):
        RootPanel().add(HTML("Server Error or Invalid Response: ERROR " + str(code) + " - " + str(message)))


class DataService(JSONProxy):
    def __init__(self):
        JSONProxy.__init__(self, "/services/pages/",
                 ["getPage", "updatePage",
                  "getPages", "addPage",
                  "getPageByName",
                  "deletePage"])

if __name__ == "__main__":
    pyjd.setup("http://127.0.0.8/site_media/public/index.html")

    el = DOM.createElement("div")
    el.innerHTML = "test"
    DOM.setAttribute(el, "id", "pyjamas.apps.Email(Text='hello')")
    label = Factory.createWidgetOnElement(el)
    RootPanel().add(label)

    app = WebApp()
    app.onModuleLoad()
    pyjd.run()


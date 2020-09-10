from burp import IBurpExtender, IContextMenuFactory
from exceptions_fix import FixBurpExceptions
from java.util import ArrayList
from javax.swing import JMenuItem
from java.awt.datatransfer import StringSelection
from java.awt.datatransfer import Clipboard
from java.awt import Toolkit
import requests
import sys
import jarray
import java
from javax.script import ScriptEngine, ScriptException
from jdk.nashorn.api.scripting import NashornScriptEngineFactory


engine = NashornScriptEngineFactory().getScriptEngine(jarray.array(["--optimistic-types=false", "--language=es6"], java.lang.String))
script = open("code.min.js", 'rb').read()
compiled = engine.compile(script)
bindings = engine.createBindings()

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        sys.stdout = callbacks.getStdout()
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Copy as python requests")
        callbacks.registerContextMenuFactory(self)
        return
    
    def createMenuItems(self, invocation):
        self.context = invocation
        menuList = ArrayList()
        blackList=['CONTEXT_SCANNER_RESULTS', 'CONTEXT_SEARCH_RESULTS', 'CONTEXT_TARGET_SITE_MAP_TABLE', 'CONTEXT_TARGET_SITE_MAP_TREE']
        for i in blackList:
            if getattr(self.context, i) == self.context.getInvocationContext():
                return menuList

        menuItem = JMenuItem("Copy as Python Request", actionPerformed=self.copyAsPyRequest)
        menuList.add(menuItem)
        return menuList

    def copyAsPyRequest(self, event):
        plainReq = str(bytearray(self.context.getSelectedMessages()[0].getRequest()))

        headers = {
            'authority': 'curl.haxx.se',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'origin': 'https://curl.haxx.se',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://curl.haxx.se/h2c/',
            'accept-language': 'en-US,en;q=0.9,id;q=0.8,fr;q=0.7',
        }

        data = {
        'http': plainReq
        }

        # trust burp CA
        response = requests.post('https://curl.haxx.se/h2c/', headers=headers, data=data, verify=False).content
        start = response.find('curl --header')
        offset = response[start:].find('\n')        

        bindings.put("inputCurl", response[start:start+offset])
        compiled.eval(bindings)
        result = bindings.get("ret")

        toolkit = Toolkit.getDefaultToolkit()
        clipboard = toolkit.getSystemClipboard()
        clipboard.setContents(StringSelection(result), None)

try:
    FixBurpExceptions()
except:
    pass



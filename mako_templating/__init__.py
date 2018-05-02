# Source: https://bitbucket.org/Lawouach/cherrypy-recipes/src/1a27059966e962be52b2abd91e9709c3ee63cf2d/web/templating/mako_templating/__init__.py

# -*- coding: utf-8 -*-
import os.path
import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        return {'msg': 'Hello world I am MAKO TEMPLATE!', 'search_term' : 'HAS BEEN SEARCHED'}
        
if __name__ == '__main__':
    # Register the Mako plugin
    from makoplugin import MakoTemplatePlugin
    MakoTemplatePlugin(cherrypy.engine, base_dir=os.getcwd()).subscribe()

    # Register the Mako tool
    from makotool import MakoTool
    cherrypy.tools.template = MakoTool()

    # We must disable the encode tool because it
    # transforms our dictionary into a list which
    # won't be consumed by the mako tool
    cherrypy.quickstart(Root(), '', {'/': {'tools.template.on': True,
                                           'tools.template.template': 'index2.html',
                                           'tools.encode.on': False}})

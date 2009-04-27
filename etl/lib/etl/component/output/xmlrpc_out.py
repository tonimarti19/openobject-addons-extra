# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""
To do: comment
"""

from etl.component import component

class xmlrpc_out(component):
    """
    # To do: comment
    """
    def __init__(self, xmlrpc_connector, name='component.output.xmlrpc_out', transformer=None, row_limit=0):
        super(xmlrpc_out, self).__init__(name=name,connector=xmlrpc_connector, transformer=transformer, row_limit=row_limit)
        self._type='component.output.xmlrpc_out'

    def __copy__(self):        
        res=xmlrpc_out(self.connector, self.name, self.transformer, self.row_limit)
        return res  

    def end(self):
        super(xmlrpc_out, self).end()
        if self.server:
            self.connector.close(self.server)   
            self.server=False           

    def process(self):
        self.server=False
        for channel,trans in self.input_get().items():
            for iterator in trans:
                for d in iterator:
                    if not self.server:
                        self.server = self.connector.connect()
                    self.server.import_data([d])
                    yield d, 'main'

def test():
    pass

if __name__ == '__main__':
    pass

#s = xmlrpclib.ServerProxy('http://localhost:5000')
#s.import_data([
#    {'org':'X.Ltd','fn':'Mr.X','email':'x@xmail.com'},
#    {'org':'Y.Ltd','fn':'Mr.Y','email':'y@ymail.com'},
#    {'org':'X.Ltd','fn':'Mr.XX','email':'xx@xmail.com'},
#    {'org':'X.Ltd','fn':'Mr.X2','email':'x2@xmail.com'},
#    {'org':'Y.Ltd','fn':'Mr.Y1','email':'y1@ymail.com'},
#    ])
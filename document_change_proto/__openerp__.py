# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################


{
    'name': 'Integrated Document Management System',
    'version': '1.99',
    'category': 'Generic Modules/Others',
    'description': """
The document_change module allows to track and manage process changes to
update documents in directories, and keep track of these updates. You
can define control points, phase of changes. This module has been
developed for Caterpillar Belgium.
""",
    'author': 'Tiny',
    'website': 'http://www.openerp.com',
    'depends': ['base', 'document_ftp','board'],
    'init_xml': [
        'data/document_change_data.xml'
    ],
    'update_xml': [
        #'security/document_process_security.xml',
        'view/document_change.xml',
        'view/document_change_config.xml',
        'data/document_change_sequence.xml',
        'data/document_process_workflow.xml',
        'data/directory_types.xml'
        #'document_change_report_view.xml',
        #'document_phase_workflow.xml',
        #'document_process_workflow.xml',
        #'cat_demo.xml'
    ],
    'demo_xml': [ ],
    'installable': True,
    'active': False,
    'certificate': None,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

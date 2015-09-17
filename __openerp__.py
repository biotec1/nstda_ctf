# -*- coding: utf-8 -*-
{
        "name" : " MSTQ ",
        "version" : "0.1",
        "author" : 'ADMIN NSTDA',
        "category" : '',
        "description": """ ฐานข้อมูลห้องปฏิบัติการทดสอบ """,
        'website': 'https://i.nstda.or.th',
        'depends': [
                    'mail',
                    ],
        'data': [
                'security/module_data.xml',
                'security/nstda_ctf_security.xml',
                'security/ir.model.access.csv',
        #        'view/nstda_ctf.xml',
                'view/nstda_ctf_view.xml',
                'view/nstda_ctf_menu_view.xml',
                
                'view/mstq_analytic.xml',
        ],
        'demo': [],
        'installable': True,
        'images': [],
}

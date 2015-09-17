# -*- coding: utf-8 -*-
import csv
import mysql.connector
import psycopg2
from openerp import models, fields, api, exceptions, _
from openerp import pooler

class nstda_ctf_syc_sql(models.Model): 
    _name = 'nstda.ctf.syc.sql'
    
    @api.one
    def syc_sql(self):
        con_sql = mysql.connector.connect(user='root',
                                          password = '1234',
                                          host = 'localhost',
                                          database = 'certificate',
                                          )
        cr_sql = con_sql.cursor()
        
        cr_sql.execute("""DELETE FROM `std` WHERE 1""")
        obj_std = self.env['nstda.ctf.list.test.unit'].search([])
        for i in obj_std:
            cr_sql.execute("""INSERT INTO `std`(`id`,`Regulator`,`StandardCode`,`Equipment`,`Standard`,`TypeStd`,`List`,`TestUnit`,`Grade` ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",(i.id,i.list_ids.cer_ids.regulator_ids.regulator,i.list_ids.cer_ids.standardcode,i.list_ids.cer_ids.equipment,i.list_ids.standard,i.list_ids.cer_ids.typestd,i.list_ids.name,i.test_unit_ids.name,i.grade_ids.name)) 
            
        cr_sql.execute("""DELETE FROM ministry WHERE 1""")
        obj_regulator = self.env['nstda.ctf.regulator'].search([])
        for i in obj_regulator:
            cr_sql.execute("""INSERT INTO ministry(ministry_id,ministry_name,regulator,address,telephone,web_site ) VALUES(%s, %s, %s, %s, %s, %s)""",(i.id,i.ministry_ids.name,i.regulator,i.address,i.telephone,i.web_site))
           
        con_sql.commit()
        cr_sql.close()       




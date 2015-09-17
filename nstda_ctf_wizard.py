# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from openerp.tools.translate import _
from email import _name
from openerp import tools
import re
from openerp import SUPERUSER_ID
from docutils.parsers import null


class nstda_ctf_list_wizard(models.TransientModel):
    def _default_cer_ids(self):
        return self.env['nstda.ctf.testunit.ability'].browse(self._context.get('active_id')).cer_id

    @api.one
    def create_list(self):
        list = self.env['nstda.ctf.list']
        list += list.create({'name':self.name, 'standard':self.standard, 
                             'cer_ids':[(4,self.cer_ids.id)] })
        
        ability = self.env['nstda.ctf.testunit.ability'].browse(self._context.get('active_id'))
        ability.ability_line_ids += ability.ability_line_ids.new(
            {'ability_id':self._context.get('active_id'), 'list_id':list.id})
#        list.cer_ids.create({'nstda_ctf_line_id':list.id,'nstda_ctf_cer_id':self.cer_ids[0]})
        return {'type': 'ir.actions.act_window_close'}

    _name = 'nstda.ctf.list.wizard'
    cer_ids = fields.Many2many('nstda.ctf.cer', default=_default_cer_ids)
    name = fields.Char('รายการทดสอบ', size=255, required=True)
    standard = fields.Char('เกณฑ์', size=3000)


class nstda_ctf_cer_wizard(models.TransientModel):
    @api.one
    def create_list(self):
        cer = self.env['nstda.ctf.cer']
        cer += cer.create({'regulator_ids':self.regulator_ids, 'standardcode':self.standardcode,
            'name':self.name, 'equipment':self.equipment, 'certype_id':self.certype_id,
            'inter_flag':self.inter_flag, 'state':'draft'})
        
        testunit = self.env['nstda.ctf.test.unit'].browse(self._context.get('active_id'))
        testunit.testunit_ability_ids += testunit.testunit_ability_ids.new({'test_unit_id':self._context.get('active_id'), 'cer_id':cer.id})
        return {'type': 'ir.actions.act_window_close'}

    _name = 'nstda.ctf.cer.wizard'
    regulator_ids = fields.Many2one('nstda.ctf.regulator', 'Regulator')          
    standardcode = fields.Char('รหัสมาตรฐาน', size=500)
    name = fields.Char('ชื่อมาตรฐาน', size=500)
    equipment = fields.Char('ผลิตภัณฑ์', size=500)
    certype_id = fields.Many2one('nstda.ctf.certype', 'ประเภท')
    inter_flag = fields.Boolean('มาตรฐานต่างประเทศ', default=False)
    state = fields.Selection([('draft', 'เพิ่มเติม'), ('confirm', ' ')], 'ชนิด', required=True, 
        default='draft')

 
# class nstda_ctf_list_test_unit_wizard(models.Model):  
#     
#     @api.one
#     def save(self):
#         obj = self.env['nstda.ctf.list.test.unit'].browse(self._context['active_ids'][0]).write({
#                                                                                           'doc_file': self.doc_file,
#                                                                                           'doc_file_filename': self.doc_file_filename,
#                                                                                          })
# 
#         return obj
# 
#     
#     @api.model
#     def set_default_doc_file(self):
#         obj = self.env['nstda.ctf.list.test.unit'].browse(self._context['active_ids'][0])
#         return obj.doc_file
#     
#     @api.model
#     def set_default_doc_file_filename(self):
#         obj = self.env['nstda.ctf.list.test.unit'].browse(self._context['active_ids'][0])
#         return obj.doc_file_filename
#     
# 
#         
#         
#     _name = 'nstda.ctf.list.test.unit.wizard'
# 
#     doc_file = fields.Binary('Document', default=set_default_doc_file)
#     doc_file_filename = fields.Char('Filename', default=set_default_doc_file_filename)
    
# class nstda_ctf_list_wizard(models.Model):  
#     
#     @api.one
#     def save(self):
#         other_std = self.env['nstda.ctf.cer'].search([('standardcode','=' ,'รายการทดสอบอื่นๆ')])
#         obj = self.env['nstda.ctf.list'].create({'cer_ids': [(4, other_std.id)],
#                                                  'name': self.name,
#                                                  'standard': self.standard,
#                                                 })
#      
#         obj2 = self.env['nstda.ctf.list.test.unit'].create({
#                                                             
#                                                             'list_ids': obj.id,
#                                                             'grade_ids': self.grade_ids.id,
#                                                             'flag': 1,
#                                                             
#                                                             })
#         write_3 = self.env['nstda.ctf.list.test.unit'].browse(obj2.id).write({'test_unit_ids': self._context.get('unit_id')})
#         return True
#                                                            
#       
# 
#         
#     _name = 'nstda.ctf.list.wizard'
#     
#     name = fields.Char('รายการทดสอบ', size=255, track_visibility='onchange')
#     standard = fields.Char('เกณฑ์', size=3000, track_visibility='onchange')
#     grade_ids = fields.Many2one('nstda.ctf.grade', track_visibility='onchange')  


   
    
  
            

    
    
    
    

 




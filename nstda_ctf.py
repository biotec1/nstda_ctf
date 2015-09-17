# -*- coding: utf-8 -*-
##############################################################################
from openerp import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from openerp.tools.translate import _
from email import _name
#from bsddb.dbtables import _columns
from openerp import tools
import re
from openerp import SUPERUSER_ID
from docutils.parsers import null
from openerp.exceptions import except_orm, Warning, RedirectWarning

        
class nstda_ctf_ministry(models.Model):
    _name = 'nstda.ctf.ministry'
    _description = 'NSTDA MSTQ ministry'
    _rec_name = 'name'
    name = fields.Char('ชื่อกระทรวง', size=1000)


class nstda_ctf_regulator(models.Model):
    _name = 'nstda.ctf.regulator'
    _description = 'NSTDA MSTQ Regulator'
    _rec_name = 'regulator'
    _inherit = ['mail.thread']
    regulator = fields.Char('ชื่อหน่วยงาน', size=255, track_visibility='onchange')
    ministry_ids = fields.Many2one('nstda.ctf.ministry', track_visibility='onchange')
    address = fields.Char('ที่อยู่', size =1000, track_visibility='onchange')
    telephone = fields.Char('โทรศัพท์',size = 60, track_visibility='onchange')
    fax = fields.Char('โทรสาร',size = 30, track_visibility='onchange')
    e_mail=fields.Char('Email',size = 120, track_visibility='onchange')
    web_site = fields.Char('Web site',size = 1000, track_visibility='onchange')
    service_individual = fields.Selection([('Y', 'เปิดให้บริการภาคเอกชน'),('N', 'ไม่เปิดให้บริการภาคเอกชน'), ],
        track_visibility='onchange',default='Y',  )
    products_test = fields.Char('ผลิตภัณฑ์ที่รับทดสอบเป็นประจำ', size =1000, track_visibility='onchange')
    service_test_per_month = fields.Integer('สามารถรองรับได้  ครั้ง/เดือน', track_visibility='onchange')
    cer_ids = fields.One2many('nstda.ctf.cer', 'regulator_ids', 'Cer', track_visibility='onchange')
    res_user = fields.Many2many('res.users')

    contact_name = fields.Char('ชื่อผู้ติดต่อ', size=200, track_visibility='onchange')
    contact_email = fields.Char('Email ผู้ติดต่อ', size=200, track_visibility='onchange')
    contact_tel = fields.Char('เบอร์ ผู้ติดต่อ', size=100, track_visibility='onchange')
    contact_ids = fields.One2many('nstda.ctf.contact', 'regulator_id',track_visibility='onchange')



class nstda_ctf_grade(models.Model):    
    _name = 'nstda.ctf.grade'
    _description = 'NSTDA MSTQ Grade'
    _rec_name = 'name'
    name = fields.Char('หน่วยงานทดสอบ', size=255)

class nstda_ctf_certype(models.Model):    
    _name = 'nstda.ctf.certype'
    _description = 'NSTDA MSTQ Certificat Type'
    name = fields.Char('ประเภท', size=40)

class nstda_ctf_list(models.Model):
    _name = 'nstda.ctf.list'
    _description = 'NSTDA MSTQ Certificat List'

    _inherit = ['mail.thread']
    cer_ids = fields.Many2many('nstda.ctf.cer', track_visibility='onchange')
    cerlist_ids = fields.One2many('nstda.ctf.cerlist', 'list_id', 'Certificate')
   
    name = fields.Char('รายการทดสอบ', size=255, track_visibility='onchange')
    standard = fields.Char('เกณฑ์', size=3000, track_visibility='onchange')


class nstda_ctf_contact(models.Model):
    _name = 'nstda.ctf.contact'
    _description = 'NSTDA MSTQ Contact'

    _inherit = ['mail.thread']
    name = fields.Char('ชื่อ', size=200, track_visibility='onchange')
    email = fields.Char('Email', size=200, track_visibility='onchange')
    tel = fields.Char('โทรศัพท์', size=100, track_visibility='onchange')
    test_unit_id = fields.Many2one('nstda.ctf.test.unit', track_visibility='onchange', ondelete='cascade')
    regulator_id = fields.Many2one('nstda.ctf.regulator', track_visibility='onchange', ondelete='cascade')


class nstda_ctf_cerlist(models.Model):
    _name = 'nstda.ctf.cerlist'
    _description = 'NSTDA MSTQ Certificate list'

    _inherit = ['mail.thread']
    name = fields.Char('เกณฑ์', size=3000, track_visibility='onchange')
    cer_id = fields.Many2one('nstda.ctf.cer', track_visibility='onchange', ondelete='cascade')
    list_id = fields.Many2one('nstda.ctf.list', track_visibility='onchange', ondelete='cascade')
    
    _order = 'list_id'


class nstda_ctf_cer(models.Model):
    
    @api.constrains('name','standardcode','inter_flag')
    def _check_constranis(self):
        if self.inter_flag == False:
            raise ValueError(_("ยังไม่เปิดบันทึกข้อมูลมาตรฐานของไทย สามารถบันทึกได้เฉพาะมาตรฐานต่างประเทศ"))
    
    _name = 'nstda.ctf.cer'
    _description = 'NSTDA MSTQ Certificat'
#    _rec_name = 'standardcode'
    _inherit = ['mail.thread']
    regulator_ids = fields.Many2one('nstda.ctf.regulator', 'Regulator', track_visibility='onchange')          
    standardcode = fields.Char('รหัสมาตรฐาน', size=500, track_visibility='onchange')
    name = fields.Char('ชื่อมาตรฐาน', size=500, track_visibility='onchange')
    equipment = fields.Char('ผลิตภัณฑ์', size=500, track_visibility='onchange')
    certype_id = fields.Many2one('nstda.ctf.certype', 'ประเภท', track_visibility='onchange')
    list_ids = fields.Many2many('nstda.ctf.list', track_visibility='onchange')
    cerlist_ids = fields.One2many('nstda.ctf.cerlist', 'cer_id', 'รายการทดสอบ')

    inter_flag = fields.Boolean('มาตรฐานต่างประเทศ', track_visibility='onchange', default=False)
    
    state = fields.Selection([('draft', 'เพิ่มเติม'), ('confirm', ' ')], 'ชนิด', required=True, 
        default='draft')
    
    ability_ids = fields.One2many('nstda.ctf.testunit.ability', 'cer_id', 'หน่วยทดสอบ')
    
    _order = 'standardcode'
    
#     @api.onchange('inter_flag')
#     def _onchange_inter_flag(self):
#         if self.inter_flag == False:
#             warning = {'title':_('เตือน ยังไม่เปิดการบันทึก!'),'message': _('เปิดให้บันทึกมาตรฐานต่างประเทศเท่านั้น')}
#             return {'value':{},'warning':warning}


class nstda_ctf_ability_cerfile(models.Model):
    _name = 'nstda.ctf.ability.cerfile'
    _description = 'NSTDA MSTQ Ability Certificate upload files'
    #_rec_name = ''
    _inherit = ['mail.thread']
    ability_id = fields.Many2one('nstda.ctf.testunit.ability', track_visibility='onchange', ondelete='cascade')
    file = fields.Binary('Document')
    file_filename = fields.Char('Filename', track_visibility='onchange')


class nstda_ctf_testunit_ability(models.Model):
    @api.one
    @api.depends('ability_line_ids')
    def _cantest_compute(self):
        can = 0
        can17025 = 0
        str01 = 'ทดสอบได้ (ISO/IEC 17025)'
        str02 = 'ทดสอบได้ '
        for line in self.ability_line_ids:
            if line.grade_ids.name != False:
                if line.grade_ids.id == 2:
                    can17025 += 1
                else:
                    if line.grade_ids.id == 1:
                        can += 1
        self.cantest = can
        self.can17025 = can17025

    @api.one
    def _certificat_save_flag(self):
        if len(self.cerfile_ids._ids) > 0:
            self.certificat_save_flag = '1'
        else:
            c = 0
            for line in self.ability_line_ids:
                if line.grade_ids.name != False:
                    str01 = 'ทดสอบได้ (ISO/IEC 17025)'
                    if line.grade_ids.name.encode('utf-8','ignore') == str01: 
                        c += 1
            if c > 0:
                self.certificat_save_flag = ''
            else:
                self.certificat_save_flag = '1'

    @api.onchange('cer_id')
    def _cer_id(self):
        # Create default ability_line from selected Certificat
        if self.cer_id.id != False:
            #if self.inter_flag == False:
            #    raise ValueError(_("ยังไม่เปิดบันทึกข้อมูลมาตรฐานของไทย สามารถบันทึกได้เฉพาะมาตรฐานต่างประเทศ"))
            if self.ability_line_ids._ids == ():
                for list in self.cer_id.list_ids:
                    self.ability_line_ids += self.ability_line_ids.new({'ability_id':self.id,'list_id':list.id})

    @api.onchange('ability_line_ids','cerfile_ids')
    def _onchange_ability_line_ids(self):
        # Check ISO 17025
        c = 0
        for line in self.ability_line_ids:
            if line.grade_ids.name != False:
                str01 = 'ทดสอบได้ (ISO/IEC 17025)'
                if line.grade_ids.name.encode('utf-8','ignore') == str01: 
                    c += 1
        if c > 0:
            if len(self.cerfile_ids._ids) > 0:
                self.certificat_save_flag = '1'
            else:
                self.certificat_save_flag = ''
        else:
            self.certificat_save_flag = '1'
#             msg = _('เตือน!!! ทดสอบได้ (ISO/IEC 17025) ต้องดำเนิน Upload Certificate ด้วย')
#             warning = {'title':_('เตือน !!!'),'message': msg}
#             return {'value':{},'warning':warning}
#             raise Warning(_('You cannot delete a.'))

    _name = 'nstda.ctf.testunit.ability'
    _description = 'NSTDA MSTQ Test Unit Ability'
    #_rec_name = ''
    _inherit = ['mail.thread']

    test_unit_id = fields.Many2one('nstda.ctf.test.unit', track_visibility='onchange', ondelete='cascade')
    cer_id = fields.Many2one('nstda.ctf.cer', track_visibility='onchange', ondelete='cascade')
    cer_state = fields.Selection(related='cer_id.state', readonly=True)
    equipment = fields.Char(string='อุปกรณ์', related='cer_id.equipment', readonly=True)
    inter_flag = fields.Boolean('มาตรฐานต่างประเทศ', related='cer_id.inter_flag')

    products_test = fields.Char('ผลิตภัณฑ์ที่รับทดสอบเป็นประจำ', size =1000,track_visibility='onchange')
    test_capacity_per_m = fields.Integer('สามารถรองรับได้  (ครั้ง/เดือน)', track_visibility='onchange')
    test_service_per_m = fields.Integer('เฉลี่ยบริการ (ครั้ง/เดือน)', track_visibility='onchange')
    confirm = fields.Boolean(string='ยืนยัน')
    doc_file = fields.Binary('Document')
    doc_file_filename = fields.Char('Filename')
    cerfile_ids = fields.One2many('nstda.ctf.ability.cerfile', 'ability_id', 'Certificate')

    ability_line_ids = fields.One2many('nstda.ctf.testunit.ability.line', 'ability_id', 'รายการทดสอบ')
    certificat_save_flag = fields.Char(compute=_certificat_save_flag, size=1)
    
    cantest = fields.Integer(compute='_cantest_compute', store=True)
    can17025 = fields.Integer(compute='_cantest_compute', store=True)



class nstda_ctf_testunit_ability_line(models.Model):
#     @api.one
#     @api.onchange('grade_ids')
#     def _grade_ids_onchange(self):
#         c = 0
#         if self.grade_ids.name != False:
#             str01 = 'ทดสอบได้ (ISO/IEC 17025)'
#             if self.grade_ids.name.encode('utf-8','ignore') == str01: 
#                 c += 1
    _name = 'nstda.ctf.testunit.ability.line'
    _description = 'NSTDA MSTQ Test Unit Ability Line'
    #_rec_name = ''
    _inherit = ['mail.thread']
    ability_id = fields.Many2one('nstda.ctf.testunit.ability', track_visibility='onchange', ondelete='cascade')
    list_id = fields.Many2one('nstda.ctf.list', track_visibility='onchange', ondelete='cascade') 
    standard = fields.Char(string='เกณฑ์', related='list_id.standard')

#     cerlist_id = fields.Many2one('nstda.ctf.cerlist', track_visibility='onchange', ondelete='cascade') 
#     list_id1 = fields.Many2one(string='รายการ', related='cerlist_id.list_id') 
#     standard1 = fields.Char(string='เกณฑ์', related='cerlist_id.name')

    grade_ids = fields.Many2one('nstda.ctf.grade', 'ความสามารถ', track_visibility='onchange')

    comment = fields.Char(string='ข้อสังเกต', size = 2000)
    comment_clear_flag = fields.Boolean(string='จัดการแล้ว')

    cer_state = fields.Selection(related='ability_id.cer_id.state', readonly=True)


class nstda_ctf_test_unit(models.Model):
    @api.one
    def create_other_list(self):
        cer_id = self.env['nstda.ctf.cer'].search([('standardcode','=','รายการอื่นๆ')])
        if cer_id.id == False:
            cer_id = self.env['nstda.ctf.cer'].create({'standardcode':'รายการอื่นๆ','equipment':'รายการอื่นๆ'})
        cer_ids1 = []
        for line in self.testunit_ability_ids:
            cer_ids1.append(line.cer_id.id)
        if (cer_id.id not in cer_ids1):
            self.testunit_ability_ids += self.testunit_ability_ids.browse(self._context.get('active_id')).browse(self._context.get('active_id')).new({'test_unit_id':self.id,'cer_id':cer_id.id})

    @api.one
    @api.depends('testunit_ability_ids')
    def _f_other_cer_invisible(self):
        cer_id = self.env['nstda.ctf.cer'].search([('standardcode','=','รายการอื่นๆ')])
        if cer_id.id == False:
            cer_id = self.env['nstda.ctf.cer'].create({'standardcode':'รายการอื่นๆ','equipment':'รายการอื่นๆ'})
        cer_ids1 = []
        for line in self.testunit_ability_ids:
            cer_ids1.append(line.cer_id.id)
        self.f_other_cer_invisible = True
        if (cer_id.id not in cer_ids1):
            self.f_other_cer_invisible = False

    @api.one
    def check_confirm1(self):
        c = 0
        for ability in self.testunit_ability_ids:
            if ability.confirm == False: c += 1
        return c

    @api.onchange('testunit_ability_ids')
    def _onchange_testunit_ability_ids(self):
        c = self.check_confirm1()
        if c[0] > 0:
            msg = _('เหลือมาตรฐาน ยังไม่ยืนยันอีก %d : มาตรฐานทั้งหมด %d') % (c[0],len(self.testunit_ability_ids._ids))
            warning = {'title':_('เตือน ยืนยันมาตรฐานไม่ครบ!'),'message': msg}
            return {'value':{},'warning':warning}
    
    @api.one
    @api.constrains('contact_ids','e_mail')
    def _check_contact_constrains(self):
        if len(self.contact_ids._ids) == 0:
            raise Warning(_("ต้องปันทึกผู้ติดต่อ"))
    
    @api.one
    @api.onchange('contact_ids')
    def _contact_ok_flag(self):
        if len(self.contact_ids._ids) > 0:
            self.contact_ok_flag = '1'
        else:
            self.contact_ok_flag = ''
    
    _name = 'nstda.ctf.test.unit'
    _description = 'NSTDA MSTQ Test Unit'
    _inherit = ['mail.thread']
#     list_test_unit_ids = fields.One2many('nstda.ctf.list.test.unit', 'test_unit_ids', 
#         track_visibility='onchange', )
# ??? add domain=[('list_ids.cer_ids','in',[107230])]
    name = fields.Char('หน่วยงานทดสอบ', size=255, track_visibility='onchange')  
    address = fields.Char('ที่อยู่', size =1000,track_visibility='onchange')  
    telephone = fields.Char('โทรศัพท์',size = 60,track_visibility='onchange')  
    fax = fields.Char('โทรสาร',size = 60,track_visibility='onchange')
    e_mail = fields.Char('Email',size = 120,track_visibility='onchange')
    website = fields.Char('Website',size = 120,track_visibility='onchange')
    service_individual = fields.Selection([('Y', 'เปิด'),('N', 'ไม่เปิด'), ],'ให้บริการภายนอก', 
        track_visibility='onchange',default='Y', )
    products_test = fields.Char('ผลิตภัณฑ์ที่รับทดสอบเป็นประจำ', size =1000,track_visibility='onchange') 
    service_test_per_month = fields.Integer('สามารถรองรับได้  ครั้ง/เดือน',track_visibility='onchange')     
    res_user = fields.Many2many('res.users')
    testunit_ability_ids = fields.One2many('nstda.ctf.testunit.ability', 'test_unit_id',track_visibility='onchange')

    contact_name = fields.Char('ชื่อผู้ติดต่อ', size=200, track_visibility='onchange')
    contact_email = fields.Char('Email ผู้ติดต่อ', size=200, track_visibility='onchange')
    contact_tel = fields.Char('เบอร์ ผู้ติดต่อ', size=100, track_visibility='onchange')
    contact_ids = fields.One2many('nstda.ctf.contact', 'test_unit_id',track_visibility='onchange')

    f_other_cer_invisible = fields.Boolean(compute='_f_other_cer_invisible', default='False')
    contact_ok_flag = fields.Char(compute=_contact_ok_flag, size=1)

    _order = 'name'
  
  
  
  
  
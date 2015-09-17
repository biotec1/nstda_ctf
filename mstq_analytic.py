from openerp import tools
from openerp.osv import fields,osv


class nstda_mstq_analytic1(osv.osv):
    _name = "mstq.certificat.report"
    _description = "Analytic Entries Statistics"
    _auto = False

    _columns = {
        'c':fields.integer('#', readonly=True),
        'regulator_id':fields.many2one('nstda.ctf.regulator', 'Regulator'),
        'certype_id':fields.many2one('nstda.ctf.certype', 'Type'),
        'ministry':fields.char('Ministry')
    }
#     _columns = {
#         'date': fields.date('Date', readonly=True),
#         'user_id': fields.many2one('res.users', 'User',readonly=True),
#         'name': fields.char('Description', size=64, readonly=True),
#         'partner_id': fields.many2one('res.partner', 'Partner'),
#         'company_id': fields.many2one('res.company', 'Company', required=True),
#         'currency_id': fields.many2one('res.currency', 'Currency', required=True),
#         'account_id': fields.many2one('account.analytic.account', 'Account', required=False),
#         'general_account_id': fields.many2one('account.account', 'General Account', required=True),
#         'journal_id': fields.many2one('account.analytic.journal', 'Journal', required=True),
#         'move_id': fields.many2one('account.move.line', 'Move', required=True),
#         'product_id': fields.many2one('product.product', 'Product', required=True),
#         'product_uom_id': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
#         'amount': fields.float('Amount', readonly=True),
#         'unit_amount': fields.integer('Unit Amount', readonly=True),
#         'nbr': fields.integer('# Entries', readonly=True),  # TDE FIXME master: rename into nbr_entries
#     }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'mstq_certificat_report')
        cr.execute("""
        create or replace view mstq_certificat_report as (
            select
            max(c.id) as id,
            count(*) as c,
            c.regulator_ids as regulator_id,
            c.certype_id,
            m.name as ministry
            from
            nstda_ctf_cer c 
            inner join nstda_ctf_cer_nstda_ctf_list_rel cl_rel on c.id = cl_rel.nstda_ctf_cer_id
            inner join nstda_ctf_list l on l.id = cl_rel.nstda_ctf_list_id
            inner join nstda_ctf_regulator r on r.id = c.regulator_ids
            inner join nstda_ctf_ministry m on m.id = r.ministry_ids
            group by
            c.regulator_ids,
            c.certype_id,
            m.name
        )
        """)



class nstda_mstq_analytic2(osv.osv):
    _name = "mstq.analytic.report"
    _description = "Analytic Entries Statistics2"
    _auto = False

    _columns = {
        'c':fields.integer('#', readonly=True),
        'standardcode':fields.char('Certificate'),
        'equipment':fields.char('Certificate1'),
        'list_name':fields.char('List'),
        'standard':fields.char('List1'),
        'testunit_name':fields.char('TestUnit'),
        'grade_name':fields.char('ability'),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'mstq_analytic_report')
        cr.execute("""
        create or replace view mstq_analytic_report as (
SELECT 
  count(*) as c,
  nstda_ctf_testunit_ability_line.id as id,
  nstda_ctf_cer.id AS cer_id, 
  nstda_ctf_cer.standardcode, 
  nstda_ctf_cer.equipment, 
  nstda_ctf_list.id AS list_id, 
  nstda_ctf_list.name AS list_name, 
  nstda_ctf_list.standard, 
  nstda_ctf_test_unit.id AS testunit_id, 
  nstda_ctf_test_unit.name AS testunit_name, 
  nstda_ctf_grade.name AS grade_name
FROM 
  public.nstda_ctf_cer, 
  public.nstda_ctf_list, 
  public.nstda_ctf_testunit_ability, 
  public.nstda_ctf_testunit_ability_line, 
  public.nstda_ctf_test_unit, 
  public.nstda_ctf_grade
WHERE 
  nstda_ctf_cer.id = nstda_ctf_testunit_ability.cer_id AND
  nstda_ctf_list.id = nstda_ctf_testunit_ability_line.list_id AND
  nstda_ctf_testunit_ability_line.ability_id = nstda_ctf_testunit_ability.id AND
  nstda_ctf_test_unit.id = nstda_ctf_testunit_ability.test_unit_id AND
  nstda_ctf_grade.id = nstda_ctf_testunit_ability_line.grade_ids
GROUP BY
  nstda_ctf_testunit_ability_line.id,
  nstda_ctf_cer.id, 
  nstda_ctf_cer.standardcode, 
  nstda_ctf_cer.equipment, 
  nstda_ctf_list.id, 
  nstda_ctf_list.name, 
  nstda_ctf_list.standard, 
  nstda_ctf_test_unit.id, 
  nstda_ctf_test_unit.name, 
  nstda_ctf_grade.name
        )
        """)



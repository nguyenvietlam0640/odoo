

from odoo import fields, api, models
from datetime import datetime
subjects = [('ma', 'Math'), ('eng', 'English'), ('lit', 'Literate')]
status_list = [('en', 'End'), ('ig', 'In progress'), ('so', 'Sold out'), ('cs', 'Comming soon')]


class create_multi_class(models.TransientModel):
    _name = 'sm.create_multi.class.wiz'
    name = fields.Char(string='Class name', required=True)
    teacher_id = fields.Many2one(string='Teacher', comodel_name='sm.teacher', ondelete='set null')
    subject = fields.Selection(subjects, string='Subject', required=True)

    start_date = fields.Date(string='Start date', default=datetime.today(), required=True)
    end_date = fields.Date(string='End date', default=datetime.today(), required=True)
    
    seat = fields.Integer(string='Seat', required=True, default=10)
    empty_seat = fields.Integer(string='Empty_seat', compute='_compute_empty_seat', store=True)
    
    status = fields.Selection(status_list, string='Status', compute='_compute_status', store=True)
    
    student_ids = fields.One2many(string='Students', comodel_name='sm.student', inverse_name='class_id')
    
    currency_id = fields.Many2one('res.currency', string='Current monetary', default=23)
    original_price = fields.Monetary(string='Original price', currency_field='currency_id')
    discount = fields.Integer(string='Discount(%)')
    fee = fields.Monetary(string='Registration fee' , currency_field='currency_id', compute='_compute_fee', store=True)
    
    
    def create_classes(self):
        print('created')
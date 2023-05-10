# -*- coding: utf-8 -*-

from odoo import models, fields, api, modules

from odoo.exceptions import ValidationError
from datetime import datetime
import base64

subjects = [('ma', 'Math'), ('eng', 'English'), ('lit', 'Literate')]
status_list = [('en', 'End'), ('ig', 'In progress'), ('so', 'Sold out'), ('cs', 'Comming soon')]


class BasicHuman(models.AbstractModel):
        _name = 'sm.human'
        name = fields.Char(string='Name')


class Human(models.AbstractModel):
    _name = 'sm.human'
    _inherit = 'sm.human'
    
    birthday = fields.Date(string="Birthday", required=True)
    photo = fields.Image(max_width=128, max_height=128)

    
class Student(models.Model):
    _name = 'sm.student'
    _inherit = 'sm.human'
    name = fields.Char(string='Student name', required=True, translate=True)
    
    class_id = fields.Many2one(string='In class', comodel_name='sm.class', ondelete='cascade', required=True)
    rel_empty_seat = fields.Integer(related='class_id.empty_seat', string='Empty seat in this class')
    email = fields.Char(string='Email')
    number = fields.Char(string='Number phone', translate=True)

    @api.constrains('class_id')
    def _check_seat(self):
        if self.rel_empty_seat <= -1:
            raise ValidationError('This class have no longer empty seat, please choose another class')

    @api.constrains('photo', 'name')
    def _check_image(self):
        print('hooo')
        if not self.photo:
            with open(modules.get_module_resource('student_management', 'static/src/img', 'default_img.png'), 'rb') as f:
                self.photo = base64.b64encode(f.read())
    
    @api.model
    def create(self, vals):
        vals['name'] = vals['name'].upper()
        return super(Student, self).create(vals)
# class StudentAdvance(models.Model):
#     # declare can see student information 
#     pass


class Teacher(models.Model):
    _name = 'sm.teacher'
    _inherit = 'sm.human'
    name = fields.Char(string='Teacher name', required=True)
    
    subject = fields.Selection(subjects, string='Subject', required=True)
    
    class_ids = fields.One2many(string='Current classes', comodel_name='sm.class', inverse_name='teacher_id')

    @api.model
    def create(self, vals):
        vals['name'] = vals['name'].upper()
        return super(Teacher, self).create(vals)


class Class(models.Model):
    _name = 'sm.class'
    _sql_constraints = [('check_name_unique', 'UNIQUE (name)', 'Class name must be unique, Given existed name.')]
    
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
    
    @api.constrains('start_date', 'end_date')
    def _check_valid_date(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be less than end date')
    
    @api.constrains('seat')
    def _check_valid_seat(self):
        if self.seat <= 0:
            raise ValidationError('Give available seat to this class')
    
    @api.depends('student_ids', 'seat')
    def _compute_empty_seat(self):
        print(self.student_ids)
        for r in self:
            r.empty_seat = r.seat - len(r.student_ids._origin)
    
    @api.depends('discount', 'original_price')
    def _compute_fee(self):
        for r in self:
            r.fee = r.original_price - r.original_price * (r.discount / 100)
    
    @api.depends('start_date', 'end_date', 'student_ids')
    def _compute_status(self):
        for r in self:
            if datetime.date(datetime.today()) < r.start_date:
                r.status = 'cs'
            elif datetime.date(datetime.today()) > r.end_date:
                r.status = 'en'
            elif r.empty_seat <= 0:
                r.status = 'so'
            else:
                r.status = 'ig'
    
    def open_update_discount_wizard(self):
        
        return {'type':'ir.actions.act_window',
                'res_model': 'sm.update.discount.wiz',
                'view_mode':'form',
                'target':'new'}
    
    def open_create_multi_class_wizard(self):
        return {'type':'ir.actions.act_window',
                'res_model': 'sm.create_multi.class.wiz',
                'view_mode':'form',
                'target':'new'}

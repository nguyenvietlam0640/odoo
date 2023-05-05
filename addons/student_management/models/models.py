# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError
from datetime import datetime

subjects = [('ma', 'Math'), ('eng', 'English'), ('lit', 'Literate')]


class Class(models.Model):
    _name = 'sm.class'
    _sql_constraints = [('check_name_unique', 'UNIQUE (name)', 'Class name must be unique, Given existed name.')]
    name = fields.Char(string='Class name', required=True)
    subject = fields.Selection(subjects, string='Subject', required=True)
    start_date = fields.Date(string='Start date', default=datetime.today(), required=True)
    end_date = fields.Date(string='End date', required=True)
    seat = fields.Integer(string='Seat', required=True, default=10)
    students = fields.One2many(string='Students', comodel_name='sm.student', inverse_name='in_class')
    teacher = fields.Many2one(string='Teacher', comodel_name='sm.teacher', ondelete='set null')
    
    empty_seat = fields.Integer(string='Empty_seat', compute='_get_empty_seat', store=True)
    
    @api.constrains('start_date', 'end_date')
    def _check_valid_date(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be less than end date')
    
    @api.constrains('seat')
    def _check_valid_seat(self):
        if self.seat <= 0:
            raise ValidationError('Give available seat to this class')

    @api.depends('students', 'seat')
    def _get_empty_seat(self):
        filled = 0
        for st in self.students:
            filled += 1
        
        self.empty_seat = self.seat - filled      


class Student(models.Model):
    _name = 'sm.student'
    name = fields.Char(string='Student name', required=True)
    birthday = fields.Date(string="Birthday", required=True)
    in_class = fields.Many2one(string='In class', comodel_name='sm.class', ondelete='cascade', required=True)
    rel_empty_seat = fields.Integer(related='in_class.empty_seat', string='Empty seat in this class')
    
    @api.constrains('in_class')
    def _check_seat(self):
        if self.rel_empty_seat <= -1:
            raise ValidationError('This class have no longer empty seat, please choose another class')


class Teacher(models.Model):
    _name = 'sm.teacher'

    name = fields.Char(string='Teacher name', required=True)
    subject = fields.Selection(subjects, string='Subject', required=True)
    birthday = fields.Date(string="Birthday", required=True)
    in_classes = fields.One2many(string='Current classes', comodel_name='sm.class', inverse_name='teacher')
    

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'academy.session'
    
    name = fields.Char(string='Session name', require=True)
    start_date = fields.Date(string='Start date', require=True, default=datetime.today())
    duration = fields.Integer(string='Duration(month)', require=True)
    number_of_seats = fields.Integer(string='Number of seats', require=True)
    current_course = fields.Many2one(string='Course', comodel_name='academy.course', ondelete='set null')
    
    @api.onchange('name')
    def _on_change_name(self):
        return {
        'warning': {
            'title': "Name was changed",
            'message': "It's very bad if this session is promoted, continue change?",
        }   
    }

    @api.constrains('duration')
    def _check_duration(self):
        
        if self.duration > 12:
            raise ValidationError("duration is too long: %s" % self.duration)

        if self.duration <= 0:
            raise ValidationError("invalid duration")


class course(models.Model):
    _name = 'academy.course'
    _rec_name = 'title'
    
    title = fields.Char(string='Course title', require=True)
    description = fields.Text(string='Description', require=True)
    
    price = fields.Float(string='Original price($)', require=True)
    discount = fields.Integer(string="Discount(%)")
    current_session = fields.One2many(string='In session', comodel_name='academy.session', inverse_name='current_course')
    new_price = fields.Float(string="Price after discount($)", compute="_compute_price", store=False)
    
    @api.depends('discount', 'price')
    def _compute_price(self):
        for r in self:
            if r.discount < 0:
                raise ValidationError("invalid duration")
            else:
                r.new_price = 0

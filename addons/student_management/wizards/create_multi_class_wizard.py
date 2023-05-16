

from odoo import fields, api, models


class create_multi_class(models.TransientModel):
    _name = 'sm.create_multi.class.wiz'
    name = fields.Char(string='Class name', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    
    def create_classes(self):
        status = 1
        
        for i in range(self.quantity):
            self.env['sm.class'].name_create(f'{self.name}_clone_{status}')
            status += 1

    def get_default(self):
        default_value = self.env['sm.class'].default_get(['start_date', 'end_date', 'seat', 'subject'])
        message = ''
        for item in default_value:
            message += f'{item} : {default_value[item]}\n' 
        return {
            'name': 'Default details',
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                'type': 'info',
                'sticky': False,
            }
        }

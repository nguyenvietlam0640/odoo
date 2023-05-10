from odoo import fields , models , api


class discount_wizard(models.TransientModel):
    _name = 'sm.update.discount.wiz'
    discount = fields.Integer(string='Update discount(%)', require=True)
    
    def update_fee(self):
        
        self.env['sm.class'].browse(self._context.get('active_ids')).update({'discount':self.discount})

    def update_all_fee(self):
        
        for r in self.env['sm.class'].search([]):
            r.discount = self.discount
    
    
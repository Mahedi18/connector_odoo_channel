from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from .ChannelEngineApi import ChannelEngineApi
from odoo.exceptions import AccessError, UserError, AccessDenied


class ChannelEngineBackend(models.Model):
    _name = "channelengine.backend"
    _description = "ChannelEngine Backend"

    _sql_constraints = [
        ("uniq_host", "unique (host)", "There can be at most one backend per host.")
    ]

    name = fields.Char()
    host = fields.Char(string="Shop url")
    api_key = fields.Char(string="API Key")
    status = fields.Selection([('not_confirmed', 'Not Confirmed'),
                               ('confirmed', 'Confirmed')],
                              default='not_confirmed', string="State")
    check_connection = fields.Boolean(string="Check Connection", default=False)

    def on_confirmed(self):
        if self.check_connection:
            self.status = 'confirmed'
        else:
            raise UserError("Connection is not Checked.")

    def on_reset_confirmed(self):
        self.status = 'not_confirmed'

    def on_check_connection(self):
        config = ChannelEngineApi(self.host, self.api_key)
        res = config.get_api_client('settings')
        if res['StatusCode'] == 200:
            self.write({
                'check_connection': True,
            })
            print(">>>>>>>>>>", self.check_connection)
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "Service working properly."
            return {
                'name': 'Success',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = res['Message']
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sh.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }


# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class SaleVIPCoupon(models.Model):
    _name = 'sale.vip.coupon'
    _description = 'VIP Coupon'

    _rec_name = 'code'

    code = fields.Char(readonly=True, copy=False, default='/')
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string='Customer',
                                 required=True)
    order_line_ids = fields.Many2many(comodel_name='sale.order.line',
                                      string='Order Line',
                                      readonly=True)
    used = fields.Boolean(string='Used',
                          compute='_compute_used',
                          store=True)

    @api.one
    @api.depends(
        'order_line_ids',
        'order_line_ids.state',
    )
    def _compute_used(self):
        order_line = None
        for line in self.order_line_ids:
            if line.state not in 'cancel':
                # we can have only 1 'non-canceled' line with the coupon
                order_line = line
                break
        self.used = bool(order_line)

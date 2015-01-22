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

from openerp import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vip_coupon_ids = fields.Many2many(comodel_name='sale.vip.coupon',
                                      string='Coupon')

    @api.multi
    def _prepare_vip_coupon_line(self, coupons):
        products = ', '.join(self.mapped('name'))
        price_unit = -sum(self.mapped('price_subtotal'))
        first_line = self[0]
        codes = ', '.join(coupon.code for coupon in coupons)
        return {
            'name': _('VIP Coupons %s on: %s') % (codes, products),
            'product_uom_qty': 1,
            'price_unit': price_unit,
            'vip_coupon_ids': [(6, 0, coupons.ids)],
            'order_id': first_line.order_id.id,
        }

    @api.multi
    def use_vip_coupon(self, coupons):
        values = self._prepare_vip_coupon_line(coupons)
        return self.create(values)

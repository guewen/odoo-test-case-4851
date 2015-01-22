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

from openerp.tests import common


class TestCouponUsed(common.TransactionCase):

    def setUp(self):
        super(TestCouponUsed, self).setUp()
        self.coupon_obj = self.env['sale.vip.coupon']
        self.order_obj = self.env['sale.order']
        self.order_line_obj = self.env['sale.order.line']
        self.product_obj = self.env['product.product']
        self.partner_obj = self.env['res.partner']

    def test_coupon_ordered(self):
        partner = self.partner_obj.create({'name': 'Valentine Wiggin'})
        coupon_obj = self.env['sale.vip.coupon']
        values = {
            'partner_id': partner.id,
        }
        coupon = coupon_obj.create(values)
        product = self.product_obj.create({'name': 'Yerba Mate',
                                           'list_price': 47})
        order = self.order_obj.create({'partner_id': partner.id})
        line = self.order_line_obj.create({'order_id': order.id,
                                           'name': 'Order Line',
                                           'product_id': product.id})
        line.use_vip_coupon(coupon)
        self.assertTrue(coupon.used)

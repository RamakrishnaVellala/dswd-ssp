# -*- coding: utf-8 -*-
# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class dswd_registry_individuals(models.Model):
    _inherit = "res.partner"

    occupation = fields.Char(string='Occupation')
    income = fields.Float(string='Income')
# -*- coding: utf-8 -*-

from odoo import models, fields

class Theloaisach(models.Model):
    _name = 'quanlythuvien.theloaisach'
    _rec_name = 'tentheloai'

    tentheloai = fields.Char("Tên thể loại sách", required=True)
    mota = fields.Text(string="Mô tả")
    sach = fields.One2many('quanlythuvien.sach', 'theloai_chinh', string="Gồm những cuốn sách")
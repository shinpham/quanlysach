# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Sach(models.Model):
    _name = 'quanlythuvien.sach'
    _rec_name = 'tensach'

    tensach = fields.Char("Tên sách", required=True)
    mota = fields.Text(string="Mô tả")
    tacgia = fields.Char("Tác giả")
    nhaxuatban = fields.Char("Nhà xuất bản")
    gia = fields.Float(string="Giá")
    soluong = fields.Float(string="Số lượng")
    namxuatban = fields.Selection(string="Năm xuất bản", selection=[('2015', 'Năm 2015'), ('2016', 'Năm 2016')])
    hethang = fields.Boolean(string="Hết hàng")
    so = fields.Integer(string="Số")
    theloai_chinh = fields.Many2one('quanlythuvien.theloaisach', string="Thể loại sách", required=True)
    length = fields.Integer(compute='_name_lenth',string ="Độ dài tên sách")
    soluongsach = fields.Integer(string="Số lượng sách trong kho")

    status = fields.Selection(string="Status",
                              selection=[
                                  ('1', 'Còn hàng'),
                                  ('2', 'Sắp hết hàng'),
                                  ('3', 'Hết hàng')
                              ])

    state = fields.Selection([
        ('new', 'New'),
        ('open', 'Open')
    ])

    _sql_constraints = [('ten_sach_unique', 'UNIQUE(tensach)', 'Tên sách đã tồn tại')]

    tinh_trang_kho = fields.Selection([
        ('con', 'Còn hàng'),
        ('het', 'Hết hàng'),
        ('saphet', 'Sắp hết hàng')
    ])
    data = fields.Binary('File')

    @api.multi
    @api.onchange('hethang')
    def update_status(self):
        self.ensure_one()
        if self.hethang is True:
            self.tinh_trang_kho = 'het'
        else:
            self.tinh_trang_kho = 'con'

    @api.multi
    @api.onchange('status')
    def update_status(self):
        self.ensure_one()
        if self.status == '1':
            self.tinh_trang_kho = 'con'
        elif self.status == '2':
            self.tinh_trang_kho = 'saphet'
        else:
            self.tinh_trang_kho = 'het'

    @api.one
    def new_progressbar(self):
        self.write({
            'state': 'new',
        })

    @api.one
    def open_progressbar(self):
        self.write({
            'state': 'open'
        })

    @api.multi
    @api.constrains("tensach")
    def kiemtra_tensach(self):
        if len(self.tensach) < 5:
            raise  exceptions.ValidationError("Tên sách quá ngắn")

    @api.depends('tensach')
    def _name_lenth(self):
        if (self.tensach):
            self.length = len(self.tensach)
        else:
            self.length = 0

    @api.depends('gia', 'soluong')
    def _tonggia(self):
        self.tonggia = self.gia * self.soluong
    tonggia = fields.Float(string="Tong gia", store=True, compute="_tonggia")

    @api.model
    def trang_thai_kho_hang(self, sl):
        if 0 < sl < 10:
            self.status = '2'
        elif sl == 0:
            self.status = '3'
        else:
            self.status = '1'

    @api.onchange("soluongsach")
    def thaysoi_soluong(self):
        self.trang_thai_kho_hang(self.soluongsach)


    @api.multi
    @api.onchange('soluong')
    def update_statuss(self):
        self.ensure_one()
        if self.soluong == '0':
            self.status = '3'
        elif 0 < self.soluong < 5:
            self.status = '2'
        else:
            self.status = '1'

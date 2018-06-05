from odoo import models, fields, api, _
from tempfile import TemporaryFile
import openpyxl
import base64
from xlrd import open_workbook


class ExcelReader(models.TransientModel):
    _name = "quanlythuvien.reader.excel"

    excel_file = fields.Binary(string='Import File')
    name = fields.Char()
    ho = fields.Char()
    age = fields.Char()

    @api.multi
    def import_excel(self):
        # Generating of the excel file to be read by openpyxl
        excel_file = self.excel_file.decode('base64')
        excel_fileobj = TemporaryFile('wb+')
        excel_fileobj.write(excel_file)
        excel_fileobj.seek(1)

        # Create workbook
        workbook = openpyxl.load_workbook(excel_fileobj, data_only=True)
        # Get the first sheet of excel file
        sheet = workbook[workbook.get_sheet_names()[0]]

        # Iteration on each rows in excel
        # for row in itertools.imap(sheet.row, range(sheet.nrows)):
        for row in sheet.rows:
            # xét row nếu khác 1 thì get giá trị
            while row != 1:
                v1 = row[0].value
                v2 = row[1].value
                v3 = row[2].value
                # nếu row[0] nhỏ hơn 2 <=> dòng đầu tiên = 1 thì ko đc ghi
                if row[0].row >= 2:
                    self.env['quanlythuvien.reader.excel'].create({'name': v1, 'ho': v2, 'age': v3})
                break
                # Get value
            # Create your record
        # return{
        #         'name': _('Import'),
        #         'res_model': 'quanlythuvien.reader.excel',
        #         'type': 'ir.actions.act_window',
        #         'view_id': False,
        #         'view_mode': 'tree,form',
        #         'view_type': 'tree',
        # }
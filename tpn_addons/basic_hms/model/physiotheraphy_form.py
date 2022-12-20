from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from random import choice
from string import digits
from pygame import mixer


class PhysiotheraphyPatient(models.Model):
    _name = 'patient.physiotheraphy'
    _description = ' Patient Physiotheraphy Form'

    name = fields.Char(string="Patient Name")
    patient_age = fields.Char(string="Patient Age")
    patient_dob = fields.Date(string="Patient Date of Birth")
    in_patient = fields.Char(string="I.P.NO")
    patient_gender = fields.Char(string="Gender")
    ward = fields.Char(string="Ward")
    room_no = fields.Char(string="Room No")
    surgery_date = fields.Datetime(string="Surgery Date")
    diagonsis = fields.Text(string="Diagonsis")
    surgery_procedure = fields.Text(string="Surgery Procedure")
    treatment_plan = fields.Integer(string="Treatment Plan")
    patient_physiotheraphy_line_ids = fields.One2many('patient.physiotheraphy.line', 'name', 'Patient Physiotheraphy')
    out_come = fields.Text(string="Physiotherapy Out Come ")
    discharge_advice = fields.Text(string="Discharge Advice")
    observation = fields.Text(string="Medical Observation")

    @api.onchange('treatment_plan')
    def onchange_name(self):
        record = self.treatment_plan
        for rec in range(record):
            count = +rec + 1
            days = 'Day'
            final = days + '' + str(count)
            b_list = [[0, 0, {
                'date': final,
                'boolean_name': True,
            }]]
            for i in range(1):
                b_list.append([0, 0, {
                    'mrg_eve': 'mrg',

                }])
            for i in range(1):
                b_list.append([0, 0, {
                    'mrg_eve': 'eve',
                }])
            self.write({'patient_physiotheraphy_line_ids': b_list})


class PhysiotheraphyPatientLine(models.Model):
    _name = 'patient.physiotheraphy.line'
    _description = ' Patient Physiotheraphy Line'

    date = fields.Char(string="Date")
    physiotheraphy = fields.Char(string="Physiotheraphy")
    remark = fields.Char(string="REMARKS")
    signature = fields.Char(string="SIGNATURE")
    name = fields.Many2one('patient.physiotheraphy', 'Patient Physiotheraphy')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    mrg_eve = fields.Selection([
        ('mrg', 'Morning'),
        ('eve', 'Evening'),
    ], string='Mrg/ Eve')
    boolean_name = fields.Boolean('REMARKS')
    line_number = fields.Integer(string='#', default=1)

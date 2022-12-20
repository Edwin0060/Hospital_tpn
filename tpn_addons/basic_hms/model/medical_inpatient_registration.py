# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import date, datetime


class medical_inpatient_registration(models.Model):
    _name = 'medical.inpatient.registration'
    _description = 'Medical Inpatient Registration'

    name = fields.Char(string="Registration Code", copy=False, readonly=True, index=True)
    patient_id = fields.Many2one('medical.patient', string="Patient", required=True)
    hospitalization_date = fields.Datetime(string="Hospitalization date", required=True)
    discharge_date = fields.Datetime(string="Expected Discharge date", required=True)
    attending_physician_id = fields.Many2one('medical.physician', string="Attending Physician")
    operating_physician_id = fields.Many2one('medical.physician', string="Operating Physician")
    admission_type = fields.Selection(
        [('routine', 'Routine'), ('maternity', 'Maternity'), ('elective', 'Elective'), ('urgent', 'Urgent'),
         ('emergency', 'Emergency  ')], required=True, string="Admission Type")
    medical_pathology_id = fields.Many2one('medical.pathology', string="Reason for Admission")
    info = fields.Text(string="Extra Info")
    bed_transfers_ids = fields.One2many('bed.transfer', 'inpatient_id', string='Transfer Bed', readonly=True)
    medical_diet_belief_id = fields.Many2one('medical.diet.belief', string='Belief')
    therapeutic_diets_ids = fields.One2many('medical.inpatient.diet', 'medical_inpatient_registration_id',
                                            string='Therapeutic_diets')
    diet_vegetarian = fields.Selection([('none', 'None'), ('vegetarian', 'Vegetarian'), ('lacto', 'Lacto Vegetarian'),
                                        ('lactoovo', 'Lacto-Ovo-Vegetarian'), ('pescetarian', 'Pescetarian'),
                                        ('vegan', 'Vegan')], string="Vegetarian")
    nutrition_notes = fields.Text(string="Nutrition notes / Directions")
    state = fields.Selection(
        [('free', 'Free'), ('confirmed', 'Confirmed'), ('hospitalized', 'Hospitalized'), ('cancel', 'Cancel'),
         ('done', 'Done')], string="State", default="free")
    nursing_plan = fields.Text(string="Nursing Plan")
    discharge_plan = fields.Text(string="Discharge Plan")
    icu = fields.Boolean(string="ICU")
    medication_ids = fields.One2many('medical.inpatient.medication', 'medical_inpatient_registration_id',
                                     string='Medication')
    physiotheraphy_count = fields.Integer(compute='_compute_physiotheraphy_count')

    def _compute_physiotheraphy_count(self):
        self.physiotheraphy_count = self.env['patient.physiotheraphy'].sudo(). \
            search_count([('in_patient', '=', self.name)])

    def get_physiotheraphy_action(self):
        self.sudo().ensure_one()
        context = dict(self._context or {})
        active_model = context.get('active_model')
        form_view = self.sudo().env.ref('basic_hms.view_physiotheraphy_form_form')
        tree_view = self.sudo().env.ref('basic_hms.view_physiotheraphy_form_tree')
        return {
            'name': _('Patient Physiotheraphy '),
            'res_model': 'patient.physiotheraphy',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'domain': [('in_patient', '=', self.name)],
        }

    def patient_physiotheraphy(self):
        print('**********************', )
        create_patient = self.env['patient.physiotheraphy']
        create_patient.create({
            'name': self.patient_id.patient_name,
            'patient_age': self.patient_id.age,
            'patient_dob': self.patient_id.date_of_birth,
            'patient_gender': dict(self.patient_id._fields['sex'].selection).get(self.patient_id.sex),
            'in_patient': self.name,
        })

    @api.model
    def default_get(self, fields):
        result = super(medical_inpatient_registration, self).default_get(fields)
        patient_id = self.env['ir.sequence'].next_by_code('medical.inpatient.registration')
        if patient_id:
            result.update({
                'name': patient_id,
            })
        return result

    def registration_confirm(self):
        self.write({'state': 'confirmed'})

    def registration_admission(self):
        self.write({'state': 'hospitalized'})

    def registration_cancel(self):
        self.write({'state': 'cancel'})

    def patient_discharge(self):
        self.write({'state': 'done'})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:s

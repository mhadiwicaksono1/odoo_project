from odoo import models, fields, api

class WarehouseContract(models.Model):
    _name = 'warehouse.contract'
    _description = 'Warehouse Contract'

    name = fields.Char(string='Nomor Kontrak', required=True, default='New')
    nota_number = fields.Char(string='Nomor Nota')
    partner_id = fields.Many2one('res.partner', string='Ditagih Kepada')
    date_start = fields.Date(string='Periode Kontrak Dari')
    date_end = fields.Date(string='Periode Kontrak Hingga')
    warehouse_type = fields.Selection([
        ('tertutup', 'Tertutup'),
        ('terbuka', 'Terbuka')
    ], string='Jenis Gudang', default='tertutup')
    warehouse_name = fields.Char(string='Nama Gudang')
    
    line_ids = fields.One2many('warehouse.contract.line', 'contract_id', string='Rincian Kontrak')
    
    total_rent = fields.Monetary(string='Total Biaya Sewa', compute='_compute_totals', store=True)
    total_tax = fields.Monetary(string='Pajak 10%', compute='_compute_totals', store=True)
    total_after_tax = fields.Monetary(string='Sewa Setelah Pajak', compute='_compute_totals', store=True)
    total_revenue_sharing = fields.Monetary(string='Revenue Sharing', compute='_compute_totals', store=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('line_ids.total_rent', 'line_ids.tax_amount', 'line_ids.total_after_tax', 'line_ids.revenue_sharing')
    def _compute_totals(self):
        for record in self:
            record.total_rent = sum(line.total_rent for line in record.line_ids)
            record.total_tax = sum(line.tax_amount for line in record.line_ids)
            record.total_after_tax = sum(line.total_after_tax for line in record.line_ids)
            record.total_revenue_sharing = sum(line.revenue_sharing for line in record.line_ids)


class WarehouseContractLine(models.Model):
    _name = 'warehouse.contract.line'
    _description = 'Warehouse Contract Line'

    contract_id = fields.Many2one('warehouse.contract', string='Contract', ondelete='cascade')
    company_id = fields.Many2one('res.partner', string='Nama Perusahaan')
    date_start = fields.Date(string='Dari')
    date_end = fields.Date(string='Hingga')
    total_months = fields.Integer(string='Total Bulan Kontrak')
    grace_period = fields.Integer(string='Grass Periode (Bulan)')
    
    billable_months = fields.Integer(string='Total Bulan (Billable)', compute='_compute_amounts', store=True)
    monthly_rent = fields.Monetary(string='Sewa per Bulan')
    
    total_rent = fields.Monetary(string='Total Biaya Sewa', compute='_compute_amounts', store=True)
    tax_amount = fields.Monetary(string='Pajak 10%', compute='_compute_amounts', store=True)
    total_after_tax = fields.Monetary(string='Sewa Setelah Pajak', compute='_compute_amounts', store=True)
    revenue_sharing = fields.Monetary(string='Revenue Sharing ke PB (5%)', compute='_compute_amounts', store=True)
    
    currency_id = fields.Many2one('res.currency', related='contract_id.currency_id', store=True)

    @api.depends('total_months', 'grace_period', 'monthly_rent')
    def _compute_amounts(self):
        for line in self:
            line.billable_months = line.total_months - line.grace_period
            line.total_rent = line.billable_months * line.monthly_rent
            line.tax_amount = line.total_rent * 0.10
            line.total_after_tax = line.total_rent - line.tax_amount
            line.revenue_sharing = line.total_after_tax * 0.05

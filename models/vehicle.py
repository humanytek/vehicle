from openerp import api, fields, models


class Vehicle(models.Model):
    _name = 'vehicle'

    name = fields.Char()

    humidity_rate = fields.Float()
    damage_rate = fields.Float()
    break_rate = fields.Float()
    impurity_rate = fields.Float()

    density = fields.Float()
    temperature = fields.Float()
    transgenic = fields.Float()

    raw_kilos = fields.Float(compute="_compute_raw_kilos", store=False)

    humid_kilos = fields.Float(compute="_compute_humid_kilos", store=False)
    damaged_kilos = fields.Float(compute="_compute_damaged_kilos", store=False)
    broken_kilos = fields.Float(compute="_compute_broken_kilos", store=False)
    impure_kilos = fields.Float(compute="_compute_impure_kilos", store=False)

    deducted_kilos = fields.Float(compute="_compute_deducted_kilos", store=False)

    clean_kilos = fields.Float(compute="_compute_clean_kilos", store=False)

    ticket = fields.Integer()

    stock_picking = fields.Many2one('stock.picking', readonly=True)

    state = fields.Selection(
    {
        'ready_transfer': 'Ready to transfer',
        'done': 'Done',
    })

    @api.one
    def _compute_raw_kilos(self):
        self.net_kilos = 0

    @api.one
    @api.depends('raw_kilos', 'humidity_rate')
    def _compute_humid_kilos(self):
        if self.humidity_rate > 14:
            self.humid_kilos = self.raw_kilos * (self.humidity_rate - 14) * .0116
        else:
            self.humid_kilos = 0

    @api.one
    def _compute_damaged_kilos(self):
        if self.damage_rate > 5:
            self.damaged_kilos = self.raw_kilos * (self.damage_rate - 5) / 100
        else:
            self.damaged_kilos = 0

    @api.one
    def _compute_broken_kilos(self):
        if self.break_rate > 2:
            self.broken_kilos = self.raw_kilos * (self.break_rate - 2) / 100
        else:
            self.broken_kilos = 0

    @api.one
    def _compute_impure_kilos(self):
        if self.impurity_rate > 2:
            self.impure_kilos = self.raw_kilos * (self.impurity_rate - 2) / 100
        else:
            self.impure_kilos = 0

    @api.one
    def _compute_deducted_kilos(self):
        self.deducted_kilos = self.humid_kilos + self.damaged_kilos + self.broken_kilos + self.impure_kilos

    @api.one
    def _compute_clean_kilos(self):
        self.clean_kilos = self.raw_kilos - self.deducted_kilos

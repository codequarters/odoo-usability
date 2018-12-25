# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.tools import misc
from odoo.tools import float_compare


class BaseUsabilityInstalled(models.AbstractModel):
    _name = "base.usability.installed"


formatLang_original = misc.formatLang

def formatLang(self, value, digits=None, grouping=True, monetary=False,
               dp=False, currency_obj=False, int_no_digits=True):
    with api.Environment.manage():
        env = api.Environment(self.cr, self.uid, {})
        if (
                'base.usability.installed' in env and
                int_no_digits and
                not monetary and
                isinstance(value, float) and
                dp):
            prec = env['decimal.precision'].precision_get(dp)
            if not float_compare(value, int(value), precision_digits=prec):
                digits = 0
                dp = False
    res = formatLang_original(
        self, value, digits=digits, grouping=grouping, monetary=monetary,
        dp=dp, currency_obj=currency_obj)
    return res


misc.formatLang = formatLang

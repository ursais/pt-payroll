import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

RULE_UPDATES = {
    "rule_pt_provision_for_holidays": "result = not get_first_year_of_contract(payslip)",
    "rule_pt_provision_for_holidays_0": "result = get_first_year_of_contract(payslip)",
    "rule_pt_provision_total_for_holidays": "result = True",
    "rule_pt_provision_for_christmas": "result = not get_first_year_of_contract(payslip)",
    "rule_pt_provision_for_christmas_0": "result = get_first_year_of_contract(payslip)",
    "rule_pt_provision_total_for_christmas": "result = True",
}


def migrate(cr, version):
    """Manually update salary rule fields that can't be updated via noupdate XML."""
    env = api.Environment(cr, SUPERUSER_ID, {})

    for xml_id, new_condition in RULE_UPDATES.items():
        try:
            rule = env.ref(f"ptplus_payroll_ee.{xml_id}")
            if rule.condition_python != new_condition:
                rule.write(
                    {
                        "condition_python": new_condition,
                        "active": False,
                    }
                )
                # Set noupdate=True in ir.model.data
            data_rec = env["ir.model.data"].search(
                [("module", "=", "ptplus_payroll_ee"), ("name", "=", xml_id)], limit=1
            )

            if data_rec and not data_rec.noupdate:
                data_rec.write({"noupdate": True})
        except Exception as e:
            _logger.warning(f"Could not update rule {xml_id}: {e}")

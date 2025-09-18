import logging

from openupgradelib import openupgrade

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )
    for company in companies:
        slips = env["hr.payslip"].search(
            [
                ("company_id", "=", company.id),
            ]
        )
        pt_slips = slips.filtered(lambda slip: slip.struct_id.country_id.code == "PT")
        for slip in pt_slips:
            try:
                for worked_day in slip.worked_days_line_ids:
                    if "FALTA" in worked_day.work_entry_type_id.code:
                        worked_day.compute_missing_days_for_dri(worked_day)
                        missing_days_curr_period = (
                            worked_day.l10n_pt_missing_days_for_dri_curr_period
                        )
                        missing_days_prev_period = (
                            worked_day.l10n_pt_missing_days_for_dri_prev_period
                        )
                        total_missing_days = (
                            missing_days_curr_period + missing_days_prev_period
                        )
                        if total_missing_days:
                            worked_day.l10n_pt_leave_amount_curr_period = (
                                missing_days_curr_period * worked_day.amount
                            ) / total_missing_days
                            worked_day.l10n_pt_leave_amount_prev_period = (
                                missing_days_prev_period * worked_day.amount
                            ) / total_missing_days
                _logger.info(slip.name)
            except UserError as e:
                _logger.warning(slip.name, e)

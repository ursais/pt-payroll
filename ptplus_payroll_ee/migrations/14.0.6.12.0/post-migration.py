from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )
    # Note: This migration script is designed to update the values for DRI.
    # Note: Now, work entries defined as unpaid do not count as work days in DRI.
    for company in companies:
        slips = env["hr.payslip"].search([("company_id", "=", company.id)])
        for slip in slips:
            try:
                (
                    slip.l10n_pt_ref_per_days_worked_for_dri,
                    slip.l10n_pt_prev_month_missing_days_for_dri,
                ) = slip.get_values_for_dri(slip)
            except Exception:
                slip.l10n_pt_ref_per_days_worked_for_dri = 0
                slip.l10n_pt_prev_month_missing_days_for_dri = 0

from openupgradelib import openupgrade

accounts_codes = [
    "631",
    "632",
    "2311",
    "2312",
]


@openupgrade.migrate()
def migrate(env, version):
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )
    for company in companies:
        slips = env["hr.payslip"].search([("company_id", "=", company.id)])

        for slip in slips:
            slip.l10n_pt_absence_type = company.l10n_pt_absence_computation_method
            try:
                (
                    slip.l10n_pt_ref_per_days_worked_for_dri,
                    slip.l10n_pt_prev_month_missing_days_for_dri,
                ) = slip.get_values_for_dri()
            except Exception:
                slip.l10n_pt_ref_per_days_worked_for_dri = 0
                slip.l10n_pt_prev_month_missing_days_for_dri = 0

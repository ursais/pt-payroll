from openupgradelib import openupgrade


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
            if slip.date_from and slip.date_to:
                slip.l10n_pt_reference_period = str(slip.date_to.month)
                if slip.date_from.month != slip.date_to.month:
                    slip.l10n_pt_different_months = True
                else:
                    slip.l10n_pt_different_months = False

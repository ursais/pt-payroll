from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    new_regime = env["hr.special.fiscal.regime.pt"].search(
        [("code", "=", "50_year_youth_irs")], limit=1
    )
    employees = env["hr.employee"].search([])
    for employee in employees:
        old_regime = employee.l10n_pt_special_fiscal_regime_id.filtered(
            lambda regime: regime.code == "4_year_youth_irs"
        )
        if old_regime and new_regime:
            for regime in employee.l10n_pt_special_fiscal_regime_id:
                if regime.code == "4_year_youth_irs":
                    employee.l10n_pt_special_fiscal_regime_id = [(3, regime.id)]
                    employee.l10n_pt_special_fiscal_regime_id = [(4, new_regime.id)]

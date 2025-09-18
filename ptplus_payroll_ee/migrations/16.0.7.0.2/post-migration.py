from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    structure_pt_monthly_pay = env.ref(
        "ptplus_payroll_ee.hr_payroll_structure_pt_monthly_pay",
        raise_if_not_found=False,
    )

    if not structure_pt_monthly_pay:
        return

    for rule in structure_pt_monthly_pay.rule_ids:
        if rule.code == "BASIC":
            rule.write({"l10n_pt_monthly_income": True})

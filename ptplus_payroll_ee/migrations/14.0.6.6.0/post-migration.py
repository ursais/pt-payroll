from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Note: This migration file was developed only for Enterprise Edition
    salary_rules = env["hr.salary.rule"].search([])

    rule_pt_unused_holidays = env.ref("ptplus_payroll_ee.rule_pt_unused_holidays")
    rule_pt_holiday_allowance_pro = env.ref(
        "ptplus_payroll_ee.rule_pt_holiday_allowance_pro"
    )
    rule_pt_christmas_allowance_pro = env.ref(
        "ptplus_payroll_ee.rule_pt_christmas_allowance_pro"
    )

    new_rules_codes = [
        rule_pt_unused_holidays.code,
        rule_pt_holiday_allowance_pro.code,
        rule_pt_christmas_allowance_pro.code,
    ]

    new_rules_ids = [
        rule_pt_unused_holidays.id,
        rule_pt_holiday_allowance_pro.id,
        rule_pt_christmas_allowance_pro.id,
    ]

    for rule in salary_rules:
        if rule.code in new_rules_codes and rule.id not in new_rules_ids:
            rule.active = False  # Deactivating the rule

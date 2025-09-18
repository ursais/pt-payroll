from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "ptplus_payroll_ee.input_pt_meal_allowance_ticket_days",
                "ptplus_payroll_ee.input_pt_meal_allowance_days",
            ),
        ],
    )

    # this code changes the "salary_rule_id" field to unlink the rule
    # "rule_en_meal_allowance_ticket_days" from the payrlsip lines that
    # have it and then remove it from the ptplus_payroll_rules.xml file.
    record = env.ref(
        "ptplus_payroll_ee.rule_pt_meal_allowance_ticket_days", raise_if_not_found=False
    )
    if record:
        slip_lines = env["hr.payslip.line"].search([("salary_rule_id", "=", record.id)])
        for line in slip_lines:
            line.write(
                {
                    "salary_rule_id": env.ref(
                        "ptplus_payroll_ee.rule_pt_meal_allowance_ticket"
                    ).id
                }
            )

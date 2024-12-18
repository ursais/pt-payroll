from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )

    # Remove rule "Vencimento Base Tributável".
    # Was no longer necessary.
    taxable_base_salary = env.ref(
        "ptplus_payroll_ee.rule_pt_taxable_base_salary", raise_if_not_found=False
    )

    if taxable_base_salary:
        for company in companies:
            slips = env["hr.payslip"].search([("company_id", "=", company.id)])

            for slip in slips:
                for line in slip.line_ids:
                    if line.salary_rule_id == taxable_base_salary:
                        line.unlink()

        taxable_base_salary.unlink()

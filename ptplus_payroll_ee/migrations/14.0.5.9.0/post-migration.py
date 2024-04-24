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
            for line in slip.line_ids:
                if line.code == "KMS_VPROP":
                    line.write({"code": "DES_VPROP"})
                rule = line.salary_rule_id
                total = line.total
                quantity = line.quantity
                (
                    amount_subject_to_it,
                    amount_exempt_to_it,
                    amount_subject_to_ss,
                ) = slip.get_s_and_e_amounts(rule, total, quantity)

                line.update(
                    {
                        "l10n_pt_amount_subject_to_it": amount_subject_to_it,
                        "l10n_pt_amount_exempt_to_it": amount_exempt_to_it,
                        "l10n_pt_amount_subject_to_ss": amount_subject_to_ss,
                    }
                )

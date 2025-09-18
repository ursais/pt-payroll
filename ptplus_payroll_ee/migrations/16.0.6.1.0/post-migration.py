from openupgradelib import openupgrade

ACCOUNTS_CODES = [
    "631",
    "632",
    "2311",
    "2312",
    "6263",
    "245",
    "242",
]


@openupgrade.migrate()
def migrate(env, version):
    companies = (
        env["res.company"]
        .search([])
        .filtered(lambda r: r.country_id == env.ref("base.pt"))
    )
    for company in companies:
        accounts = {}
        for code in ACCOUNTS_CODES:
            account = env["account.account"].search(
                [("company_id", "=", company.id), ("code", "like", "%s%%" % code)],
                limit=1,
            )
            accounts[code] = account

        RULES_TO_BE_UPDATED = [
            "SS",
            "IRS",
            "DED_SEG_S",
            "IRS_SOMA_BASE_TOTAL",
        ]

        rules = env["hr.salary.rule"].search(
            [
                ("struct_id.country_id.code", "=", "PT"),
                ("code", "in", RULES_TO_BE_UPDATED),
            ]
        )

        for rule in rules:
            if rule.code == "SS":
                accounts_dict = {
                    "account_debit": accounts["245"],
                    "account_credit": accounts["2312"],
                    "l10n_pt_account_debit_corporate_body": accounts["245"],
                    "l10n_pt_account_credit_corporate_body": accounts["2311"],
                }
            elif rule.code == "IRS":
                accounts_dict = {
                    "account_debit": accounts["242"],
                    "account_credit": accounts["2312"],
                    "l10n_pt_account_debit_corporate_body": accounts["242"],
                    "l10n_pt_account_credit_corporate_body": accounts["2311"],
                }
            elif rule.code == "DED_SEG_S":
                accounts_dict = {
                    "account_debit": accounts["6263"],
                    "account_credit": accounts["2312"],
                    "l10n_pt_account_debit_corporate_body": accounts["6263"],
                    "l10n_pt_account_credit_corporate_body": accounts["2311"],
                }
            elif rule.code == "IRS_SOMA_BASE_TOTAL":
                # remove accounts
                accounts_dict = {
                    "account_debit": "",
                    "account_credit": "",
                    "l10n_pt_account_debit_corporate_body": "",
                    "l10n_pt_account_credit_corporate_body": "",
                }
            else:
                continue

            rule.write(accounts_dict)

        slips = env["hr.payslip"].search([("company_id", "=", company.id)])

        for slip in slips:
            for line in slip.line_ids:
                rule = line.salary_rule_id
                dmr_subject_code = rule.l10n_pt_dmr_subject_amount
                dmr_exempt_code = rule.l10n_pt_dmr_exempt_amount
                is_not_subject_dmr = not dmr_subject_code or dmr_subject_code == "N/A"
                is_exempt_dmr = dmr_exempt_code and dmr_exempt_code != "N/A"

                if is_not_subject_dmr and is_exempt_dmr:
                    # fix subject and exempt amounts for exempt rules
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

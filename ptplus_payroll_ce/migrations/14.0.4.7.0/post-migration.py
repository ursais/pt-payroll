from openupgradelib import openupgrade

accounts_codes = [
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
        for code in accounts_codes:
            account = env["account.account"].search(
                [("company_id", "=", company.id), ("code", "like", "%s%%" % code)],
                limit=1,
            )
            accounts[code] = account

        rules_to_be_updated = [
            "SS",
            "IRS",
            "DED_SEG_S",
        ]

        rules = env["hr.salary.rule"].search(
            [
                ("company_id", "=", company.id),
                ("code", "in", rules_to_be_updated),
            ]
        )

        for rule in rules:
            if rule.code == "SS":
                accounts_dict = {
                    "account_debit": accounts["2312"],
                    "account_credit": accounts["245"],
                    "l10n_pt_account_debit_corporate_body": accounts["2311"],
                    "l10n_pt_account_credit_corporate_body": accounts["245"],
                }
            elif rule.code == "IRS":
                accounts_dict = {
                    "account_debit": accounts["2312"],
                    "account_credit": accounts["242"],
                    "l10n_pt_account_debit_corporate_body": accounts["2311"],
                    "l10n_pt_account_credit_corporate_body": accounts["242"],
                }
            elif rule.code == "DED_SEG_S":
                accounts_dict = {
                    "account_debit": accounts["6263"],
                    "account_credit": accounts["2312"],
                    "l10n_pt_account_debit_corporate_body": accounts["6263"],
                    "l10n_pt_account_credit_corporate_body": accounts["2311"],
                }
            else:
                continue

            rule.write(accounts_dict)

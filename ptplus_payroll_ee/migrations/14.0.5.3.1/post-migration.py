from openupgradelib import openupgrade

ACCOUNT_CODES = [
    "631",
    "632",
    "2311",
    "2312",
]


@openupgrade.migrate()
def migrate(env, version):
    # Get a list of companies using Exo's chart of accounts
    chart_templates = env["account.chart.template"]._get_pt_charts()
    companies = env["res.company"].search(
        [("chart_template_id", "in", chart_templates.ids)]
    )

    # Replace accounts/rules on each one
    for company in companies:
        accounts = {}
        for code in ACCOUNT_CODES:
            account = env["account.account"].search(
                [("company_id", "=", company.id), ("code", "like", "%s%%" % code)],
                limit=1,
            )
            accounts[code] = account

        rules_to_be_updated = [
            "TICKET_EDUC",
            "OUT_REN_ESP",
            "REND_ESP_2CIRS",
        ]

        rules = env["hr.salary.rule"].search(
            [
                ("struct_id.country_id.code", "=", "PT"),
                ("code", "in", rules_to_be_updated),
            ]
        )

        for rule in rules:
            rule.write(
                {
                    "account_credit": accounts["2312"],
                    "account_debit": accounts["632"],
                    "l10n_pt_account_credit_corporate_body": accounts["2311"],
                    "l10n_pt_account_debit_corporate_body": accounts["631"],
                },
            )

from openupgradelib import openupgrade

accounts_codes = [
    "631",
    "632",
    "2311",
    "2312",
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
            "TIC_ENS_CHE_EST",
            "TIC_INF_CHE_CRE",
            "AC_S_REGR_DIA_RES",
            "AC_C_REGR_DIA_RES",
            "SUBS_DESLO",
            "FALTA310",
        ]

        rules = env["hr.salary.rule"].search(
            [
                ("struct_id.country_id.code", "=", "PT"),
                "|",
                ("code", "in", rules_to_be_updated),
                ("category_id.code", "=", "DES"),
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

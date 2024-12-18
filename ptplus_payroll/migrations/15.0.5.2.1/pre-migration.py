from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if "l10n_pt_fiscal_regime" in env["hr.employee"]._fields:
        openupgrade.rename_fields(
            env,
            [
                (
                    "hr.employee",
                    "hr_employee",
                    "l10n_pt_fiscal_regime",
                    "l10n_pt_special_fiscal_regime",
                ),
            ],
        )

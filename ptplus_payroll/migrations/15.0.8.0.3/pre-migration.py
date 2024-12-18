from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        CREATE TABLE temp_table_mig (id SERIAL PRIMARY KEY, employee_id INTEGER, value VARCHAR(255));
        """,
    )

    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO temp_table_mig (employee_id, value)
        SELECT id, l10n_pt_special_fiscal_regime FROM hr_employee WHERE l10n_pt_special_fiscal_regime IS NOT NULL;
        """,
    )


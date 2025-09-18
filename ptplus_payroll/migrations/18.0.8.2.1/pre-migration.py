import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """
    This pre-migration script is designed to transfer data from the company_dependent field
    l10n_pt_professional_category, into a temporary column in the hr_employee table.
    """

    _logger.info(
        "Adding temporary column 'l10n_pt_professional_category_tmp' to table 'hr_employee'..."
    )
    env.cr.execute(
        """
        ALTER TABLE hr_employee
        ADD COLUMN l10n_pt_professional_category_tmp INT;
    """
    )
    _logger.info("Temporary column added.")

    # Select id and JSON field from all hr_employee records with non-null professional category
    env.cr.execute("""
        SELECT id, l10n_pt_professional_category, company_id
        FROM hr_employee
        WHERE l10n_pt_professional_category IS NOT NULL
    """)
    rows = env.cr.fetchall()

    for emp_id, prof_cat_json, company_id in rows:
        value_to_set = None
        # prof_cat_json is already a Python dict when fetched from jsonb
        if isinstance(prof_cat_json, dict):
            # Use company_id as string key (or int if keys are int)
            comp_key = str(company_id)
            if comp_key in prof_cat_json:
                value_to_set = prof_cat_json[comp_key]
            elif prof_cat_json:
                # fallback: first value
                value_to_set = next(iter(prof_cat_json.values()))

        if value_to_set:
            env.cr.execute("""
                UPDATE hr_employee
                SET l10n_pt_professional_category_tmp = %s
                WHERE id = %s
            """, (int(value_to_set), emp_id))

    _logger.info("Clearing 'l10n_pt_professional_category' field on hr.employee to avoid post-migration errors...")
    env.cr.execute("""
        UPDATE hr_employee SET l10n_pt_professional_category = NULL;
    """)
    _logger.info("'l10n_pt_professional_category' field cleared.")

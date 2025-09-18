import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Post-migration script to:
    1. Transfer data from the temporary column 'l10n_pt_professional_category_tmp'
       to the actual model field 'l10n_pt_professional_category'.
    2. Drop the temporary column.
    3. Delete obsolete entries from ir.property.
    """

    api.Environment(cr, SUPERUSER_ID, {})

    _logger.info("Migrating data from temporary column to real field...")

    # Update the real field 'l10n_pt_professional_category' with values from
    # the temporary column
    cr.execute(
        """
        UPDATE hr_employee
        SET l10n_pt_professional_category = l10n_pt_professional_category_tmp
        WHERE l10n_pt_professional_category_tmp IS NOT NULL
    """
    )
    _logger.info("Migration of values done.")

    # Drop the temporary column
    try:
        cr.execute(
            """
            ALTER TABLE hr_employee
            DROP COLUMN l10n_pt_professional_category_tmp;
        """
        )
        _logger.info("Temporary column dropped.")
    except Exception as e:
        _logger.warning(
            f"Could not drop 'l10n_pt_professional_category_tmp' column. "
            f"It may not exist or another error occurred: {e}"
        )

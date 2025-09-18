import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """
    This pre-migration script is designed to transfer data from the company_dependent field
    l10n_pt_professional_category, stored in the ir.property model, into a temporary
    column in the hr_employee table. It creates a new integer column named
    l10n_pt_professional_category_tmp, identifies the relevant property records, selects
    the most appropriate value per employee (based on the lowest ID), and populates the
    temporary column accordingly.
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

    # Search for properties related to the professional category
    properties = env["ir.property"].search(
        [("name", "=", "l10n_pt_professional_category")]
    )

    # Group properties by employee, keeping the one with the smallest ID
    grouped_properties = {}
    for prop in properties:
        if (
            prop.res_id not in grouped_properties
            or prop.id < grouped_properties[prop.res_id]
        ):
            grouped_properties[prop.res_id] = prop.id

    # Apply the property value to the new temporary column
    for _res_id_str, prop_id in grouped_properties.items():
        prop = env["ir.property"].browse(prop_id)
        _, category_id = prop.value_reference.split(",")
        model, record_id = prop.res_id.split(",")

        employee_id = int(record_id)
        env.cr.execute(
            """
            UPDATE hr_employee
            SET l10n_pt_professional_category_tmp = %s
            WHERE id = %s
        """,
            (int(category_id), employee_id),
        )

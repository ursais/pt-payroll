from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Note: This migration script is developed to update the values of the 'contract_modality'
    # field from the contract to the employee.
    employees = env["hr.employee"].search([])

    for employee in employees:
        if employee.contract_id.l10n_pt_contract_modality:
            employee.update(
                {
                    "l10n_pt_contract_modality": employee.contract_id.l10n_pt_contract_modality,
                }
            )

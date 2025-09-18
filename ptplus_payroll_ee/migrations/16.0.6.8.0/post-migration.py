from openupgradelib import openupgrade

RULES_CODES = {
    "BASIC": "Vencimento Base",
    "GROSS": "Total de Abonos",
    "NET": "Total a Receber",
}

NET_PYTHON_CODE = """result = categories.T_ABONOS + categories.T_DES - \
result_rules['SUBS_REF_TIC']['total'] - result_rules['T_RECEBER_ESP']['total']"""


@openupgrade.migrate()
def migrate(env, version):
    # Note: This migration script is designed to update the 'registration_number'
    # field with the ID of each employee and to update the name rules.
    # Note: This migration file was developed only for Enterprise Edition
    employees = (
        env["hr.employee"]
        .search([])
        .filtered(lambda r: r.company_id.country_id == env.ref("base.pt"))
    )

    for employee in employees:
        registration_numbers = (
            env["hr.employee"].search([("company_id", "=", employee.company_id.id)])
        ).mapped("registration_number")

        slips = env["hr.payslip"].search([("employee_id", "=", employee.id)])

        if (
            not employee.registration_number
            and (str(employee.id) not in registration_numbers)
            and slips
        ):
            employee.update(
                {
                    "registration_number": employee.id,
                }
            )

    ###############
    rules = (
        env["hr.salary.rule"]
        .search([])
        .filtered(
            lambda r: r.struct_id.country_id == env.ref("base.pt")
            and r.code in RULES_CODES
        )
    )

    for rule in rules:
        if rule.code in RULES_CODES.values():
            rule.update(
                {
                    "name": RULES_CODES[rule.code],
                }
            )
        if rule.code == "NET":
            rule.update(
                {
                    "amount_python_compute": NET_PYTHON_CODE,
                }
            )

    # This code fix a migration error
    employees = env["hr.employee"].search([])

    for employee in employees:
        if (
            employee.contract_id.l10n_pt_contract_modality
            and not employee.l10n_pt_contract_modality
        ):
            employee.update(
                {
                    "l10n_pt_contract_modality": employee.contract_id.l10n_pt_contract_modality,
                }
            )

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Retrieve all tax office records
    tax_offices = env["hr.tax.office.pt"].search([])

    # Create a dictionary to store the latest record for each tax office code
    tax_office_map = {}
    for office in tax_offices:
        if office.code:
            # If the code is not in the dictionary or if the current ID is greater,
            # update the mapping
            if (
                office.code not in tax_office_map
                or office.id > tax_office_map[office.code].id
            ):
                tax_office_map[office.code] = office

    # Update employees to reference the correct tax office
    employees = env["hr.employee"].search([])
    for employee in employees:
        if employee.l10n_pt_tax_office_id:
            correct_office = tax_office_map.get(employee.l10n_pt_tax_office_id.code)
            if (
                correct_office
                and correct_office.id != employee.l10n_pt_tax_office_id.id
            ):
                employee.l10n_pt_tax_office_id = correct_office

    # Update partners to reference the correct tax office
    partners = env["res.partner"].search([])
    for partner in partners:
        if partner.l10n_pt_tax_office_id:
            correct_office = tax_office_map.get(partner.l10n_pt_tax_office_id.code)
            if correct_office and correct_office.id != partner.l10n_pt_tax_office_id.id:
                partner.l10n_pt_tax_office_id = correct_office

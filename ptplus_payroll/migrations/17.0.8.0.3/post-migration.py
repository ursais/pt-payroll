from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute("SELECT employee_id, value FROM temp_table_mig")
    temp_table_mig_values = env.cr.fetchall()

    employees = env["hr.employee"].search([])
    temp_table_dict = {
        employee_id: value for employee_id, value in temp_table_mig_values
    }

    for employee in employees:
        employee_value = temp_table_dict.get(employee.id)
        if employee_value:
            if employee_value == "1_year":
                employee.l10n_pt_special_fiscal_regime_id = env.ref(
                    "ptplus_payroll.1_year_youth_irs"
                )
            elif employee_value == "2_year":
                employee.l10n_pt_special_fiscal_regime_id = env.ref(
                    "ptplus_payroll.2_year_youth_irs"
                )
            elif employee_value == "3_year":
                employee.l10n_pt_special_fiscal_regime_id = env.ref(
                    "ptplus_payroll.3_year_youth_irs"
                )
            elif employee_value == "4_year":
                employee.l10n_pt_special_fiscal_regime_id = env.ref(
                    "ptplus_payroll.4_year_youth_irs"
                )
            elif employee_value == "5_year":
                employee.l10n_pt_special_fiscal_regime_id = env.ref(
                    "ptplus_payroll.5_year_youth_irs"
                )

    env.cr.execute("DROP TABLE IF EXISTS temp_table_mig")

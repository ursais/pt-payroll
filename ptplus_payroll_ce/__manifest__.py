##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
{
    "name": "Portugal - Payroll Community Edition",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://github.com/exosoftware/portugal-payroll",
    "category": "Localization",
    "version": "16.0.6.1.0",
    "depends": [
        "ptplus_payroll",
        "payroll_account",
        "payroll_rule_time_parameter",
    ],
    "excludes": [
        "ptplus_payroll_ee",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "data/hr_rule_parameters_data.xml",
        "data/ptplus_payroll_data.xml",
        "data/ptplus_payroll_rules.xml",
        "data/hr_holidays_data.xml",
        "security/ir.model.access.csv",
        "security/ptplus_payroll_ce_security.xml",
        "views/hr_payroll_structure_views.xml",
        "views/hr_payslip_input_template_views.xml",
        "views/res_config_settings_views.xml",
        "views/hr_salary_rule_views.xml",
        "views/hr_payslip_views.xml",
        "views/hr_salary_complement_pt_views.xml",
        "views/menus.xml",
        "views/hr_payroll_report.xml",
        "views/email_template.xml",
        "views/employee_multiple_send_payslip.xml",
        "wizards/payroll_statement.xml",
    ],
    "demo": [],
    "post_init_hook": "post_init_hook",
    "installable": True,
}

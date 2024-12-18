##############################################################################
{
    "name": "Portugal - Payroll Enterprise Edition",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://exosoftware.pt",
    "category": "Localization",
    "version": "15.0.8.0.3",
    "depends": [
        "ptplus_payroll",
        "hr_payroll_account",
        "hr_payroll_account_sepa",
        "hr_payroll_expense",
        "ptplus_expense",
    ],
    "excludes": [
        "ptplus_payroll_ce",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "data/hr_work_entry_data.xml",
        "data/ptplus_payroll_data.xml",
        "data/hr_holidays_data.xml",
        "data/ptplus_payroll_rules.xml",
        "data/hr_rule_parameters_data.xml",
        "security/ir.model.access.csv",
        "security/ptplus_payroll_ee_security.xml",
        "views/hr_payroll_structure_views.xml",
        "views/hr_salary_complement_pt_views.xml",
        "views/menus.xml",
        "views/res_config_settings_views.xml",
        "views/hr_salary_rule_views.xml",
        "views/hr_payslip_views.xml",
        "views/hr_payroll_report.xml",
        "views/hr_expense_views.xml",
        "views/hr_contract_views.xml",
        "views/email_template.xml",
        "views/employee_multiple_send_payslip.xml",
        "wizards/payroll_statement.xml",
        "wizards/hr_payroll_edit_payslip_lines_wizard_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'ptplus_payroll_ee/static/src/**/*.js',
        ],
    },
    "demo": [],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "auto_install": True,
}
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################

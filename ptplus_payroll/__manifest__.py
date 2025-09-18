##############################################################################
#
#    Copyright (C) 2016 Exo Software, Lda. (<https://exosoftware.pt>)
#
##############################################################################
# pylint: disable=license-allowed, manifest-required-author

{
    "name": "Portugal - Payroll",
    "license": "OPL-1",
    "author": "Exo Software",
    "website": "https://github.com/exosoftware/portugal-payroll",
    "category": "Localization",
    "version": "18.0.8.2.1",
    "depends": ["hr_contract", "ptplus", "hr_holidays", "ptplus_partner"],
    "data": [
        "data/hr_marital_status_pt.xml",
        "data/hr.income.tax.pt.csv",
        "data/hr_insurance_company_pt.xml",
        "data/hr.profession.pt.csv",
        "data/hr.qualification.pt.csv",
        "data/hr.social.security.tax.pt.csv",
        "data/hr_special_fiscal_regime_pt.xml",
        "security/ir.model.access.csv",
        "views/dataport_log_views.xml",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_income_tax_pt_views.xml",
        "views/hr_insurance_company_pt_views.xml",
        "views/hr_profession_pt_views.xml",
        "views/hr_qualification_pt_views.xml",
        "views/hr_social_security_tax_pt_views.xml",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "views/hr_professional_category_pt_views.xml",
        "views/res_users_views.xml",
        "views/hr_tax_office_pt_views.xml",
        "report/hr_payroll_report.xml",
        "report/report_payslip_templates.xml",
        "report/annual_income_stmt_report.xml",
        "report/payroll_dri_statement_report.xml",
        "wizards/payroll_statement.xml",
        "wizards/single_report_statement_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ptplus_payroll/static/src/scss/single_report.scss",
        ]
    },
    "demo": [],
    "installable": True,
    "external_dependencies": {"python": ["unidecode"]},
}

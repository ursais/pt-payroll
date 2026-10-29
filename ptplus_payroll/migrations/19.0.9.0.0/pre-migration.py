import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


_WIZARD_FORM_XMLID = "wizard_payroll_statement_form"
_EMPLOYEE_FORM_XMLID = "view_employee_form_pt"
_EMPLOYEE_FORM_RENAMED = "view_employee_form_pt_payroll"


def _drop_redundant_wizard_view(env):
    """Remove the _ee primary wizard view that collides with the base view.

    Both ``ptplus_payroll.wizard_payroll_statement_form`` and
    ``ptplus_payroll_ee.wizard_payroll_statement_form`` exist on installs that
    have both modules. The _ee version is an empty primary view; we drop it
    and redirect any references to the base view before the module rename.
    """
    imd = env["ir.model.data"]
    base = imd.search(
        [("module", "=", "ptplus_payroll"), ("name", "=", _WIZARD_FORM_XMLID)],
        limit=1,
    )
    ee = imd.search(
        [("module", "=", "ptplus_payroll_ee"), ("name", "=", _WIZARD_FORM_XMLID)],
        limit=1,
    )
    if not ee:
        return
    if not base:
        ee.write({"module": "ptplus_payroll"})
        return

    env.cr.execute(
        "UPDATE ir_act_window SET view_id = %s WHERE view_id = %s",
        (base.res_id, ee.res_id),
    )
    env.cr.execute(
        "UPDATE ir_act_window_view SET view_id = %s WHERE view_id = %s",
        (base.res_id, ee.res_id),
    )
    env.cr.execute(
        "UPDATE ir_ui_view SET inherit_id = %s WHERE inherit_id = %s",
        (base.res_id, ee.res_id),
    )
    env.cr.execute("DELETE FROM ir_ui_view WHERE id = %s", (ee.res_id,))
    ee.unlink()


def _drop_stale_views(env):
    """Drop stale views referencing fields renamed in 19.0 before data load.

    ``relatorio_unico_statement_form`` inherits ``wizard_payroll_statement_form``
    and its pre-19.0 arch references ``contract_id`` on
    ``ru.extra.data.employee``, a field renamed to ``version_id`` in 19.0.
    When ``wizards/payroll_statement.xml`` rewrites the parent view, Odoo
    validates the combined arch and the still-stale child makes the module
    update abort with a ParseError. The module recreates the view later in the
    same load (``wizards/single_report_statement_views.xml``), so it is safe to
    delete the view and its xmlid here.

    ``report_slip_pt`` was the payslip report template in 18.0; it was renamed
    to ``report_payslip_pt`` in 19.0, so its stale arch (``contract_id`` on
    ``hr.payslip``) is never overwritten. Drop it as well.
    """
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "ptplus_payroll.relatorio_unico_statement_form",
            "ptplus_payroll.report_slip_pt",
        ],
        delete_childs=True,
    )


def _rename_employee_form(env):
    """Rename the _ee employee form view xmlid to avoid collision.

    Both modules legitimately define an ``hr.employee`` form view with id
    ``view_employee_form_pt`` but they inherit from different parents:
    the base inherits from ``hr.view_employee_form`` (personal data) while
    the _ee one inherits from ``hr_payroll.payroll_hr_employee_view_form``
    (payroll data). Keep both — rename the _ee record so they can co-exist
    in the unified module.
    """
    imd = env["ir.model.data"]
    ee = imd.search(
        [("module", "=", "ptplus_payroll_ee"), ("name", "=", _EMPLOYEE_FORM_XMLID)],
        limit=1,
    )
    if ee:
        ee.write({"name": _EMPLOYEE_FORM_RENAMED})


@openupgrade.migrate()
def migrate(env, version):
    _drop_stale_views(env)

    if not openupgrade.is_module_installed(env.cr, "ptplus_payroll_ee"):
        _logger.info("ptplus_payroll_ee is not installed; skipping merge migration.")
        return

    _logger.info(
        "Merging ptplus_payroll_ee into ptplus_payroll: "
        "redirecting ir_model_data and uninstalling the legacy module."
    )

    _drop_redundant_wizard_view(env)
    _rename_employee_form(env)

    openupgrade.update_module_names(
        env.cr,
        [("ptplus_payroll_ee", "ptplus_payroll")],
        merge_modules=True,
    )

    env.cr.execute(
        """
        UPDATE ir_module_module
        SET state = 'uninstalled', latest_version = NULL
        WHERE name = 'ptplus_payroll_ee'
        """
    )

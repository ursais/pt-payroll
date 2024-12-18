/** @odoo-module **/

import { registry } from "@web/core/registry";
import { X2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ListRenderer } from "@web/views/list/list_renderer";
import { Field } from "@web/views/fields/field";

export class L10nPtWorkedDaysField extends Field {
    get fieldComponentProps() {
        const props = super.fieldComponentProps;
        const record = this.props.record;
        const oldUpdate = props.update;
        props.update = async (value) => {
            if ((this.props.name === 'l10n_pt_leave_amount_curr_period' || this.props.name === 'l10n_pt_leave_amount_prev_period' || this.props.name === 'amount') && record.data.amount !== value) {
                await record.update({ [this.props.name]: value });
                await record.save( { stayInEdition: true, noReload: true });
                // getting the wizard id. when js team gets rid of the basic relational model, we'll clean this
                const wizardId = record.model.__bm_load_params__.res_id;
                if (wizardId) {
                    const action = await this.env.services.orm.call(
                        "hr.payroll.edit.payslip.lines.wizard",
                        "recompute_worked_days_lines",
                        [wizardId]
                    );
                    await this.env.services.action.doAction(action);
                }
            } else {
                await oldUpdate(value);
            }
        }
        return props;
    }
}

export class L10nPtWorkedDaysRenderer extends ListRenderer {}
L10nPtWorkedDaysRenderer.components = {
    ...ListRenderer.components,
    Field: L10nPtWorkedDaysField,
}

export class L10nPtWorkedDaysLineOne2Many extends X2ManyField {
    async onAdd ({ context, editable }) {
        const wizardId = this.props.record.resId;
        return super.onAdd({
            context: {
                ...context,
                default_edit_payslip_lines_wizard_id: wizardId,
            },
            editable
        });
    }
}
L10nPtWorkedDaysLineOne2Many.components = {
    ...X2ManyField.components,
    ListRenderer: L10nPtWorkedDaysRenderer
};


registry.category('fields').add('l10n_pt_worked_days_line_one2many', L10nPtWorkedDaysLineOne2Many);


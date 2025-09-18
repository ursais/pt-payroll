/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Field} from "@web/views/fields/field";
import {X2ManyField, x2ManyField} from "@web/views/fields/x2many/x2many_field";
import {ListRenderer} from "@web/views/list/list_renderer";
import {useEnv} from "@odoo/owl";

export class L10nPtWorkedDaysField extends Field {
    setup() {
        super.setup(...arguments);
        this.actionService = useService("action");
        this.orm = useEnv().services.orm;
    }

    get fieldComponentProps() {
        const props = super.fieldComponentProps;
        const record = this.props.record;
        if (!record.isWorkedDaysField) {
            record.isWorkedDaysField = true;
            const oldUpdate = record.update.bind(record);
            record.update = async (changes) => {
                if (
                    "l10n_pt_leave_amount_curr_period" in changes ||
                    "l10n_pt_leave_amount_prev_period" in changes ||
                    "amount" in changes
                ) {
                    await oldUpdate(changes);
                    // save x2many from its parent for the relation to work
                    await record._parentRecord.save();
                    const wizardId = record.model.config.resId;
                    if (wizardId) {
                        const action = await this.orm.call(
                            "hr.payroll.edit.payslip.lines.wizard",
                            "recompute_worked_days_lines",
                            [wizardId]
                        );
                        if (action) {
                            await this.actionService.doAction(action);
                        }
                    }
                } else {
                    await oldUpdate(changes);
                }
            };
        }
        return props;
    }
}

export class L10nPtWorkedDaysRenderer extends ListRenderer {}
L10nPtWorkedDaysRenderer.components = {
    ...ListRenderer.components,
    Field: L10nPtWorkedDaysField,
};

export class L10nPtWorkedDaysLineOne2Many extends X2ManyField {
    async onAdd({context, editable}) {
        const wizardId = this.props.record.resId;
        return super.onAdd({
            context: {
                ...context,
                default_edit_payslip_lines_wizard_id: wizardId,
            },
            editable,
        });
    }
}
L10nPtWorkedDaysLineOne2Many.components = {
    ...X2ManyField.components,
    ListRenderer: L10nPtWorkedDaysRenderer,
};

export const l10nPtWorkedDaysLineOne2Many = {
    ...x2ManyField,
    component: L10nPtWorkedDaysLineOne2Many,
};

registry
    .category("fields")
    .add("l10n_pt_worked_days_line_one2many", l10nPtWorkedDaysLineOne2Many);

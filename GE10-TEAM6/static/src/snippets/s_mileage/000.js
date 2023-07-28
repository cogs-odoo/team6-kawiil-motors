odoo.define('GE10-TEAM6.s_mileage', function (require) {
'use strict';

const core = require('web.core');
const publicWidget = require('web.public.widget');
const weUtils = require('web_editor.utils');

const _t = core._t;

const MileageWidget = publicWidget.Widget.extend({
    selector: '.s_mileage',
    disabledInEditableMode: false,

    /**
     * @override
     */
    start: function () {
        this.$wrapper = this.$('.s_mileage_canvas_wrapper');
        this.$wrapper.addClass('d-flex justify-content-center');
        this.size = parseInt(this.el.dataset.size);
        this.display = this.el.dataset.display;

        this._render();
        return this._super(...arguments);
    },
    /**
     * @override
     */
    destroy: function () {
        this.$('.s_mileage_canvas_wrapper').removeClass('d-none');

        clearInterval(this.setInterval);
        this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Draws the whole countdown, including one countdown for each time unit.
     *
     * @private
     */
    _render: function () {
        this.$('.s_mileage_canvas_wrapper').addClass('d-none');
    },
});

publicWidget.registry.mileage = MileageWidget;

return MileageWidget;
});

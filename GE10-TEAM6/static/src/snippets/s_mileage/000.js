odoo.define('GE10-TEAM6.s_mileage', function (require) {
'use strict';

const ajax = require('web.ajax');
const publicWidget = require('web.public.widget');

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
        this.width = parseInt(this.size);
        this.display = this.el.dataset.display;
        this.textColor = this.el.dataset.textColor;

        this._render();
        return this._super(...arguments);
    },
    /**
     * @override
     */
    destroy: function () {
        this.$('.s_mileage_canvas_wrapper').removeClass('d-none');
        this.$('.s_mileage_canvas_flex').remove();

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
        var self = this;

        ajax.jsonRpc('/mileage', 'call').then(function (data) {
            var mileage = data;
            var unit = "mi";

            const canvas = $('<div class="s_mileage_canvas_flex"><canvas class="w-100"></canvas></div>').appendTo(self.$wrapper)[0].querySelector('canvas');

            const ctx = canvas.getContext("2d");
            const nbSize = self.size / 4;
            const unitSize = self.size / 12;
        
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            // Value
            ctx.font = `${nbSize}px Arial`;
            ctx.fillStyle = self.textColor;
            ctx.fillText(mileage, canvas.width / 2, canvas.height / 2);

            // Units
            ctx.font = `${unitSize}px Arial`;
            ctx.fillText(unit, canvas.width / 2, canvas.height / 2 + nbSize / 1.5, self.width);
    
            ctx.fillStyle = "rgb(13, 255, 0)";
            ctx.fillRect(10, 10, 50, 50);
    
            ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
            ctx.fillRect(30, 30, 50, 50);
        });
    },
    /**
     * Erases the canvas.
     *
     * @private
     * @param {RenderingContext} ctx - Context of the canvas
     */
    _clearCanvas: function (ctx) {
        ctx.clearRect(0, 0, this.size, this.size);
    },
});

publicWidget.registry.mileage = MileageWidget;

return MileageWidget;
});

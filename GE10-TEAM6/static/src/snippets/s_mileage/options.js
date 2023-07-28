odoo.define('GE10-TEAM6.s_mileage_options', function (require) {
'use strict';

const core = require('web.core');
const options = require('web_editor.snippets.options');

const qweb = core.qweb;

options.registry.mileage = options.Class.extend({
    events: _.extend({}, options.Class.prototype.events || {}, {
        'click .toggle-edit-message': '_onToggleEndMessageClick',
    }),
});
});

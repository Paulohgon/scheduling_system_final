// Copyright (c) 2024, Paulo Henrique and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Appointment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Appointment', {
    refresh: function(frm) {
        frm.add_custom_button(__('Calendar View'), function() {
            frappe.set_route('List', 'Appointment', 'Calendar');
        });
    }
});


# Copyright (c) 2024, Paulo Henrique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import timedelta

class Appointment(Document):
          
    def validate(self):
        self.set_end_date()
        self.validate_seller_availability()

    def validate_seller_availability(self):

        overlapping_appointments = frappe.db.sql("""
            SELECT
                name
            FROM
                `tabAppointment`
            WHERE
                seller = %s
                AND name != %s
                AND (
                    (start_date <= %s AND end_date >= %s)
                    OR (start_date <= %s AND end_date >= %s)
                    OR (start_date >= %s AND end_date <= %s)
                )
        """, (self.seller, self.name, self.start_date, self.start_date, self.end_date, self.end_date, self.start_date, self.end_date))


        if overlapping_appointments:
            frappe.throw(("Seller is already booked for another appointment during this time period."))
	

    def set_end_date(self):
        if self.start_date and self.duration:
            start_datetime = frappe.utils.get_datetime(self.start_date)
            duration_parts = self.duration.split(':')
            duration_hours = int(duration_parts[0])
            duration_minutes = int(duration_parts[1])
            end_datetime = start_datetime + timedelta(hours=duration_hours, minutes=duration_minutes)
            self.end_date = end_datetime
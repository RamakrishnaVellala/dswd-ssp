import json
import logging
from datetime import datetime

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request


class DswdSelfServicePortal(http.Controller):
    @http.route(["/selfservice/home"], type="http", auth="user", website=True)
    def self_service_home(self, **kwargs):
        self.self_service_check_roles("REGISTRANT")
        query = request.params.get("query")
        domain = [("name", "ilike", query)]
        programs = request.env["g2p.program"].sudo().search(domain).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled", "not_eligible": "Not Eligible"}
        amount_received = 0
        myprograms = []
        for program in programs:
            membership = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            amount_issued = sum(
                ent.amount_issued
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            amount_received = sum(
                ent.amount_paid
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            if len(membership) > 0:
                myprograms.append(
                    {
                        "id": program.id,
                        "name": program.name,
                        "has_applied": len(membership) > 0,
                        "status": states.get(membership.state, "Error"),
                        "issued": "{:,.2f}".format(amount_issued),
                        "paid": "{:,.2f}".format(amount_received),
                        "enrollment_date": membership.enrollment_date.strftime(
                            "%d-%b-%Y"
                        )
                        if membership.enrollment_date
                        else None,
                        "is_latest": (datetime.today() - program.create_date).days < 21,
                        "application_id": membership.application_id
                        if membership.application_id
                        else None,
                    }
                )

        entitlement = sum(
            ent.amount_issued
            for ent in request.env["g2p.payment"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)])
        )
        received = sum(
            ent.amount_paid
            for ent in request.env["g2p.payment"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner_id.id),
                ]
            )
        )
        pending = entitlement - received
        labels = ["Received", "Pending"]
        values = [received, pending]
        data = json.dumps({"labels": labels, "values": values})

        return request.render(
            "g2p_self_service_portal.dashboard",
            {"programs": myprograms, "data": data},
        )
    
    def self_service_check_roles(self, role_to_check):
        # And add further role checks and return types
        if role_to_check == "REGISTRANT":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            if not request.env.user.partner_id.is_registrant:
                raise Forbidden(_("User is not allowed to access the portal"))
        pass
    def jsonize_form_data(self, data, program, membership=None):
        for key in data:
            value = data[key]
            if isinstance(value, FileStorage):
                if not program.supporting_documents_store:
                    _logger.error(
                        "Supporting Documents Store is not set in Program Configuration"
                    )
                    data[key] = None
                    continue

                data[key] = self.add_file_to_store(
                    value,
                    program.supporting_documents_store,
                    program_membership=membership,
                )
                if not data.get(key, None):
                    _logger.warning("Empty/No File received for field %s", key)
                    continue

        return data

    @classmethod
    def add_file_to_store(cls, file: FileStorage, store, program_membership=None):
        if store and file.filename:
            if len(file.filename.split(".")) > 1:
                supporting_document_ext = "." + file.filename.split(".")[-1]
            else:
                supporting_document_ext = None
            document_file = store.add_file(
                file.stream.read(),
                extension=supporting_document_ext,
                program_membership=program_membership,
            )
            document_uuid = document_file.name.split(".")[0]
            return {
                "document_id": document_file.id,
                "document_uuid": document_uuid,
                "document_name": document_file.name,
                "document_slug": document_file.slug,
                "document_url": document_file.url,
            }
        return None
    @http.route(
        ["/selfservice/apply/<int:_id>"], type="http", auth="user", website=True
    )
    def self_service_apply_programs(self, _id):
        self.self_service_check_roles("REGISTRANT")

        relations=self.get_relationships()
        print(relations)
        family_details=self.get_family_details()
        print(family_details)
        program = request.env["g2p.program"].sudo().browse(_id)
        multiple_form_submission = program.multiple_form_submission
        current_partner = request.env.user.partner_id

        for mem in current_partner.program_membership_ids:
            if mem.program_id.id == _id and not multiple_form_submission:
                return request.redirect(f"/selfservice/submitted/{_id}")

        view = program.self_service_portal_form.view_id

        # return request.render(
        #     view.id,
        #     {
        #         "program": program.name,
        #         "program_id": program.id,
        #         "user": request.env.user.given_name,
        #     },
        # )
        return request.render("dswd_self_service_portal.beneficiary_details_capturing_program_form",{
                "program": program.name,
                "program_id": program.id,
                "user": request.env.user.given_name,
                "relations" : relations  ,
                "family_details":family_details
        })

    @http.route(
        ["/selfservice/submitted/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def self_service_form_details(self, _id, **kwargs):
        self.self_service_check_roles("REGISTRANT")
        program = request.env["g2p.program"].sudo().browse(_id)
        current_partner = request.env.user.partner_id
        program_member = None
        prog_membs = (
            request.env["g2p.program_membership"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", current_partner.id),
                    ("program_id", "=", program.id),
                ]
            )
        )
        if len(prog_membs) > 0:
            program_member = prog_membs[0]
        if request.httprequest.method == "POST":
            if len(prog_membs) == 0:
                program_member = (
                    request.env["g2p.program_membership"]
                    .sudo()
                    .create(
                        {
                            "partner_id": current_partner.id,
                            "program_id": program.id,
                        }
                    )
                )
            form_data = kwargs
            print(kwargs)
            # Hardcoding Account number from form data for now
            account_num = form_data.get("Account Number", None)
            if account_num:
                if len(current_partner.bank_ids) > 0:
                    # TODO: Fixing value of first account number for now, if more than one exists
                    current_partner.bank_ids[0].acc_number = account_num
                else:
                    current_partner.bank_ids = [(0, 0, {"acc_number": account_num})]
            program_registrant_info_ids = (
                request.env["g2p.program.registrant_info"]
                .sudo()
                .search(
                    [
                        ("program_id", "=", program.id),
                        ("registrant_id", "=", current_partner.id),
                        ("status", "=", "awaiting_approval"),
                    ]
                )
            )
            program_registrant_info_ids.write({"status": "closed"})
            request.env["g2p.program.registrant_info"].sudo().create(
                {
                    "status": "applied",
                    "program_registrant_info": self.jsonize_form_data(
                        form_data, program, membership=program_member
                    ),
                    "program_id": program.id,
                    "registrant_id": current_partner.id,
                }
            )
        else:
            if not program_member:
                return request.redirect(f"/selfservice/apply/{_id}")
        return request.render(
            "dswd_self_service_portal.self_service_form_submitted",
            {
                "program": program.name,
                "submission_date": program_member.enrollment_date.strftime("%d-%b-%Y"),
                "application_id": program_member.application_id,
                "user": current_partner.given_name.capitalize(),
            },
        )
    def get_relationships(self):
        relationships = request.env["g2p.relationship"].sudo().search([])
        rel_list = []
        for rel in relationships:
            rel_list.append(rel.name)

        return (
            rel_list
        )
   
    def get_family_details(self):
        reg_rel = request.env["g2p.reg.rel"].sudo().search([("destination", "=", request.env.user.partner_id.id)])
        family_details = []
        for rel in reg_rel:
            family_details.append({
                "name": rel.source.name,
                "relation": rel.relation.name,
                "dob": rel.source.birthdate,
                "ocupation": rel.source.occupation,
                "income": rel.source.income
            })

        return (
            family_details
        )
#     @http.route('/dswd_self_service_portal/dswd_self_service_portal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dswd_self_service_portal/dswd_self_service_portal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dswd_self_service_portal.listing', {
#             'root': '/dswd_self_service_portal/dswd_self_service_portal',
#             'objects': http.request.env['dswd_self_service_portal.dswd_self_service_portal'].search([]),
#         })

#     @http.route('/dswd_self_service_portal/dswd_self_service_portal/objects/<model("dswd_self_service_portal.dswd_self_service_portal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dswd_self_service_portal.object', {
#             'object': obj
#         })

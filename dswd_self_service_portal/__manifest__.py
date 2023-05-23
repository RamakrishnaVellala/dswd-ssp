{
    "name": "DSWD Self Service Portal",
    "category": "G2P",
    "version": "15.0.1.1.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "Other OSI approved licence",
    "development_status": "Alpha",
    "depends": [
        "g2p_self_service_portal",
    ],
    "data": [
        "views/g2p_self_service_beneficiary_details_capturing_form_template.xml",
        "views/g2p_self_service_form_page_template.xml",
        "views/g2p_self_service_submitted_forms.xml"
    ],
    "assets": {
        "web.assets_backend": [],
        "web.assets_qweb": [
            #   "views/g2p_self_service_portal.doughnut_chart.xml",
        ],
        "web.assets_frontend": [
            "dswd_self_service_portal/static/src/js/self_service_beneficiaries_capturing_action.js"
            # # "g2p_self_service_portal/static/src/js/self_service_pie_chart.js",
            # "g2p_self_service_portal/static/src/js/self-service_search_sort.js",
            # "g2p_self_service_portal/static/src/js/self-service_search_sort_all.js",
            # "g2p_self_service_portal/static/src/js/self_service_welcome_alert.js"
        ],
        "web.assets_common": [],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}

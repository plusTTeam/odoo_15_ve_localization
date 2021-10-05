# Constants used in the module

ACCOUNT_MODEL = "account.account"
RESOURCE_CALENDAR_LEAVES_MODEL = "resource.calendar.leaves"
RES_LANG_MODEL = "res.lang"
RES_PARTNER_MODEL = "res.partner"
RESOURCE_CALENDAR_ATTENDANCE_MODEL = "resource.calendar.attendance"
IR_MODEL_DATA = "ir.model.data"
REF_MAIN_COMPANY = "base.main_company"
MESSAGE_EXCEPTION_NOT_EXECUTE = "The exception was not executed correctly"
MESSAGE_DAY_NOT_FOUND = "Day not found"
MESSAGE_DOCUMENT_WRONG = "Field type document is wrong"
DOMAIN_COMPANY = "[('company_id', '=', company_id)]"
GLOBAL_TIME_OFF = [
    {
        "name": "Navidad",
        "month": "12",
        "day": "24"
    }, {
        "name": "Navidad",
        "month": "12",
        "day": "25"
    }, {
        "name": "Año Nuevo",
        "month": "12",
        "day": "31"
    }, {
        "name": "Año Nuevo",
        "month": "01",
        "day": "01"
    }, {
        "name": "Día del trabajador",
        "month": "05",
        "day": "01"
    }, {
        "name": "Declaración de Independencia",
        "month": "04",
        "day": "19"
    }, {
        "name": "Batalla de Carabobo",
        "month": "06",
        "day": "24"
    }, {
        "name": "Día de la Independencia",
        "month": "07",
        "day": "05"
    }, {
        "name": "Natalicio de Simón Bolívar",
        "month": "07",
        "day": "24"
    }, {
        "name": "Día de la Resistencia Indígena",
        "month": "10",
        "day": "12"
    }
]
WEEK_DAYS = {
    "monday": {
        "morning": {
            "name_spanish": "Lunes por la mañana",
            "name_english": "Monday Morning"
        },
        "afternoon": {
            "name_spanish": "Lunes por la tarde",
            "name_english": "Monday Afternoon"
        }
    },
    "tuesday": {
        "morning": {
            "name_spanish": "Martes por la mañana",
            "name_english": "Tuesday Morning"
        },
        "afternoon": {
            "name_spanish": "Martes por la tarde",
            "name_english": "Tuesday Afternoon"
        }
    },
    "wednesday": {
        "morning": {
            "name_spanish": "Miércoles por la mañana",
            "name_english": "Wednesday Morning"
        },
        "afternoon": {
            "name_spanish": "Miércoles por la tarde",
            "name_english": "Wednesday Afternoon"
        }
    },
    "thursday": {
        "morning": {
            "name_spanish": "Jueves por la mañana",
            "name_english": "Thursday Morning"
        },
        "afternoon": {
            "name_spanish": "Jueves por la tarde",
            "name_english": "Thursday Afternoon"
        }
    },
    "friday": {
        "morning": {
            "name_spanish": "Viernes por la mañana",
            "name_english": "Friday Morning"
        },
        "afternoon": {
            "name_spanish": "Viernes por la tarde",
            "name_english": "Friday Afternoon"
        }
    }
}
RETENTION_TYPE_IVA = "iva"
RETENTION_TYPE_ISLR = "islr"
NAME_PRODUCT = "Product that cost %s"

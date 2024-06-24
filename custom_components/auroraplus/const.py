import datetime

DOMAIN = "auroraplus"

CONF_SERVICE_AGREEMENT_ID = "service_agreement_id"
CONF_ROUNDING = "rounding"

SENSOR_ESTIMATEDBALANCE = 'Estimated Balance'
SENSOR_DOLLARVALUEUSAGE = 'Dollar Value Usage'
SENSOR_KILOWATTHOURUSAGE = 'Kilowatt Hour Usage'
SENSOR_KILOWATTHOURUSAGETARIFF = 'Kilowatt Hour Usage Tariff'
SENSOR_DOLLARVALUEUSAGETARIFF = 'Dollar Value Usage Tariff'

SENSORS_MONETARY = [
    SENSOR_ESTIMATEDBALANCE,
    SENSOR_DOLLARVALUEUSAGE,
]


POSSIBLE_MONITORED = SENSORS_MONETARY + [SENSOR_KILOWATTHOURUSAGE]

DEFAULT_MONITORED = POSSIBLE_MONITORED

DEFAULT_ROUNDING = 2
DEFAULT_SCAN_INTERVAL = datetime.timedelta(hours=1)


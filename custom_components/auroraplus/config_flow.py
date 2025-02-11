import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import ConfigEntryAuthFailed

from sqlalchemy.exc import SQLAlchemyError

import voluptuous as vol

from .api import aurora_init
from .const import (
    CONF_ROUNDING,
    CONF_SERVICE_AGREEMENT_ID,
    DEFAULT_MONITORED,
    DEFAULT_ROUNDING,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    POSSIBLE_MONITORED,
)

_LOGGER = logging.getLogger(__name__)

# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
    }
)

class AuroraPlusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """AuroraPlus config flow."""
    VERSION = 0
    MINOR_VERSION = 1
    reauth_entry = None

    async def async_step_user(self,
                              user_input: dict[str, Any] | None = None
                              ):
        _LOGGER.debug(dir(self))
        return await self._configure(user_input)

    async def _configure(self,
                              user_input: dict[str, Any] | None = None
                              ):
        """
        Get access_token from the user, and create a new service.

        If self.reauth_entry is set, this entry will be updated instead.

        """
        errors = {}
        if user_input is not None:
            access_token = user_input.get(CONF_ACCESS_TOKEN)
            try:
                session = await self.hass.async_add_executor_job(
                    aurora_init,
                    access_token
                )
                address = session.month['ServiceAgreements'][session.serviceAgreementID]['PremiseName']
                await self.async_set_unique_id(session.serviceAgreementID)

                if self.reauth_entry:
                    self.hass.config_entries.async_update_entry(
                        self.reauth_entry,
                        data={
                            CONF_ACCESS_TOKEN: access_token,
                            CONF_SERVICE_AGREEMENT_ID: session.serviceAgreementID,
                        },
                    )
                    await self.hass.config_entries.async_reload(
                        self.reauth_entry.entry_id)
                    return self.async_abort(reason="reauth_successful")

                else:
                    return self.async_create_entry(
                        title=address,
                        data={
                            CONF_ACCESS_TOKEN: access_token,
                            CONF_SERVICE_AGREEMENT_ID: session.serviceAgreementID,
                        },
                    )

            except ConfigEntryAuthFailed as e:
                errors = {
                    'base': 'auth',
                }

        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(self, user_input=None):
        """Perform reauth upon an API authentication error."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=vol.Schema({}),
            )

        return await self.async_step_user()

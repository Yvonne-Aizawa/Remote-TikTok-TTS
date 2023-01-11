"""Support for the TikTok speech service."""
import logging
import requests
import asyncio
import aiohttp
import re
import async_timeout
import voluptuous as vol
import base64

import homeassistant.helpers.config_validation as cv
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from urllib.parse import quote
import json


_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["en_us_ghostface",
                     "en_male_grinch",
                     "en_male_wizard",
                     "en_female_ht_f08_halloween",
                     "en_female_madam_leota",
                     "en_male_ghosthost",
                     "en_male_pirate",
                     "en_female_ht_f08_glorious",
                     "en_male_sing_funny_it_goes_up",
                     "en_female_samc",
                     "en_male_cody",
                     "en_female_ht_f08_wonderful_world",
                     "en_male_m2_xhxs_m03_silly",
                     "en_male_funny",
                     "en_female_emotional",
                     "en_male_m03_sunshine_soon",
                     "en_female_f08_warmy_breeze",
                     "en_male_m03_lobby",
                     "en_female_f08_salut_damour" ,
                     "es_mx_002",
                     "en_male_narration",
                     "en_us_007",
                     "en_us_009",
                     "en_us_010",
                     "en_us_006",
                     "en_au_001",
                     "en_uk_001",
                     "en_us_002",
                     "en_au_002"]
DEFAULT_LANG = "en_us_007"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 59126

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up Tiktok speech component."""
    return TikTokTTS(hass, config[CONF_LANG], config[CONF_HOST], config[CONF_PORT])


class TikTokTTS(Provider):
    """The TikTok TTS API."""

    def __init__(self, hass, lang, host, port):
        """Initialize TikTok TTS provider."""
        self._hass = hass
        self._lang = lang
        self._host = host
        self._port = port
        self.name = "TikTokTTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message, voice, options=None):
        """Load TTS using the api that tiktok provides."""
        websession = async_get_clientsession(self._hass)

        try:
            with async_timeout.timeout(5):
                # set url
                url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
                # format message
                # message = quote(message)

                # set payload
                payload = {
                    "text": message,
                    "voice": 'en_us_001'
                }
                # send request
                request = await websession.post(url, json=payload)

                data = await request.json()  # this is a coroutine
                # extract mp3 data
                data = base64.b64decode(data['data'])

                if request.status != 200:
                    _LOGGER.error(
                        "Error %d on load url %s", request.status, request.url
                    )
                    return (None, None)
                # data = await request.read()

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for Tiktok's API")
            return (None, None)

        if data:
            # return the data as an mp3 file
            return ("mp3", data)
        return (None, None)

# Home Assistant Component for a remote picoTTS installation.

[![hacs_badge](https://img.shields.io/badge/HACS-default-orange.svg)](https://github.com/custom-components/hacs)

This is a component for Home Assistant which integrates Tiktok's TTS into home assistant.


# Installation

## HACS

Install it in the `Integrations` tab on the [Home Asssistant Community Store](https://github.com/custom-components/hacs).
You need to add this repo first though



# Configuration

Add following config to your yaml if you are using the Supervisor Addon

```yaml
tts:
  - platform: tiktok_tts

```


## Voice  
[voice list](https://github.com/oscie57/tiktok-voice/wiki/Voice-Codes) taken from here
example: `en_us_ghostface`, `en_au_001` in the language key

```yaml
tts:
  - platform: tiktok_tts
    language: "en_au_002"

```

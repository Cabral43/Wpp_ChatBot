from pydantic_settings import BaseSettings, SettingsConfigDict

class TwilioSettings(BaseSettings):
    account_sid:   str
    auth_token:    str
    phone_number:  str


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='twilio_'
    )

class AppSettings(BaseSettings):
    homolog_mode: bool = False
    reload:       bool = False
    host:         str  = '0.0.0.0'
    port:         int  = 8000
    database_url: str  = 'sqlite:///./wpp_chatbot.db'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

twilio_settings = TwilioSettings()
app_settings    = AppSettings()

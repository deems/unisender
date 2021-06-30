import logging
from typing import List, Any

import requests

from unisender.exceptions.unisender_exception import UnisenderException

logger = logging.getLogger('unisender')


class Unisender:
    _URL_API = 'https://api.unisender.com/ru/api/'
    _FORMAT = 'json'

    def __init__(self, api_key):
        self._api_key: str = api_key

    def import_contacts(self, field_names: List[str], data: List[List[Any]], overwrite_tags=0) -> dict:
        params = {
            'field_names': field_names,
            'data': data,
            'overwrite_tags': overwrite_tags
        }
        return self._request('importContacts', params)

    def send_email_by_unisender(self, email: str, sender_name: str, sender_email: str,
                                subject: str, body: str, list_id: int, lang: str = 'en'):
        """
        Отправка email через unisender.

        Документация: https://www.unisender.com/ru/support/api/messages/sendemail/
        """
        params = {
            'email': email,
            'sender_name': sender_name,
            'sender_email': sender_email,
            'subject': subject,
            'body': body,
            'list_id': list_id,
            'lang': lang,
            'error_checking': 1
        }
        response_data = self._request('sendEmail', params)

        send_results = response_data.get('result')
        if isinstance(send_results, list) is False:
            logger.error(f'unknown send error {response_data}')
            raise UnisenderException(response_data)
        for send_result in send_results:
            email_to = send_result['email']
            if send_result.get('errors'):
                logger.error(f'unknown send error: {send_result["errors"]} email: {email_to}')
            else:
                logger.info(f'email sent successfully: {email_to}. email ID: {send_result["id"]}')

    def _request(self, method: str, request_params: dict) -> dict:
        request_params['api_key'] = self._api_key
        request_params['format'] = self._FORMAT
        response = requests.post(f'{self._URL_API}{method}', data=self._http_build_query(request_params))
        if response.status_code != 200:
            logger.error(f'Unisender error {response.text}')
            raise UnisenderException(response.text)
        return response.json()

    def _http_build_query(self, params, key=None):
        """
        Re-implement http_build_query for systems that do not already have it
        """
        ret = {}

        for name, val in params.items():
            name = name

            if key is not None and not isinstance(key, int):
                name = '%s[%s]' % (key, name)
            if isinstance(val, dict):
                ret.update(self._http_build_query(val, name))
            elif isinstance(val, list):
                ret.update(self._http_build_query(dict(enumerate(val)), name))
            elif val is not None:
                ret[name] = val

        return ret

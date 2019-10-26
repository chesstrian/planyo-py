from hashlib import md5
from time import time

try:
    # noinspection PyProtectedMember
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests


class Planyo(object):
    """
    Planyo API low level client. Provides a straightforward mapping from
    Python to Planyo REST endpoint.

      >>> from planyo import Planyo
      >>> client = Planyo(api_key='ABC')
      >>> client.api_test()

    The instance has all methods in Planyo API Docs: https://api.planyo.com/api.php
    It is highly recommended to checks docs for params received by any method. Just pass a dictionary in `params` with
    all desired arguments.

      >>> client.api_test(params=dict(language='IT'))

    Hash key is also supported, in this case the instance needs to be initialized with the secret hash key from Planyo

      >>> client = Planyo(api_key='ABC', hash_key='DEF')
      >>> client.api_test()
    """

    endpoint = "https://api.planyo.com/rest/"
    methods = (
        # Check
        'api_test',

        # Reservations
        'add_reservation_payment',
        'can_make_reservation',
        'delete_custom_property',
        'delete_reservation',
        'do_reservation_action',
        'get_custom_property',
        'get_rental_price',
        'get_reservation_actions',
        'get_reservation_data',
        'get_reservation_payment_amount',
        'list_payments',
        'list_reservation_payments',
        'list_reservations',
        'make_reservation',
        'modify_reservation',
        'modify_reservation_payment',
        'recalculate_price',
        'remove_reservation_payment',
        'reservation_search',
        'search_reservations_by_form_item',
        'set_custom_properties',
        'set_custom_property',
        'set_reservation_color',
        'set_reservation_notes',
        'set_reservation_price',

        # Availability
        'add_recurring_vacation',
        'add_vacation',
        'can_make_reservation',
        'get_event_times',
        'get_ical_feed_url',
        'get_resource_usage',
        'get_resource_usage_for_month',
        'get_weekly_schedule',
        'is_resource_available',
        'list_vacations',
        'remove_vacation',
        'resource_search',
        'set_event_times',
        'set_resource_availability',
        'set_weekly_schedule',

        # Additional products
        'add_additional_product',
        'add_custom_product',
        'add_product_image',
        'get_reservation_products',
        'list_additional_products',
        'modify_additional_product',
        'remove_additional_product',
        'remove_custom_product',
        'remove_product_image',
        'set_product_usage_for_reservation',
        'set_reservation_products',

        # Resources
        'add_custom_property_definition',
        'add_resource',
        'add_resource_image',
        'delete_custom_property',
        'get_bundle_contents',
        'get_custom_property',
        'get_custom_property_definition',
        'get_event_times',
        'get_form_items',
        'get_ical_feed_url',
        'get_package_contents',
        'get_resource_info',
        'get_resource_pricing',
        'get_resource_seasons',
        'get_simplified_daily_pricing',
        'get_simplified_daily_restrictions',
        'list_resources',
        'modify_resource',
        'remove_custom_property_definition',
        'remove_resource',
        'remove_resource_image',
        'set_custom_properties',
        'set_custom_property',
        'set_event_times',
        'set_package_contents',
        'set_resource_admin',
        'set_resource_pricing',
        'set_unit_names',

        # Sites
        'add_custom_property_definition',
        'add_site',
        'add_site_image',
        'add_site_moderator',
        'add_url_to_admin_favorites',
        'delete_custom_property',
        'get_custom_property',
        'get_custom_property_definition',
        'get_form_items',
        'get_ical_feed_url',
        'get_site_info',
        'list_reviews',
        'list_sites',
        'modify_site',
        'remove_custom_property_definition',
        'remove_site_image',
        'remove_site_moderator',
        'remove_url_from_admin_favorites',
        'set_custom_properties',
        'set_custom_property',
        'set_payment_gateway',

        # Users
        'add_agent',
        'add_site_moderator',
        'add_user',
        'delete_custom_property',
        'get_custom_property',
        'get_user_data',
        'list_custom_user_properties',
        'list_users',
        'modify_user',
        'remove_site_moderator',
        'remove_user',
        'set_custom_properties',
        'set_custom_property',
        'set_resource_admin',

        # Shopping cart
        'create_cart',
        'delete_cart',
        'get_cart_items',
        'list_cart_payments',
        'list_carts',
        'move_reservations_to_cart',

        # Coupons and vouchers
        'apply_coupon',
        'apply_voucher',
        'create_voucher',
        'generate_coupon',
        'generate_coupon_payment_request',
        'list_coupon_types',
        'list_coupons',
        'list_vouchers',

        # Notifications
        'add_notification_callback',
        'add_notification_message',
        'remove_notification_callback',
        'send_email_to_customer',

        # Invoices
        'generate_invoice',
        'get_invoice_items',
        'list_invoices',

        # Templates
        'process_template',

        # Translations
        'list_translations',
        'set_translation'
    )

    def __init__(self, api_key, hash_key=None):
        """
        :param api_key: Planyo API key
        :param hash_key: Planyo secret hash key
        """
        self.api_key = api_key
        self.hash_key = hash_key

    def _get_hash_key(self, ts, method):
        """
        Calculate hash key

        :param ts: Timestamp
        :param method: Function name
        :return: MD5 hash
        """
        return md5('{hash_key}{ts}{method}'.format(hash_key=self.hash_key, ts=ts, method=method).encode()).hexdigest()

    def _wrapper(self, method):
        """
        Wrapper to implement all methods dynamically

        :param method: Function name
        :return: Function to request Planyo API with the desired method
        """

        def perform_request(params=None, retry=3):
            """
            Requests for Planyo API

            :param params: Dict with arguments to request `method`
            :param retry: Aux value to retry requests
            :return: Response from Planyo API
            """
            args = dict(method=method, api_key=self.api_key)
            if self.hash_key:
                ts = int(time())
                args.update(hash_timestamp=ts, hash_key=self._get_hash_key(ts, method))

            if params:
                params.update(args)
            else:
                params = args

            try:
                response = requests.post(self.endpoint, data=params)
            except (requests.ReadTimeout, requests.ConnectTimeout, requests.ConnectionError):
                if retry > 0:
                    return self._perform_request(params, is_hash_enabled, retry=retry - 1)

                raise ServerConnectionLostException

            try:
                return response.json()
            except JSONDecodeError as e:
                raise e

        return perform_request

    def __getattr__(self, item):
        """
        Method overwrite for dynamic API methods

        :param item: method name
        :return: Function to request Planyo API with the desired method
        """
        if item in self.methods:
            return self._wrapper(method=item)


class ServerConnectionLostException(Exception):
    """
    Planyo API Server is Down
    """


__all__ = ('Planyo', 'ServerConnectionLostException')

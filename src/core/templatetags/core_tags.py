from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def alert_type_class(value):
    if value in ['cod', 'delivery', 'in_transit', 'bank_account', "MANAGER", "trialing", 'new']:
        return 'primary'
    if value in ['cod', 'delivery', 'in_transit', 'bank_account', "CASHIER", "incomplete", "incomplete_expired",
                 'closed']:
        return 'info'
    elif value in ['completed', 'success', 'approved', 'paid', 'card', "OWNER", "active", "sent", 'resolved']:
        return 'success'
    elif value in ['pending', "STAFF", "ADMIN", "past_due", "pause", 'in_progress']:
        return 'warning'
    elif value in ['online', 'cancel', 'cancelled', 'unpaid', 'failed', "ROOT", "failed"]:
        return 'danger'
    else:
        return 'secondary'


@register.filter
def check_null(value):
    if value:
        return value
    return "-"
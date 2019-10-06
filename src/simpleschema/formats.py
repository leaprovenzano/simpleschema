from enum import Enum
from itertools import chain


class Date(Enum):

    date_time = 'date-time'
    time = 'date-time'
    date = 'date'


class Email(Enum):

    email = 'email'
    idn_email = 'idn-email'


class HostName(Enum):

    hostname = 'hostname'
    idn_hostname = 'idn-hostname'


class IPAddress(Enum):

    ipv4 = 'ipv4'
    ipv6 = 'ipv6'


class ResourceIdentifier(Enum):

    uri = 'uri'
    uri_reference = 'uri-reference'
    iri = 'iri'
    iri_reference = 'iri-reference'
    uri_template = 'uri-template'


class JSONPointer(Enum):

    json_pointer = 'json-pointer'
    relative_json_pointer = 'relative-json-pointer'


class Regex(Enum):

    regex = 'regex'


Format = Enum(
    'Format',
    [
        (i.name, i.value)
        for i in chain(Date, Email, HostName, IPAddress, ResourceIdentifier, JSONPointer, Regex)
    ],
)

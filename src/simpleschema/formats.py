from enum import Enum
from itertools import chain


class FormatEnum(Enum):

    @property
    def schema(self):
        return {'type': 'string', 'format': self.value}


class Date(FormatEnum):

    date_time = 'date-time'
    time = 'time'
    date = 'date'


class Email(FormatEnum):

    email = 'email'
    idn_email = 'idn-email'


class HostName(FormatEnum):

    hostname = 'hostname'
    idn_hostname = 'idn-hostname'


class IPAddress(FormatEnum):

    ipv4 = 'ipv4'
    ipv6 = 'ipv6'


class ResourceIdentifier(FormatEnum):

    uri = 'uri'
    uri_reference = 'uri-reference'
    iri = 'iri'
    iri_reference = 'iri-reference'
    uri_template = 'uri-template'


class JSONPointer(FormatEnum):

    json_pointer = 'json-pointer'
    relative_json_pointer = 'relative-json-pointer'


class Regex(FormatEnum):

    regex = 'regex'


Format = FormatEnum(
    'Format',
    [
        (i.name, i.value)
        for i in chain(Date, Email, HostName, IPAddress, ResourceIdentifier, JSONPointer, Regex)
    ],
)

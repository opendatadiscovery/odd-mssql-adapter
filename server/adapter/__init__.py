from collections import namedtuple

_adapter_prefix: str = "mssql/"

_data_set_metadata_schema_url: str = \
    "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/" \
    "extensions/mssql.json#/definitions/MssqlDataSetExtension"
_data_set_field_metadata_schema_url: str = \
    "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/" \
    "extensions/mssql.json#/definitions/MssqlDataSetFieldExtension"

_table_metadata: str = \
    "table_catalog, table_schema, table_name, table_type"
_table_table: str = "information_schema.tables"
_table_order_by: str = "table_catalog, table_schema, table_name"

_column_metadata: str = \
    "table_catalog, table_schema, table_name, column_name, ordinal_position, column_default, is_nullable, " \
    "data_type, character_maximum_length, character_octet_length, " \
    "numeric_precision, numeric_precision_radix, numeric_scale, datetime_precision, " \
    "character_set_catalog, character_set_schema, character_set_name, " \
    "collation_catalog, collation_schema, collation_name, domain_catalog, domain_schema, domain_name"
_column_table: str = "information_schema.columns"
_column_order_by: str = f"{_table_order_by}, ordinal_position"

MetadataNamedtuple = namedtuple("MetadataNamedtuple", _table_metadata)
ColumnMetadataNamedtuple = namedtuple("ColumnMetadataNamedtuple", _column_metadata)

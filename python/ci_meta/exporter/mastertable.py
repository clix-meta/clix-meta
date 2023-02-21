# -*- coding: utf-8 -*-

import logging
import regex as re

import pyexcel as pe


# Order matters! Earlier operators will be preferred,
# so <= MUST appear before <, etc.
SUPPORTED_OPERATORS = [
    '<=',
    '>=',
    '<',
    '>',
]
SUPPORTED_REDUCERS = [
    'min',
    'max',
    'sum',
    'mean',
]


def build_period(spec):
    PERIODS = {
        'annual': 'annual',
        'seasonal': 'seasonal',
        'monthly': 'monthly',
        '_': 'unknown',
        '': 'unknown',
    }
    return PERIODS[spec]


def tr_cell_methods(cell_method_string):
    name = r'(?P<name>\w+):'
    method = (r'(?P<method>('
              r'point|sum|maximum|maximum_absolute_value|median|'
              r'mid_range|minimum|minimum_absolute_value|mean|'
              r'mean_absolute_value|mean_of_upper_decile|mode|'
              r'range|root_mean_square|standard_deviation|'
              r'sum_of_squares|variance))')
    where = r'where'
    type1 = r'(?P<type1>\w+)'
    type2 = r'(?P<type2>\w+)'
    clim_indicator = r'(?P<indicator>(within|over))'
    clim_unit = r'(?P<unit>(days|years))'
    cell_method = re.compile(
        f'({name} )+{method}'
        f'(( {where} {type1}( over {type2})?)|'
        f'( {clim_indicator} {clim_unit}))?')
    cms = [m.group(0) for m in cell_method.finditer(cell_method_string)]
    return cms


def split_parts(no_parts, part_string):
    if no_parts == 0:
        return []
    parts = [p.strip() for p in part_string.split(',')]
    assert len(parts) == no_parts
    return parts


def tr_inputs(input):
    inputs = {}
    for input_variable in input.split(','):
        key, variable = input_variable.split(':')
        inputs[key.strip()] = variable.strip()
    return inputs


def tr_parameter(parameter):
    if parameter['operator'] is not None:
        d = {'var_name': parameter['name'],
             'kind': 'operator',
             'operator': parameter['operator']}
    elif parameter['reducer'] is not None:
        d = {'var_name': parameter['name'],
             'kind': 'reducer',
             'reducer': parameter['reducer']}
    elif parameter['value'] is not None:
        raw_value = parameter['value']
        try:
            float(raw_value)
            value = raw_value
        except ValueError:
            value = f'"{raw_value}"'
        d = {'var_name': parameter['name'],
             'kind': 'quantity',
             'standard_name': parameter['standard_name'],
             'proposed_standard_name': parameter['proposed_standard_name'],
             'data': value,
             'units': parameter['units'],
             'long_name': parameter['long_name']}
    elif parameter["time_range"] is not None:
        d = {
            "var_name": parameter["name"],
            "kind": "time_range",
            "data": parameter["time_range"],
        }
    else:
        raise RuntimeError(f"Invalid parameter found {parameter[0]}")
    return d


def split_parameter_definitions(parameter_definitions_string, parameter_names):
    name_regex = r'(?P<name>{})'.format('|'.join(parameter_names))
    op_regex = r'(?P<operator>{})'.format('|'.join(SUPPORTED_OPERATORS))
    red_regex = r'(?P<reducer>{})'.format('|'.join(SUPPORTED_REDUCERS))
    qty_regex = (
        r'\(var_name: (?P<var_name>[^,]*), '
        r'standard_name: (?P<standard_name>[^,]*), '
        r'(proposed_standard_name: (?P<proposed_standard_name>[^,]*), )?'
        r'value: (?P<value>[^,]*), '
        r'unit: (?P<units>[^,)]*)(, |\))'
        r'(long_name: \p{Pi}(?P<long_name>[^\p{Pf}]*)\p{Pf}\))?')
    timestamp_regex = (
        r"[1-9][0-9]*(-[0-1][0-9](-[0-3][0-9](T[0-2][0-9][0-5][0-9][0-5][0-9])?)?)?"
    )
    period_regex = r"P[0-9]*Y([0-9]*M([0-9]*D)?)?"
    time_range_regex = rf"(?P<time_range>{timestamp_regex}/{timestamp_regex}|{timestamp_regex}/{period_regex}|{period_regex}/{timestamp_regex})"
    param_regex = r"{}: (?:{}|{}|{}|{})".format(
        name_regex, red_regex, op_regex, qty_regex, time_range_regex
    )
    matcher = re.compile(param_regex)
    result = [tr_parameter(p)
              for p in matcher.finditer(parameter_definitions_string)]
    return result


def tr_index_function(index_name, name, no_thresholds,
                      parameter_names_string, parameter_definitions_string):
    parameter_names = split_parts(no_thresholds, parameter_names_string)
    parameters = split_parameter_definitions(parameter_definitions_string,
                                             parameter_names)
    found_parameters = set(p['var_name'] for p in parameters)
    if found_parameters != set(parameter_names):
        logging.warn(f"For index {index_name}, the parameters listed in "
                     f"parameter_name ({parameter_names}) are different from "
                     f"those defined in PARAMETER_definition "
                     f"({found_parameters}). Please check the table!")
    index_function = {
        'name': name,
        'parameters': parameters,
    }
    return index_function


def prepare_record(record):
    var_name = record['VarName']
    no_parameters = int(record['N_parameters'])
    d = {
        'var_name': var_name,
        'reference': record['OUTPUT_reference'],
        'default_period': build_period(record['default_period']),
        'output': {
            'var_name': var_name,
            'standard_name': record['OUTPUT_standard_name'],
            'proposed_standard_name': record['OUTPUT_proposed_standard_name'],
            'long_name': record['OUTPUT_long_name'],
            'cell_methods': tr_cell_methods(record['OUTPUT_cell_methods']),
            'units': record['OUTPUT_units'],
        },
        'inputs': tr_inputs(record['input']),
        'index_function': tr_index_function(
            var_name,
            record['index_function'],
            no_parameters,
            record['parameter_name'], record['PARAMETER_definition']),
        'ET': {
            'short_name': record['ET_short_name'],
            'long_name': record['ET_long_name'],
            'definition': record['ET_definition'],
            'comment': record['ET_comment'],
        }
    }
    proposed_standard_name = record['OUTPUT_proposed_standard_name']
    if proposed_standard_name.strip() != '':
        d['output']['proposed_standard_name'] = proposed_standard_name
    return d


def build_index_definitions(file_name):
    sheet = pe.get_sheet(file_name=file_name,
                         sheet_name='index_definitions')
    sheet.name_columns_by_row(0)
    records = sheet.to_records()
    index_definitions = []
    for record in records:
        try:
            ready = int(record['ready'])
        except ValueError:
            ready = -1
        if ready != 1:
            continue
        index_definitions.append(prepare_record(record))
    return index_definitions


def prepare_variable_record(record):
    var_name = record['var_name'].strip()
    d = {
        'var_name': var_name,
        'standard_name': record['standard_name'].strip(),
        'cell_methods': tr_cell_methods(record['cell_methods']),
        'aliases': [a.strip() for a in record['aliases'].split(',')],
        'comment': record['comment'].strip()
    }
    return d


def build_variables(file_name):
    sheet = pe.get_sheet(file_name=file_name,
                         sheet_name='variables')
    sheet.name_columns_by_row(0)
    records = sheet.to_records()
    variables = []
    for record in records:
        if record['var_name'].strip() == '':
            continue
        variables.append(prepare_variable_record(record))
    return variables

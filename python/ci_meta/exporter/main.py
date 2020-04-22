# -*- coding: utf-8 -*-

import argparse
from contextlib import contextmanager
import logging

from jinja2 import Environment, PackageLoader

import ci_meta
from .mastertable import build_index_definitions, build_variables


def add_space(variable, quote=False):
    value = variable.strip()
    if len(value) > 0:
        if quote:
            return ' "{}"'.format(value)
        else:
            return ' {}'.format(value)
    else:
        return value


def prepare_environment(args):
    loader = PackageLoader('ci_meta.exporter')
    env = Environment(
        loader=loader,
        trim_blocks=True,
    )
    env.filters['add_space'] = add_space
    return env


def parse_args():
    parser = argparse.ArgumentParser(
        description=(f'An exporter for climate index metadata, '
                     f'version {ci_meta.__version__}.'))
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('-t', '--table-version', default=ci_meta.__version__)
    parser.add_argument('document')
    return parser.parse_args()


@contextmanager
def opened_w_force(filename, force):
    try:
        f = open(filename, 'x')
    except FileExistsError:
        if force:
            logging.warning('File {} already exists. '
                            'Overwriting due to --force'.format(filename))
            f = open(filename, 'w')
        else:
            raise
    try:
        yield f
    finally:
        f.close()


def main():
    args = parse_args()
    env = prepare_environment(args)
    var_definition_template = env.get_template('variables.yml')
    var_definitions = build_variables(args.document)
    var_output = var_definition_template.render(variables=var_definitions,
                                                version=args.table_version)

    idx_definition_template = env.get_template('index_definitions.yml')
    idx_definitions = build_index_definitions(args.document)
    idx_output = idx_definition_template.render(indices=idx_definitions,
                                                version=args.table_version)

    with opened_w_force('variables.yml', args.force) as outfile:
        outfile.write(var_output)

    with opened_w_force('index_definitions.yml', args.force) as outfile:
        outfile.write(idx_output)

#!/usr/bin/env python2
# ruleset        ::= ( general-rule | output-spec )*
# general-rule   ::= ( '__default' : ( '__keep' | '__drop' ) ) |
#                    ( '__except' : keylist ) |
# output-spec    ::= output-key : input-spec
# keylist        ::= [ key* ]
# output-key     ::= string
# input-spec     ::= ( input-key ) |
#                    ( complex-input )
# input-key      ::= string
# complex-input  ::= { source-spec? nsplitc-spec? translate-spec? '}'
# source-spec    ::= '__source' : { output-spec* }
# nsplitc-spec     ::= '__split' : ( integer | key )
# translate-spec ::= '__translate' : { ( key : { ( oldval : newval )+ } )+ }

class JTException(Exception): # {{{
    # subclassing the general Exception in order to have one
    # specific to jsontranslate
    pass
# }}}
try:
    foo = unicode
except NameError:
    unicode = str
def apply_ruleset(rules, in_data): # {{{
    out_data = collections.OrderedDict()
    processed_keys = set()
    upk_default = None
    upk_except = set()

    # Iterate over the rules dict (the keys are put in rk, the values in rv)
    # and apply them to the in_data if applicable. Some rules are special
    # and they begin with a double underscore. For now it's only __default,
    # which define if items in the input that match no other rule should be
    # kept as-is, or dropped entirely, and __except, which gives the opportunity
    # add exceptions to this rule (i.e. input items that should be dropped by
    # default, if the default rule is to keep, or the other way around).
    # If the rule does not have a key starting with double underscore, we process
    # it, and the input, with apply_input_spec. Two values are returned from this
    # function, the processed data (result), and a set of data keys that have been
    # used in the function. This in order to stop them from being subjected to the
    # default rule mentioned earlier, that is applied to all fields that match no rule.
    # The result data is put into the output data with the key that is the name of
    # the rule, that is the rk variable.
    for rk,rv in rules.items(): # {{{
        result = None
        if rk == '__default' :
            if rv in ['__keep', '__drop']:
                upk_default = rv
            else:
                raise JTException('__default rule should be "__keep" or "__drop", and not "{}"'.format(rv))
        elif rk == '__except':
            upk_except = set(rv)
        elif not rk.startswith('__'):
            try:
                result, pk = apply_input_spec(rv, in_data)
            except JTException as e:
                raise JTException('applying rule "{}":\n{}'.format(
                    rk, e.args[0]).replace('\n', '\n\t'))
            out_data[rk] = result
            processed_keys |= pk
    # }}}
    # After trying to apply every rule the input field keys that have so far not been used,
    # get subjected to the default rule if it exists.
    unprocessed_keys = set(in_data.keys()) - processed_keys
    if len(unprocessed_keys) > 0: # {{{
        if upk_default is not None:
            for key in unprocessed_keys:
                if (key in upk_except and upk_default == '__drop') or (key not in upk_except and upk_default == '__keep'):
                    out_data[key] = in_data[key]
        else:
            raise JTException('input contains key(s) ({}) for which there are no rule, and no default rule is specified'.format(
                '"' + '", "'.join([str(_) for _ in unprocessed_keys]) + '"'))
    # }}}
    # Lastly, the rest of this function separates "thick" items like dicts and lists, i.e.
    # items containing subitems from "thin" items, that are only singular values, and
    # orders the result, so that the thin items are placed at the top. This is just asthetics.
    out_data_thin = collections.OrderedDict()
    out_data_thick = collections.OrderedDict()
    for k,v in out_data.items():
        if isinstance(v, dict) or isinstance(v, list):
            out_data_thick[k] = v
        else:
            out_data_thin[k] = v
    out_data_ordered = collections.OrderedDict()
    out_data_ordered.update(out_data_thin)
    out_data_ordered.update(out_data_thick)
    return out_data_ordered
# }}}
def apply_input_spec(ispec, in_data): # {{{
    # If the input spec (ispec) is a string* the rule just mandates a renaming of the field
    # and this functions role is just to extract and return the data field specified by the string.
    # The new name of the field will, as in the other cases, be the name of the rule, and is part of
    # the apply_ruleset function. For input specs that are other types, the rules, and their application
    # is more complex.
    # *: Both unicode and str tests are done, since they are different datatypes in python 2, see also
    # the test at line 20
    if isinstance(ispec, str) or isinstance(ispec, unicode):
        try:
            value = in_data[ispec]
        except KeyError as e:
            raise JTException('The input has no field with the key "{}".'.format(e.args[0]))
        return value, set([ispec])
    else:
        # The more complex rules use additional keywords, again prefixed by double underscore:
        # __source:    A key-value map of the same type as the general rule, that is either
        #              just string keys mapped to string values in order to rename values, or more
        #              complex rules.
        # __split:     If this keyword is present, the value is supposed to either be a number, or
        #              the name of an input field that will contain a number. The generated data
        #              from the rest of the ruleset is then expected to be contain comma separated
        #              values, that can be split up in this number of items. If the __source contents
        #              is a dict they will all be split, and a list of dicts will be generated.
        #              If it's a string, a list of strings is generated from the data.
        # __translate: This keyword can be used in case one or more values need to be changed.
        #              It should contain a map, whose keys are the field names (as they are named
        #              in the output) and the value is another map. This other map is filled with
        #              key-value pairs containing the input-output mappings.
        source = None
        translation = None
        nsplitc = None
        processed_keys = set()
        for cik,civ in ispec.items(): # {{{
            if cik == '__source': # {{{
                if isinstance(civ, str) or isinstance(civ, unicode):
                    source = in_data[civ]
                    processed_keys |= set(civ)
                else:
                    source = collections.OrderedDict()
                    for isk,isv in civ.items():
                        try:
                            result,pks = apply_input_spec(isv, in_data)
                            source[isk] = result
                            processed_keys |= pks
                        except JTException as e:
                            raise JTException('Error applying rule for the __source field with key "{}":\n{}'.format(
                                isk, e.args[0]).replace('\n', '\n\t'))
            # }}}
            elif cik == '__split': # {{{
                if civ.isnumeric():
                    nsplitc = int(civ)
                else:
                    try:
                        nsplitc = int(in_data[civ])
                        processed_keys |= set(civ)
                    except KeyError:
                        raise JTException('The __split field references a field with key "{}" which does not exist.'.format(
                            civ))
                    except ValueError as e:
                        raise JTException('The __split field references a field with key "{}" which does not contain an integer, but "{}".'.format(
                            civ, in_data[civ]))
            # }}}
            elif cik == '__translate': # {{{
                translation = civ
            # }}}
        # }}}
        # apply split
        if nsplitc is not None:
            source = apply_split(source, nsplitc)
        # apply value translation
        if translation is not None:
            source = apply_translation(source, translation)
        # sort by "thickness" of datatypes just as in apply_ruleset()
        out_data_thin = collections.OrderedDict()
        out_data_thick = collections.OrderedDict()
        return source, processed_keys
# }}}
def apply_split(in_data, nsplitc): # {{{
    out_data = None
    if nsplitc == 0:
        return []
    if isinstance(in_data, str) or isinstance(in_data, unicode):
        out_data = in_data.split(',')
        if len(out_data) != nsplitc:
            raise JTException('Splitting "{}" does not yield a list of the expected {}, but instead {} elements.'.format(
                vl, nsplitc, len(out_data)))
        for index,item in enumerate(out_data):
            out_data[index] = item.strip()
    elif isinstance(in_data, dict):
        out_data = [{} for _ in range(nsplitc)]
        for k,v in in_data.items():
            vl = v.split(',')
            if len(vl) != nsplitc:
                raise JTException('Splitting "{}":"{}" does not yield a list of the expected {}, but instead {} elements.'.format(
                    k, v, nsplitc, len(vl)))
            for index,item in enumerate(vl):
                out_data[index][k] = item.strip()
    return out_data
# }}}
def apply_translation(in_data, translation): # {{{
    out_data = in_data
    if isinstance(in_data, str) or isinstance(in_data, unicode):
        if in_data in translation:
            out_data = translation[in_data]
    elif isinstance(in_data, list):
        out_data = [apply_translation(x, translation) for x in in_data]
    elif isinstance(in_data, dict):
        out_data = {}
        for k,v in in_data.items():
            if k in translation:
                out_data[k] = apply_translation(v, translation[k])
            else:
                out_data[k] = v
    return out_data
# }}}

import sys, json, collections

if len(sys.argv) == 1:
    sys.stderr.write("We need to have a set of rules as the parameter\n")
    sys.exit(1)

# The first command line parameter is the rules file, load it, and use the
# json library to parse it. Make sure that the order of the rules as they
# listed file are kept by using an OrderedDict instead of a regular dict
# After this, the data to be processed is read from standard in, and parsed
# as json as well.
rules = None
with open(sys.argv[1], 'r') as rulesfd:
    rules = json.load(rulesfd, object_pairs_hook=collections.OrderedDict)
inp = json.loads(sys.stdin.read(), object_pairs_hook=collections.OrderedDict)
out = []

# Iterate over the input data elements, but use enumerate() so that we get both
# an index number (i), as well as the data item (elem). The index makes debugging
# easier. For each elem, apply the ruleset and append the result to the output
# list. Catch any error exceptions and print verbose diagnostics.
for i,elem in enumerate(inp): # {{{
    try:
        out.append(apply_ruleset(rules, elem))
    except JTException as e:
        sys.stderr.write("================================================================================\n")
        sys.stderr.write("Error processing input index {}\n".format(i))
        sys.stderr.write("--------------------------------------------------------------------------------\n")
        sys.stderr.write(json.dumps(elem, indent=2)+'\n')
        sys.stderr.write("--------------------------------------------------------------------------------\n")
        sys.stderr.write(e.args[0]+'\n')
        sys.stderr.write("================================================================================\n")
        if '__error' in rules and rules['__error'] == 'quit':
            sys.exit(2)
# }}}

# Use the json library to write all the output data as neatly formatted json.
sys.stdout.write(json.dumps(out, indent=2)+'\n')

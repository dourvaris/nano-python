"""
Generates docs for the rpc client
"""

import os
import sys
import inspect
import textwrap

from nano.rpc import Client


def indent(value, n=2, character=' '):
    """
    Indent a value by `n` `character`s

    :param value: string to indent
    :param n: number of characters to indent by
    :param character: character to indent with
    """

    prefix = n * character
    return '\n'.join(prefix + line for line in value.splitlines())


def extract_docs():
    """
    Parses the nano.rpc.Client for methods that have a __doc_meta__ attribute
    and saves generated docs
    """

    methods = []

    def _key(entry):
        return

    sorted_entries = sorted(Client.__dict__.items(), key=lambda x: x[0])

    tree = {}
    meta_key = '__doc_meta__'

    for attr_name, attr_value in sorted_entries:

        if not hasattr(attr_value, meta_key):
            continue

        func = attr_value
        meta = getattr(func, meta_key)

        arg_spec = inspect.getargspec(func)
        if arg_spec[0] and arg_spec[0][0] in ('cls', 'self'):
            del arg_spec[0][0]

        func_name = func.__name__
        func_spec = func_name + inspect.formatargspec(*arg_spec)

        doc = textwrap.dedent((func.__doc__ or ''))
        doc = indent(doc, n=3)

        func_desc_lines = []
        for i, line in enumerate(func.__doc__.splitlines()):
            if i == 0:
                continue
            func_desc_lines.append(line.strip())
            if not line:
                break
        func_desc = ' '.join(func_desc_lines)

        doc = textwrap.dedent("""\
            {func_name}
            {func_name_line}

            {func_desc}
            :py:func:`nano.rpc.Client.{func_spec} <nano.rpc.Client.{func_name}>`

            .. .. py:function:: nano.rpc.Client.{func_spec}

            .. {doc}
            """).format(func_spec=func_spec,
                        func_name_line='-' * len(func_name),
                        func_name=func_name,
                        func_desc=func_desc,
                        doc=doc)

        categories = meta['categories']
        for category in categories:
            tree.setdefault(category, []).append(doc)

    directory = 'rpc/methods'
    for file in os.listdir(directory):
        if file.endswith('.rst'):
            os.unlink(os.path.join(directory, file))

    for category, func_docs in sorted(tree.items(), key=lambda x: x[0]):
        category = category or 'other'
        file_path = os.path.join(directory, category) + '.rst'
        with open(file_path, 'w') as docfile:
            docfile.write('.. _%s-ref:\n' % category + '\n')
            title = '{category}'.format(category=category.capitalize())
            docfile.write('%s\n' % title)
            docfile.write('%s\n' % (len(title) * '='))
            docfile.write('\n')


            for func_doc in func_docs:
                docfile.write(func_doc + '\n')

if __name__ == '__main__':
    extract_docs()

from .core import CatboostError
from collections import defaultdict

def create_cd(
    label=None,
    cat_features=None,
    weight=None,
    baseline=None,
    doc_id=None,
    group_id=None,
    subgroup_id=None,
    timestamp=None,
    auxiliary_columns=None,
    feature_names=None,
    output_path='train.cd'
):
    _from_param_to_cd = {
        'label': 'Label',
        'weight': 'Weight',
        'baseline': 'Baseline',
        'doc_id': 'DocId',
        'group_id': 'GroupId',
        'subgroup_id': 'SubgroupId',
        'timestamp': 'Timestamp'
    }
    _column_description = defaultdict(lambda : ['Num', ''])
    for key, value in locals().copy().items():
        if not (key.startswith('_') or value is None):
            if key in ('cat_features', 'auxiliary_columns'):
                if isinstance(value, int):
                    value = [value]
                for index in value:
                    if not isinstance(index, int):
                        raise CatboostError('Unsupported index type. Expected int, got {}'.format(type(index)))
                    if index in _column_description:
                        raise CatboostError('The index {} occurs more than once'.format(index))
                    _column_description[index] = ['Categ', ''] if key == 'cat_features' else ['Auxiliary','']
            elif not key in ('feature_names', 'output_path'):
                if not isinstance(value, int):
                    raise CatboostError('Unsupported index type. Expected int, got {}'.format(type(value)))
                if value in _column_description:
                    raise CatboostError('The index {} occurs more than once'.format(value))
                _column_description[value] = [_from_param_to_cd[key], '']
    if not feature_names is None:
        for index, name in feature_names.items():
            _column_description[index][1] = name
    with open(output_path, 'w') as f:
        for index, (title, name) in sorted(_column_description.items()):
            f.write('{}\t{}\t{}\n'.format(index, title, name))

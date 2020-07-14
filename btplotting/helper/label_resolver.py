import backtrader as bt

from ..utils import get_params_str, get_clock_obj


def datatarget2label(datas):

    """
    Convert datas (usually a datafeed but might also be an indicator if
    one indicator operates on another indicator) to a readable string.
    If a name was provided manually then use that.
    """

    # try some popular attributes that might carry string represantations
    # _name: user assigned value upon instantiation
    # shortname: used by some datafeeds
    # _dataname: underlying bt dataname (should always be available
    # as last resort)
    prim_names = ['_name', 'shortname', '_dataname']
    labels = []
    for d in datas:
        if isinstance(d, bt.IndicatorBase):
            labels.append(indicator2label(d))
        elif isinstance(d, bt.AbstractDataBase):
            for n in prim_names:
                val = getattr(d, n, "")
                if val is None:
                    continue
                val = str(val)

                if len(val) > 0:
                    labels.append(val)
                    break
        else:
            raise RuntimeError(f'Unexpected data type: {d.__class__}')

    if len(labels) == 0:
        return "Unidentified"
    return ','.join(labels)


def strategy2label(strategycls, params):
    label = strategycls.__name__
    parameter_labels = get_params_str(params)
    if len(parameter_labels) > 0:
        label += f' [{parameter_labels}]'
    return label


def plotobj2label(obj):
    if isinstance(obj, bt.IndicatorBase):
        return f'{indicator2label(obj)}@{indicator2fullid(obj)}'
    elif isinstance(obj, bt.ObserverBase):
        return f'{observer2label(obj)}'
    elif isinstance(obj, bt.AbstractDataBase):
        return obj.__class__.__name__
    else:
        raise RuntimeError(f'Unsupported type: {obj.__class__.__name__}')


def indicator2label(ind):
    return ind.plotlabel()


def observer2label(obs):
    return obs.plotlabel()


def strategy2shortname(strategy):
    return strategy.plotinfo.plotname or strategy.__class__.__name__


def indicator2fullid(ind):

    """
    Returns a string listing all involved data feeds. Empty string if
    there is only a single feed in the mix
    """

    if isinstance(ind, bt.LineActions):
        return "Line Action"

    names = []
    for x in ind.datas:
        if isinstance(x, bt.AbstractDataBase):
            return datatarget2label([x])
        elif isinstance(x, bt.LineSeriesStub):
            # indicator target is one specific line of a datafeed
            # add "[L]" at the end
            return datatarget2label([get_clock_obj(x)]) + ' [L]'
        elif isinstance(x, bt.IndicatorBase):
            names.append(indicator2label(x))
    return f"({','.join(names)})"
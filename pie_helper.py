"""
Creates labels and percentage labels for matplotlib.pie().'

Authors: Mark Bannister (make_labels), 'unutbu' (make_autopct)
Source: http://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct
"""
def make_labels(categories,values):
    """Make pie chart labels with category names and values.
    Args:
        categories (list): list of pie chart categories.
        values (list): list of pie chart values.
    Returns:
        labels (list): list of pie chart labels in the format "Category (Value)".
    """
    labels = []
    for i in range(0, len(values)):
        labels.append("{c} ({v})".format(c=categories[i], v=values[i]))
    return labels

def make_autopct(values):
    """Make pie chart autopct labels.
    Args:
        values (list): list of pie chart values.
    Returns:
        my_autopct (function): function to pass to autopct parameter.
    """
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.1f}%'.format(p=pct,v=val)
    return my_autopct
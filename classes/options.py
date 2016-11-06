class Options:
    """Collection of options.

    Attributes:
        iterations (int): Number of iterations.
        max_rules (int): Max number of rules per iterations.
        name_tag (str): The formating for names.
        norm_tag (bool): Enable the nomralization  of numbers.
        norm_prof (bool): Enable the normalization of professions.
        left_tag (str): Left tag of a sentence.
        right_tag (str): Right tag of a sentence.
        tablet (bool): Add start of tablet line.
        mode (str): Switch between `csv` and `multiline` modes.
    """

    def __init__(self, iterations, max_rules, name_tag, norm_num,
                 norm_prof, left_tag, right_tag, tablet, mode):
        """Sets the ``iterations``, ``max_rules``, ``name_tag``, ``norm_num``,
        ``norm_prof``, ``left_tag``, ``right_tag``, ``tablet``, and ``mode``
        attributes for the ``Options`` class.

        Args:
            iterations (int): Number of iterations.
            max_rules (int): Max number of rules per iterations.
            name_tag (str): The formating for names.
            norm_tag (bool): Enable the nomralization  of numbers.
            norm_prof (bool): Enable the normalization of professions.
            left_tag (str): Left tag of a sentence.
            right_tag (str): Right tag of a sentence.
            tablet (bool): Add start of tablet line.
            mode (str): Switch between `csv` and `multiline` modes.

        Returns:
            None

        Raises:
            None
        """

        self.iterations = iterations
        self.max_rules = max_rules
        self.name_tag = name_tag
        self.norm_num = norm_num
        self.norm_prof = norm_prof
        self.left_tag = left_tag
        self.right_tag = right_tag
        self.tablet = tablet
        self.mode = mode



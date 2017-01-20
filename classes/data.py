"""Data"""
class Data:
    """Collection of locations for data files.

    Attributes:
        corpus (str): Location of corpus file.
        attestations (str): Location of attestations file.
        seed_rules (str): Location of seed rules file.
        output (str): Location of output file.
    """

    def __init__(self, corpus, attestations, seed_rules,
                 train, dev, test, output, log):
        """Sets the ``corpus``, ``attestations``, ``seed_rules``, and
        ``output`` attributes for the ``Data`` class.

        Args:
            corpus (str): Location of corpus file.
            attestations (str): Location of attestations file.
            seed_rules (str): Location of seed rules file.
            output (str): Location of output file.

        Returns:
            None

        Raises:
            None
        """

        self.corpus = corpus
        self.attestations = attestations
        self.seed_rules = seed_rules
        self.train = train
        self.dev = dev
        self.test = test
        self.output = output
        self.log = log

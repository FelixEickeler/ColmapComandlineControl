from enum import Enum


class NamedEnum(Enum):
    @staticmethod
    def fromBinaryString(str):
        steps = []
        for binary, switch in enumerate(str):
            if switch == "1":
                steps.append(Steps(2 ** binary))
        return steps

    def __iter__(self):
        return self

    def next(self):
        try:
            integer = 2 ^ self.value
            yield Steps(integer)
        except Exception:
            raise StopIteration()

    def name(self):
        return self.__str__().split(".")[-1]


class MatchingStrategy(NamedEnum):
    exhaustive_matcher = 1
    sequential_matcher = 2
    vocab_tree_matcher = 4
    transitive_matcher = 8

    def __init__(self, value):
        NamedEnum.__init__(self, value)
        self.vocab_tree_path = ""


class Steps(NamedEnum):
    feature_extractor = 1
    matcher = 2
    mapper = 4
    image_undistorter = 8
    dense_stereo = 16
    dense_fuser = 32
    create_statistics = 64

    def __init__(self, value):
        NamedEnum.__init__(self, value)
        self.matching_strategy = MatchingStrategy.exhaustive_matcher

    def name(self):
        name = super(Steps, self).name()
        return name if name != "matcher" else self.matching_strategy.name()

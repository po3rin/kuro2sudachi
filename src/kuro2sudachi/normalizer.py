import sys
import unicodedata


class SudachiCharNormalizer:
    def __init__(self, rewrite_def_path="./rewrite.def"):
        self.ignore_normalize_set = set()
        self.replace_char_map = {}
        self.read_rewrite_def(rewrite_def_path)

    def read_rewrite_def(self, rewrite_def_path):
        with open(rewrite_def_path, encoding="utf8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line.startswith("#") or not line:
                    continue

                cols = line.split()
                if len(cols) == 1:
                    if len(cols[0]) != 1:
                        raise Exception(
                            "'{}' is not a single character at line {}".format(
                                cols[0], i
                            )
                        )
                    self.ignore_normalize_set.add(cols[0])
                elif len(cols) == 2:
                    if cols[0] in self.replace_char_map:
                        raise Exception(
                            "'Replacement for '{}' defined again at line {}".format(
                                cols[0], i
                            )
                        )
                    self.replace_char_map[cols[0]] = cols[1]
                else:
                    raise Exception("Invalid format '{}' at line {}".format(line, i))

    def rewrite(self, text):
        chars_after = []

        offset = 0
        next_offset = 0
        i = -1
        while True:
            i += 1
            if i >= len(text):
                break
            textloop = False
            offset += next_offset
            next_offset = 0

            # 1. replace char without normalize
            for l in range(len(text) - i, 0, -1):
                replace = self.replace_char_map.get(text[i : i + l])
                if replace:
                    chars_after.append(replace)
                    next_offset += len(replace) - l
                    i += l - 1
                    textloop = True
                    continue
            if textloop:
                continue

            # 2. normalize
            # 2-1. capital alphabet (not only latin but greek, cyrillic, etc) -> small
            original = text[i]
            lower = original.lower()
            if lower in self.ignore_normalize_set:
                replace = lower
            else:
                # 2-2. normalize (except in ignoreNormalize)
                # e.g. full-width alphabet -> half-width / ligature / etc.
                replace = unicodedata.normalize("NFKC", lower)
            next_offset = len(replace) - 1
            chars_after.append(replace)

        return "".join(chars_after)

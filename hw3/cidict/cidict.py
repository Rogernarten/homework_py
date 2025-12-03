# cidict.py
#
# Yixiao Huang
#
# This file defines the CIDict class, a case-insensitive dictionary that
# normalizes all string keys to lower case while preserving dictionary behavior.
# The class supports standard dictionary operations such as item assignment,
# lookup, deletion, and also provides a method for applying a transformation
# function to all stored values.


# write your CIDict here
class CIDict(dict):
    """
    A case-insensitive dictionary where all string keys are internally converted
    to lower case. Non-string keys are left unmodified. The class behaves like a
    standard Python dictionary except for key normalization.

    Keys:
      All string keys are transformed to their lower-case representation.

    Initialization:
      Accepts keyword arguments and inserts them into the dictionary with
      normalized keys.
    """

    def __init__(self, **kwargs):
        """
        Initializes the dictionary using keyword arguments. Each provided key is
        normalized before insertion.

        Inputs:
          kwargs (dict): Key-value pairs to be inserted at creation time.

        Returns:
          A new CIDict instance with case-insensitive key handling.
        """
        super().__init__()
        for k, v in dict(**kwargs).items():
            self[k] = v

    def __setitem__(self, key, value):
        """
        Overrides dictionary assignment to normalize string keys to lower case.

        Inputs:
          key (any): The key to insert or update. If the key is a string, it is
            converted to lower case.
          value (any): The value to be associated with the processed key.

        Returns:
          None.
        """
        key = key.lower() if isinstance(key,str) else key
        super().__setitem__(key,value)

    def __getitem__(self, item):
        """
        Retrieves a value from the dictionary using a case-insensitive lookup
        when the key is a string.

        Inputs:
          item (any): The key to retrieve. String keys are normalized to lower
            case before lookup.

        Returns:
          The value associated with the normalized key.

        Error Handling:
          Raises KeyError if the key (after normalization) does not exist.
        """
        item = item.lower() if isinstance(item, str) else item
        return super().__getitem__(item)

    def __delitem__(self, key):
        """
        Deletes an entry from the dictionary using a case-insensitive key match.

        Inputs:
          key (any): The key to delete. If it is a string, it is normalized to
            lower case.

        Returns:
          None.

        Error Handling:
          Raises KeyError if the normalized key is not present.
        """
        key = key.lower() if isinstance(key, str) else key
        super().__delitem__(key)

    def update_all(self, fun):
        """
        Applies a transformation function to all values in the dictionary.
        Each value is replaced with the result of calling fun(v).

        Inputs:
          fun (callable): A function applied to every value in the dictionary.

        Returns:
          None.

        Behavior:
          The dictionary is updated in place. Keys remain unchanged.
        """
        for k, v in self.items():
            self[k] = fun(v)
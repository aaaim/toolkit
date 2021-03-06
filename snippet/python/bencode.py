#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def decode(data):
    def _decode(data):
        dt = data[0]
        if dt == "i":
            data = data[1:]
            integer, _, data = data.partition("e")
            return (int(integer), data)
        elif dt == "l":
            data = data[1:]
            blist = []
            while True:
                dt = data[0]
                if dt == "e":
                    return (blist, data[1:])
                else:
                    item, data = _decode(data)
                    blist.append(item)
        elif dt == "d":
            data = data[1:]
            bdict = {}
            key = None
            while True:
                dt = data[0]
                if dt == "e":
                    return (bdict, data[1:])
                else:
                    key_value, data = _decode(data)
                    if key:
                        bdict[key] = key_value
                        key = None
                    else:
                        key = key_value
        else:
            length, _, data = data.partition(":")
            length = int(length)
            return (data[:length], data[length:])

    return _decode(data)[0]




def encode(data):
    if isinstance(data, str):
        return "{}:{}".format(len(data), data)
    elif isinstance(data, int):
        return "i{}e".format(data)
    elif isinstance(data, list):
        return "l{}e".format("".join(encode(item) for item in data))
    elif isinstance(data, dict):
        result = []
        for key, val in data.items():
            result.extend( (encode(key), encode(val)) )
        return "d{}e".format("".join(result))
    else:
        raise Exception("unsupported type {}".format(type(data)))




if __name__ == '__main__':
    test_cases = [
        ("10:helloworld", "helloworld"),
        ("12:0.0.0.0:3000", "0.0.0.0:3000"),

        ("i0e", 0),
        ("i42e", 42),
        ("i-42e", -42),

        ("l5:helloi42ee", ["hello", 42]),
        ("l5:helloi42eli-1ei0ei1ei2ei3e4:fouree", ['hello', 42, [-1, 0, 1, 2, 3, 'four']]),
        ("lllleeee", [[[[]]]]),
        ("llelelelleee", [[], [], [], [[]]]),
        ("ldededee", [{}, {}, {}]),

        ("de", {}),
        ("lld9:favoritesleeei500ee", [[{"favorites": []}], 500]),
        ("d3:agei100ee", {"age": 100}),
        ("d4:name8:the dudee", {"name": "the dude"}),
    ]
    for case in test_cases:
        assert decode(case[0]) == case[1]
        assert encode(case[1]) == case[0]

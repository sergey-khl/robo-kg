import pandas as pd
from text_to_uri import standardized_uri
import numpy as np


def get_vec_for_window(df, query):
    vecs = []

    query = query.split()

    prev_idx = 0
    prev_match = None
    curr_idx = 0
    while curr_idx < len(query):
        uri = standardized_uri('en', "-".join(query[prev_idx:curr_idx+1]))
        if uri in df.index:
            prev_match = uri
            curr_idx += 1
            if curr_idx != len(query):
                continue

        
        if prev_match is not None:
            print(f"matched {prev_match}")
            vecs.append(df.loc[prev_match].values)
            prev_match = None
            prev_idx = curr_idx

    return vecs


def main():
    query = "prepare me a fruit salad"


    # these are the behaviour tree which represent full tasks
    tasks = {
            "stash_fruit": ["robot_pickup_kiwi", "<HOME>", "item_drop_box", "<HOME>", "robot_pickup_strawberry", "<HOME>", "item_drop_box"]
            }

    df = pd.read_hdf('mini.h5')
    whitelist_english = df.index.str.startswith('/c/en') # for our use case we only care about english
    df = df[whitelist_english]

    query_vecs = get_vec_for_window(df, query)
    print(query_vecs)

if __name__ == "__main__":
    main()

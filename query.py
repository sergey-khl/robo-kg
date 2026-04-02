import pandas as pd
from text_to_uri import standardized_uri
import numpy as np


def get_vecs_and_count_for_query(df, query):
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
            vec = df.loc[prev_match].values
            normalized_vec = vec / np.linalg.norm(vec)
            vecs.append(normalized_vec)
            prev_match = None
            prev_idx = curr_idx

    return vecs, len(vecs)

def get_vecs_and_count_for_task(df, skills):
    filtered_skills = [skill for skill in skills if skill != "<HOME>"]
    skills_to_find_uris_for = [
        word 
        for skill in filtered_skills 
        for word in skill.split("_")
    ]
    uris = [standardized_uri('en', skill) for skill in skills_to_find_uris_for]
    vecs = [df.loc[uri].values for uri in uris if uri in df.index]
    
    normalized_vecs = [vec / np.linalg.norm(vec) for vec in vecs]

    return normalized_vecs, len(vecs)


def find_task_similarity(query_vecs, task_vecs, normalizer):
    sim = 0
    for qvec in query_vecs:
        for tvec in task_vecs:
            sim += np.dot(qvec, tvec)

    return sim / normalizer

# NOTE: we are always working with normalized embeddings so dot product is always cos sim
def main():
    query = "prepare me a fruit salad"
    # query = "lighting never strikes twice"
    # query = "make me fruit, robot!"


    # these are the behaviour trees which represent full tasks
    tasks = {
            "making_a_fruit_salad": ["robot_pickup_kiwi", "<HOME>", "item_drop_box", "<HOME>", "robot_pickup_strawberry", "<HOME>", "item_drop_box"],
            "do_dishes": ["robot_pickup_cup", "<HOME>", "cup_place_dishwasher"],
            "detonate_building": ["push_button"],
            "start_car": ["push_button"],
            "dust_the_furniture": ["robot_pickup_duster", "<HOME>", "duster_clean_photo", "<HOME>", "duster_clean_countertop", "<HOME>", "robot_putaway_duster"],
            "🍞_🎥": ["🤖_pickup_🎥", "<HOME>", "🎥_capture_🍞", "<HOME>", "🤖_putaway_🎥"],
            }

    df = pd.read_hdf('mini.h5')
    whitelist_english = df.index.str.startswith('/c/en') # for our use case we only care about english
    whitelist_emojis = df.index.str.startswith('/c/mul') # and emojis
    df = df[whitelist_english]

    query_vecs, query_count = get_vecs_and_count_for_query(df, query)
    task_sim = {}
    for task, skills in tasks.items():
        task_vecs, task_count = get_vecs_and_count_for_task(df, skills) 

        sim = find_task_similarity(query_vecs, task_vecs, query_count*task_count)

        task_sim[task] = sim

    print(task_sim)

    winner = max(task_sim, key=task_sim.get)

    print(f"The winning task is {winner} with a value of {task_sim[winner]}")


if __name__ == "__main__":
    main()

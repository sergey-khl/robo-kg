import pandas as pd
from text_to_uri import standardized_uri
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# this does fancy window slider which we use for our query and task name
def window_parse(df, words):
    vecs = []

    words = words.split()

    prev_idx = 0
    prev_match = None
    curr_idx = 0
    while curr_idx < len(words):
        uri = standardized_uri('en', "-".join(words[prev_idx:curr_idx+1]))
        if uri in df.index:
            prev_match = uri
            curr_idx += 1
            if curr_idx != len(words):
                continue

        
        if prev_match is not None:
            print(f"matched {prev_match}")
            vec = df.loc[prev_match].values
            normalized_vec = vec / np.linalg.norm(vec)
            vecs.append(normalized_vec)
            prev_match = None
            prev_idx = curr_idx
        else:
            # skip word if not in kg
            curr_idx += 1
            prev_idx = curr_idx

    return vecs, len(vecs)

# this assumes each word in all our skills are part of the conceptnet graph
def regular_parse(df, skills):
    filtered_skills = [skill for skill in skills if skill != "<HOME>"]
    skills_to_find_uris_for = [
        word 
        for skill in filtered_skills 
        for word in skill.split("_")
    ]
    uris = [standardized_uri('en', skill) for skill in skills_to_find_uris_for]

    print(f"matched skills: {uris}")

    vecs = [df.loc[uri].values for uri in uris if uri in df.index]
    
    normalized_vecs = [vec / np.linalg.norm(vec) for vec in vecs]

    return normalized_vecs, len(vecs)


# NOTE: we are always working with normalized embeddings so dot product is always cos sim
def find_task_similarity(query_vecs, task_vecs, normalizer):
    sim = 0
    for qvec in query_vecs:
        for tvec in task_vecs:
            sim += np.dot(qvec, tvec)

    return sim / normalizer

def main():
    # these are the behaviour trees which represent full tasks
    tasks = {
            "making a fruit salad": ["robot_pickup_kiwi", "<HOME>", "item_drop_box", "<HOME>", "robot_pickup_strawberry", "<HOME>", "item_drop_box"],
            "do dishes": ["robot_pickup_cup", "<HOME>", "cup_place_dishwasher"],
            "detonate building": ["push_button"],
            "start car": ["push_button"],
            "dust the furniture": ["robot_pickup_duster", "<HOME>", "duster_clean_photo", "<HOME>", "duster_clean_countertop", "<HOME>", "robot_putaway_duster"],
            "film bread": ["robot_pickup_camera", "<HOME>", "camera_capture_bread", "<HOME>", "robot_putaway_camera"],
            "water plant": ["robot_pickup_bottle", "<HOME>", "bottle_pour_plant", "<HOME>", "robot_putaway_bottle"],
            "knee surgery": ["robot_pickup_scalpel", "<HOME>", "scalpel_cut_knee", "<HOME>", "robot_putaway_scalpel", "<HOME>", "robot_fix_knee"],
            "start fire": ["robot_pickup_wood", "<HOME>", "wood_place_camp", "<HOME>", "robot_pickup_kindling", "<HOME>", "robot_place_camp", "<HOME>", "robot_pickup_lighter", "<HOME>", "ligher_light_kindling"],
            "fix pants": ["robot_pickup_needle", "<HOME>", "needle_sow_pants"],
            }

    df = pd.read_hdf('mini.h5')
    whitelist_english = df.index.str.startswith('/c/en') # for our use case we only care about english
    df = df[whitelist_english]

    task_data = {}
    for title, skills in tasks.items():
        skill_vecs, skill_count = regular_parse(df, skills) 
        title_vecs, title_count = window_parse(df, title) 

        task_vecs = [*skill_vecs, *title_vecs]
        task_count = skill_count + title_count
        print("counts ", title_count, skill_count)
        
        task_data[title] = {
            'vecs': task_vecs,
            'count': task_count
        }

    query_df = pd.read_csv("kg_experiment.csv")

    y_true = []
    y_pred = []

    for _, row in query_df.iterrows():
        query = row['query']
        actual_task = row['task']
        
        query_vecs, query_count = window_parse(df, query)

        task_sim = {}
        for title, data in task_data.items():
            task_vecs = data['vecs']
            task_count = data['count']

            sim = find_task_similarity(query_vecs, task_vecs, query_count * task_count)
            task_sim[title] = sim

        winner = max(task_sim, key=task_sim.get)

        y_pred.append(winner)
        y_true.append(actual_task)
            

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")
    print(f"acc: {accuracy}, f1: {f1}")


if __name__ == "__main__":
    main()

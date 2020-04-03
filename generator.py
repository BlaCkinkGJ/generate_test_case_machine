#!/usr/bin/python3
from faker import Faker
import time
import random
from tqdm import tqdm
import pprint

NR_TEST_CASE = int(1e5)
INSERT = 0
REMOVE = 1
UPDATE = 2
SEARCH = 3

MAX_NR_ENTRY = 100000

SEARCH_DOMINANT = [INSERT, REMOVE] + [SEARCH for _ in range(8)]
REMOVE_DOMINANT = [INSERT, SEARCH] + [REMOVE for _ in range(8)]
INSERT_DOMINANT = [REMOVE, SEARCH] + [INSERT for _ in range(8)]
UNIFORM_DISTRIB = [INSERT, REMOVE, SEARCH]

COMMAND_LIST = UNIFORM_DISTRIB

# per char [] > 64
if __name__ == "__main__":
    # fake = Faker(['ko_KR'])
    pbar = tqdm(total=NR_TEST_CASE)

    fake = Faker()
    seed_value = time.time() * 1e6

    Faker.seed(seed_value)  # seed value
    random.seed(seed_value)  # seed value

    id_set = set()
    idx = 0

    test_file = open("test.inp", "w")
    test_file.write("{}\n".format(NR_TEST_CASE))  # N value

    state = (random.sample(COMMAND_LIST, 1))[0]

    nr_insert = 0
    nr_remove = 0
    nr_update = 0
    nr_search = 0

    while idx < NR_TEST_CASE:

        if state == REMOVE:
            if len(id_set) <= 0:
                state = INSERT
                continue
            student_id = (random.sample(id_set, 1))[0]
            test_file.write("REMOVE,{}\n".format(student_id))
            id_set.remove(student_id)
            nr_remove += 1

        elif state == UPDATE:
            if len(id_set) <= 0:
                state = INSERT
                continue

            student_id = (random.sample(id_set, 1))[0]
            name = fake.first_name()
            bban = fake.bban()
            email = fake.email()

            test_file.write(
                "UPDATE,{},{},{},{}\n".format(
                    student_id, fake.first_name(), fake.bban(), fake.ascii_email(),
                )
            )
            nr_update += 1

        elif state == SEARCH:
            if len(id_set) <= 0:
                state = INSERT
                continue
            student_id = (random.sample(id_set, 1))[0]
            test_file.write("SEARCH,{}\n".format(student_id))
            nr_search += 1

        elif state == INSERT:

            student_id = random.randint(202000000, 202099999)
            if (student_id in id_set) or len(id_set) > MAX_NR_ENTRY:
                state = (
                    random.sample(
                        [_command for _command in COMMAND_LIST if _command != INSERT], 1
                    )
                )[0]
                continue
            id_set.add(student_id)

            name = fake.first_name()
            bban = fake.bban()
            email = fake.email()

            test_file.write(
                "INSERT,{},{},{},{}\n".format(student_id, name, bban, email)
            )
            nr_insert += 1

        idx += 1
        pbar.update(1)
        state = (random.sample(COMMAND_LIST, 1))[0]

    pbar.close()

    test_file.close()

    nr_total = (nr_insert + nr_update + nr_remove + nr_search) / 100.0
    print(
        "insert: {}%,search: {}%,update: {}%,remove: {}%".format(
            nr_insert / nr_total,
            nr_search / nr_total,
            nr_update / nr_total,
            nr_remove / nr_total,
        )
    )

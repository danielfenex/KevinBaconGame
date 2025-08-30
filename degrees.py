import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

# loads data into names, people, movies
def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    # ?
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # get id for sourcename
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    # get id for targetname
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    #currently returns distance only

    # input : source and target are both type person_id
    # output : distance of shortest path, list of (actor, movie) pairs on path
    # create a queue 'visited'
    # source is the id of input name 1
    # target is the id of input name 2
    # declare a QueueFrontier object
    frontier = QueueFrontier()
    # create a node using source and add it to frontier
    source_node = Node(state=source, parent=0)
    frontier.add(source_node)
    # variables to track which nodes have already been visited and the distance of nodes away from source
    visited = []
    distance = 1

    # base case, source and target are in the same movie
    for (m,p) in neighbors_for_person(source):
        if(p==target): return 0

    # while loop to go through nodes recursively
    while(frontier.empty() != True):
        # pop the next node from the frontier
        current_node = frontier.remove()
        # add the next node to visited
        visited.append(current_node)
        # get list of all pairs (movie_id, person_id) such that
        # movie_id is a movie that current_node.state starred in
        # and person_id is another person in that movie
        next_nodes = neighbors_for_person(current_node.state)
        for (m,p) in next_nodes:
            for i in visited:
                if(p != i):
                    if (p == target):
                        return distance
                    frontier.add(p)
        distance += 1
    return 0
        
        

    # TODO
    raise NotImplementedError
    
    

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

# use small and 'check50' for testing
# check for goal node when addd
if __name__ == "__main__":
    main()

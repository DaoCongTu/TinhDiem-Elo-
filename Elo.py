class Club(object):
    def __init__(self, name, points=1000):
        self.name = name
        self.points = points

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.points > other.points

    def compute_points(self, opponent, is_home, result):
        rating_diff = self.points - opponent.points + (100 if is_home else -100)
        expected = 1 / (1 + 10 ** (-rating_diff / 400))
        return 32 * (result - expected)


def play_match(home, away, result):
    home_change = int(home.compute_points(away, True, result))
    away_change = int(away.compute_points(home, False, 1 - result))
    home.points += home_change
    away.points += away_change


def club_index(club_to_find, clubs):
    index = 0
    while index < len(clubs):
        club = clubs[index]
        if club.name == club_to_find:
            return index
        index += 1
    return -1


def main():
    clubs = []
    with open("C:/Users\Administrator\PycharmProjects\pythonProject\matches") as file:
        matches = file.readlines()

    for match in matches:
        (home_str, away_str, result) = match.split(" ")

        index = club_index(home_str, clubs)
        if index == -1:
            home = Club(home_str)
            clubs.append(home)
        else:
            home = clubs[index]

        index = club_index(away_str, clubs)
        if index == -1:
            away = Club(away_str)
            clubs.append(away)
        else:
            away = clubs[index]

        play_match(home, away, float(result))

    clubs = sorted(clubs)
    clubs.reverse()
    with open("ranking.txt", "w") as file:
        for club in clubs:
            file.write(club.name + ": " + str(club.points) + "\n")


if __name__ == "__main__":
    main()
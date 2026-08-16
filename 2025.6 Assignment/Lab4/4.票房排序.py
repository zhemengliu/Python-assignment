movies = [
    ("《哪吒之魔童降世》", 49.34),
    ("《疯狂的外星人》", 21.83),
    ("《流浪地球》", 46.18),
    ("《我和我的祖国》", 29.64),
    ("《烈火英雄》", 16.76),
    ("《中国机长》", 28.46)
]

sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)

for movie in sorted_movies:
    print(f"{movie[0]}，票房：{movie[1]}亿")

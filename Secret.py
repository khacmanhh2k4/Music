import os

print("---------Menu--------")
print('1. Music Anime')
print('2. Music Game')

n = int(input("Hôm nay tâm trạng của bạn thế nào: "))
if(n == 1):
    open('MyFavoriteMusicAnime.txt')
    os.system('notepad MyFavoriteMusicAnime.txt')
if(n==2):
    open("MusicGame.txt")
else:
    exit
#!/usr/bin/env python3
"""
Create a comprehensive movie dataset with genres quickly
"""

import pandas as pd
import os

# Comprehensive movie list with genres
movies_data = [
    # Action
    {'title': 'Die Hard', 'genres': 'Action, Thriller', 'vote_average': 8.5, 'release_date': '1988-07-15', 'popularity': 85.5, 'overview': 'An off-duty cop must save his wife and fellow hostages from a group of terrorists.'},
    {'title': 'The Dark Knight', 'genres': 'Action, Crime, Drama', 'vote_average': 9.0, 'release_date': '2008-07-18', 'popularity': 90.0, 'overview': 'Batman faces against a criminal mastermind.'},
    {'title': 'Mission Impossible', 'genres': 'Action, Adventure, Thriller', 'vote_average': 7.2, 'release_date': '1996-05-22', 'popularity': 72.0, 'overview': 'An American agent goes undercover.'},
    {'title': 'John Wick', 'genres': 'Action, Crime, Drama', 'vote_average': 7.4, 'release_date': '2014-10-24', 'popularity': 75.0, 'overview': 'A retired hitman comes out of retirement.'},
    {'title': 'Mad Max Fury Road', 'genres': 'Action, Adventure, Sci-Fi', 'vote_average': 8.1, 'release_date': '2015-05-15', 'popularity': 80.0, 'overview': 'Post-apocalyptic wasteland action.'},
    {'title': 'The Matrix', 'genres': 'Action, Sci-Fi', 'vote_average': 8.7, 'release_date': '1999-03-31', 'popularity': 87.0, 'overview': 'A computer programmer discovers reality.'},
    {'title': 'Terminator 2', 'genres': 'Action, Sci-Fi', 'vote_average': 8.5, 'release_date': '1991-07-03', 'popularity': 82.0, 'overview': 'A terminator sent back to protect a boy.'},
    {'title': 'Fast and Furious 7', 'genres': 'Action, Crime, Drama', 'vote_average': 7.1, 'release_date': '2015-04-03', 'popularity': 78.0, 'overview': 'The crew faces off against a powerful force.'},
    {'title': 'Raid 2 Berendal', 'genres': 'Action, Crime, Drama', 'vote_average': 8.0, 'release_date': '2014-03-28', 'popularity': 76.0, 'overview': 'Indonesian action masterpiece.'},
    {'title': 'Kingsman The Secret Service', 'genres': 'Action, Adventure, Comedy', 'vote_average': 7.7, 'release_date': '2014-10-24', 'popularity': 77.0, 'overview': 'A stylish secret agent recruits a street orphan.'},
    
    # Sci-Fi
    {'title': 'Inception', 'genres': 'Action, Sci-Fi, Thriller', 'vote_average': 8.8, 'release_date': '2010-07-16', 'popularity': 88.0, 'overview': 'A thief who steals corporate secrets through dreams.'},
    {'title': 'Interstellar', 'genres': 'Adventure, Drama, Sci-Fi', 'vote_average': 8.6, 'release_date': '2014-11-07', 'popularity': 86.0, 'overview': 'Explorers travel through a wormhole in space.'},
    {'title': 'The Martian', 'genres': 'Adventure, Drama, Sci-Fi', 'vote_average': 8.0, 'release_date': '2015-10-02', 'popularity': 80.0, 'overview': 'An astronaut must survive on Mars.'},
    {'title': 'Blade Runner 2049', 'genres': 'Drama, Mystery, Sci-Fi', 'vote_average': 8.0, 'release_date': '2017-10-06', 'popularity': 79.0, 'overview': 'A cop uncovers a secret in Los Angeles.'},
    {'title': 'Back to the Future', 'genres': 'Adventure, Comedy, Sci-Fi', 'vote_average': 8.5, 'release_date': '1985-07-03', 'popularity': 85.0, 'overview': 'Time travel adventure to the past.'},
    {'title': 'Avatar', 'genres': 'Action, Adventure, Fantasy, Sci-Fi', 'vote_average': 7.8, 'release_date': '2009-12-18', 'popularity': 78.0, 'overview': 'A paraplegic marine travels to an alien moon.'},
    {'title': 'Gravity', 'genres': 'Adventure, Drama, Sci-Fi, Thriller', 'vote_average': 7.7, 'release_date': '2013-10-04', 'popularity': 77.0, 'overview': 'Two astronauts must return to Earth.'},
    {'title': 'Tenet', 'genres': 'Action, Sci-Fi, Thriller', 'vote_average': 6.8, 'release_date': '2020-09-03', 'popularity': 68.0, 'overview': 'Temporal inversion espionage thriller.'},
    {'title': 'Dune', 'genres': 'Action, Adventure, Drama, Sci-Fi', 'vote_average': 8.0, 'release_date': '2021-10-22', 'popularity': 80.0, 'overview': 'Epic adaptation of Frank Herbert novel.'},
    {'title': 'Ready Player One', 'genres': 'Action, Adventure, Sci-Fi', 'vote_average': 7.2, 'release_date': '2018-03-29', 'popularity': 72.0, 'overview': 'Virtual reality adventure in a dystopian future.'},
    
    # Drama
    {'title': 'The Shawshank Redemption', 'genres': 'Drama', 'vote_average': 9.3, 'release_date': '1994-10-14', 'popularity': 93.0, 'overview': 'Two imprisoned men bond over years.'},
    {'title': 'Forrest Gump', 'genres': 'Drama, Romance', 'vote_average': 8.8, 'release_date': '1994-07-06', 'popularity': 88.0, 'overview': 'A man with low IQ changes America.'},
    {'title': 'The Godfather', 'genres': 'Crime, Drama', 'vote_average': 9.2, 'release_date': '1972-03-24', 'popularity': 92.0, 'overview': 'The aging patriarch of crime dynasty transfers control.'},
    {'title': 'The Godfather Part II', 'genres': 'Crime, Drama', 'vote_average': 9.0, 'release_date': '1974-12-20', 'popularity': 90.0, 'overview': 'The story of the Corleone family continues.'},
    {'title': 'Pulp Fiction', 'genres': 'Crime, Drama', 'vote_average': 8.9, 'release_date': '1994-10-14', 'popularity': 89.0, 'overview': 'The lives of two mob hitmen, a boxer, and a pair of diner bandits.'},
    {'title': 'Life is Beautiful', 'genres': 'Comedy, Drama, Family', 'vote_average': 8.6, 'release_date': '1997-12-20', 'popularity': 86.0, 'overview': 'A father uses imagination to shield his son from war.'},
    {'title': 'The Pursuit of Happiness', 'genres': 'Biography, Drama', 'vote_average': 8.2, 'release_date': '2006-12-15', 'popularity': 82.0, 'overview': 'A father and son try to survive homelessness.'},
    {'title': 'Schindlers List', 'genres': 'Biography, Drama, History', 'vote_average': 9.0, 'release_date': '1993-11-30', 'popularity': 90.0, 'overview': 'An industrialist saves his workers during the Holocaust.'},
    {'title': 'The Sum of All Fears', 'genres': 'Drama, Thriller', 'vote_average': 6.5, 'release_date': '2002-05-02', 'popularity': 65.0, 'overview': 'A CIA analyst uncovers a nuclear conspiracy.'},
    {'title': 'Gladiator', 'genres': 'Action, Adventure, Drama', 'vote_average': 8.5, 'release_date': '2000-05-05', 'popularity': 85.0, 'overview': 'A former Roman slavery fights in the arena.'},
    
    # Comedy
    {'title': 'Forrest Gump', 'genres': 'Comedy, Drama, Romance', 'vote_average': 8.8, 'release_date': '1994-07-06', 'popularity': 88.0, 'overview': 'A man with low IQ changes America.'},
    {'title': 'The Great Dictator', 'genres': 'Comedy, Drama, War', 'vote_average': 8.5, 'release_date': '1940-10-15', 'popularity': 85.0, 'overview': 'A Jewish barber is mistaken for a dictator.'},
    {'title': 'Singin in the Rain', 'genres': 'Comedy, Musical, Romance', 'vote_average': 8.3, 'release_date': '1952-03-27', 'popularity': 83.0, 'overview': 'Hollywood musical about silent films.'},
    {'title': 'Sunset Boulevard', 'genres': 'Comedy, Drama, Film-Noir', 'vote_average': 8.4, 'release_date': '1950-08-10', 'popularity': 84.0, 'overview': 'A failed writer seduced by a faded film star.'},
    {'title': 'Citizen Kane', 'genres': 'Comedy, Drama, Mystery', 'vote_average': 8.3, 'release_date': '1941-05-01', 'popularity': 83.0, 'overview': 'The story of a newspaper magnate.'},
    {'title': 'Parasite', 'genres': 'Comedy, Drama, Thriller', 'vote_average': 8.6, 'release_date': '2019-05-30', 'popularity': 86.0, 'overview': 'A poor family schemes their way into wealth.'},
    {'title': 'The Grand Budapest Hotel', 'genres': 'Adventure, Comedy, Crime', 'vote_average': 8.1, 'release_date': '2014-03-28', 'popularity': 81.0, 'overview': 'A writer visits a legendary concierge.'},
    {'title': 'Jojo Rabbit', 'genres': 'Comedy, Drama, War', 'vote_average': 7.9, 'release_date': '2019-10-18', 'popularity': 79.0, 'overview': 'A boy with an imaginary Führer experiences friendship.'},
    {'title': 'The Gentlemen', 'genres': 'Action, Comedy, Crime', 'vote_average': 8.0, 'release_date': '2019-12-25', 'popularity': 80.0, 'overview': 'An American expat drug lord tries to escape.'},
    {'title': 'Knives Out', 'genres': 'Comedy, Crime, Drama', 'vote_average': 7.9, 'release_date': '2019-11-27', 'popularity': 79.0, 'overview': 'A detective investigates a familys secrets.'},
    
    # Horror
    {'title': 'The Shining', 'genres': 'Drama, Horror', 'vote_average': 8.4, 'release_date': '1980-05-23', 'popularity': 84.0, 'overview': 'A family isolated at a haunted hotel.'},
    {'title': 'The Exorcist', 'genres': 'Horror', 'vote_average': 8.1, 'release_date': '1973-12-26', 'popularity': 81.0, 'overview': 'A possessed girl needs an exorcist.'},
    {'title': 'Hereditary', 'genres': 'Drama, Horror, Mystery', 'vote_average': 7.6, 'release_date': '2018-06-08', 'popularity': 76.0, 'overview': 'A family is haunted by mysterious forces.'},
    {'title': 'A Quiet Place', 'genres': 'Drama, Horror, Sci-Fi', 'vote_average': 7.5, 'release_date': '2018-04-06', 'popularity': 75.0, 'overview': 'A family must live in silence to survive.'},
    {'title': 'Get Out', 'genres': 'Horror, Mystery, Thriller', 'vote_average': 7.7, 'release_date': '2017-02-24', 'popularity': 77.0, 'overview': 'A man visits his girlfriends family estate.'},
    {'title': 'It Follows', 'genres': 'Horror, Mystery', 'vote_average': 6.8, 'release_date': '2014-03-27', 'popularity': 68.0, 'overview': 'A supernatural entity follows its prey.'},
    {'title': 'The Ring', 'genres': 'Horror, Mystery', 'vote_average': 7.1, 'release_date': '2002-10-18', 'popularity': 71.0, 'overview': 'Watching a tape leads to death.'},
    {'title': 'Insidious', 'genres': 'Horror, Mystery, Thriller', 'vote_average': 6.8, 'release_date': '2010-09-01', 'popularity': 68.0, 'overview': 'A family struggles with a supernatural haunting.'},
    {'title': 'The Conjuring', 'genres': 'Horror, Mystery, Thriller', 'vote_average': 7.5, 'release_date': '2013-07-19', 'popularity': 75.0, 'overview': 'Paranormal investigators help a haunted family.'},
    {'title': 'Sinister', 'genres': 'Crime, Drama, Horror', 'vote_average': 7.6, 'release_date': '2012-10-05', 'popularity': 76.0, 'overview': 'A writer discovers a dark family secret.'},
    
    # Romance
    {'title': 'The Notebook', 'genres': 'Drama, Romance', 'vote_average': 7.8, 'release_date': '2004-06-25', 'popularity': 78.0, 'overview': 'A poor yet passionate man falls in love.'},
    {'title': 'Titanic', 'genres': 'Drama, Romance', 'vote_average': 7.8, 'release_date': '1997-12-19', 'popularity': 78.0, 'overview': 'Two passengers meet on the Titanic.'},
    {'title': 'Pride and Prejudice', 'genres': 'Drama, Romance', 'vote_average': 7.6, 'release_date': '2005-09-23', 'popularity': 76.0, 'overview': 'Elizabeth and Darcy navigate love and society.'},
    {'title': 'La La Land', 'genres': 'Drama, Musical, Romance', 'vote_average': 8.0, 'release_date': '2016-12-09', 'popularity': 80.0, 'overview': 'Two artists fall in love in Los Angeles.'},
    {'title': 'Crazy, Stupid, Love', 'genres': 'Comedy, Drama, Romance', 'vote_average': 7.6, 'release_date': '2011-06-24', 'popularity': 76.0, 'overview': 'Romantic and comedic entanglements.'},
    {'title': 'The Fault in Our Stars', 'genres': 'Drama, Romance', 'vote_average': 7.8, 'release_date': '2014-06-06', 'popularity': 78.0, 'overview': 'Two teenagers with cancer fall in love.'},
    {'title': 'About Time', 'genres': 'Comedy, Drama, Fantasy, Romance', 'vote_average': 7.8, 'release_date': '2013-09-04', 'popularity': 78.0, 'overview': 'A man uses time travel to improve his life.'},
    {'title': 'The Vow', 'genres': 'Drama, Romance', 'vote_average': 6.8, 'release_date': '2012-02-10', 'popularity': 68.0, 'overview': 'After a car accident, a woman loses her memory.'},
    {'title': 'Romeo and Juliet', 'genres': 'Drama, Romance', 'vote_average': 6.8, 'release_date': '1996-11-01', 'popularity': 68.0, 'overview': 'The classic Shakespearean tragedy.'},
    {'title': 'Atonement', 'genres': 'Drama, Romance, War', 'vote_average': 7.1, 'release_date': '2007-09-14', 'popularity': 71.0, 'overview': 'A false accusation ruins young love.'},
    
    # Thriller
    {'title': 'The Silence of the Lambs', 'genres': 'Crime, Drama, Thriller', 'vote_average': 8.6, 'release_date': '1991-02-14', 'popularity': 86.0, 'overview': 'An FBI trainee seeks help from a serial killer.'},
    {'title': 'Se7en', 'genres': 'Crime, Drama, Mystery, Thriller', 'vote_average': 8.6, 'release_date': '1995-09-22', 'popularity': 86.0, 'overview': 'Two detectives hunt a serial killer.'},
    {'title': 'Psycho', 'genres': 'Horror, Thriller', 'vote_average': 8.5, 'release_date': '1960-12-08', 'popularity': 85.0, 'overview': 'A woman checks into a sinister motel.'},
    {'title': 'The Sting', 'genres': 'Comedy, Crime, Drama', 'vote_average': 8.3, 'release_date': '1973-12-25', 'popularity': 83.0, 'overview': 'Two con artists plan an elaborate scheme.'},
    {'title': 'Rear Window', 'genres': 'Mystery, Thriller', 'vote_average': 8.4, 'release_date': '1954-08-01', 'popularity': 84.0, 'overview': 'A man spies on neighbors from his window.'},
    {'title': 'Vertigo', 'genres': 'Mystery, Romance, Thriller', 'vote_average': 8.3, 'release_date': '1958-05-09', 'popularity': 83.0, 'overview': 'A detective with acrophobia investigates a mystery.'},
    {'title': 'No Country for Old Men', 'genres': 'Crime, Drama, Thriller', 'vote_average': 8.1, 'release_date': '2007-11-21', 'popularity': 81.0, 'overview': 'A hunter discovers drug cartel money.'},
    {'title': 'The Prestige', 'genres': 'Drama, Mystery, Sci-Fi, Thriller', 'vote_average': 8.5, 'release_date': '2006-10-20', 'popularity': 85.0, 'overview': 'Two magicians engage in a rivalry.'},
    {'title': 'Zodiac', 'genres': 'Crime, Drama, Mystery', 'vote_average': 7.9, 'release_date': '2007-05-25', 'popularity': 79.0, 'overview': 'The hunt for the Zodiac Killer.'},
    {'title': 'Mindhunters', 'genres': 'Crime, Drama, Mystery, Thriller', 'vote_average': 7.6, 'release_date': '2004-05-14', 'popularity': 76.0, 'overview': 'A group of profilers hunt serial killers.'},
]

# Create DataFrame
df = pd.DataFrame(movies_data)

# Save to CSV
df.to_csv('enhanced_movies.csv', index=False)
print(f"✅ Created enhanced_movies.csv with {len(df)} movies")
print(f"Genres available: {df['genres'].nunique()} unique genre combinations")
print(f"Sample genres: {df['genres'].unique()[:5]}")


import math
import Ant
import colony
import graph
import numpy as np
import pandas as pd
import operator
import matplotlib.pyplot as plt
num_of_iter = 400
num_of_ants = 20

the_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'] #the features that we looking at for smoothness
features_importancy = np.array([2, 2, 1, 1, 1, 1, 1, 2, 4])  # the importance of each feature


def main():

    df = pd.read_csv('./data/genres_v2.csv', dtype={"song_name": "string"})
    song_names = ['Everlong', 'Miss Murder', 'A$AP Forever (feat. Moby)', 'In Da Club', 'All About That Bass', 'P.I.M.P.', 'Ms. Jackson', 'Hey, Soul Sister', 'Shape of You', 'Viva La Vida', 'In the End', 'Oops!...I Did It Again',  'Get Lucky (feat. Pharrell Williams & Nile Rodgers)', 'I Gotta Feeling', 'Dance Monkey', 'Blinding Lights', 'Candy Shop', 'Rolling In The Deep', 'Stronger (What Doesn\'t Kill You)', 'Party Rock Anthem', 'Faint', 'Thnks fr th Mmrs', 'Bring Me To Life']
    print(f"number of songs in the list: {len(song_names)}")


    print(f"the song playlist: {song_names}")
    songs_features = songlist_to_songfeatures(song_names, df)
    dist_matrix = songs_features_to_dist_matrix(songs_features)

    args = {}
    args['alpha'] = 1. # the pheromones importance wight
    args['beta'] = 2.  # the heuristic ( 1/distance of local edge) importance wight
    args['ro'] = 0.06  # the evaporation rate (smaller number of songs need smaller evaporation rate so the ant wont get stack at the same tour)
    args['q0'] = 0.7  # the exploitation vs exploration parameter (smaller number of songs need smaller exploitation rate so the ant wont get stack at the same tour)

    G = graph.Graph(dist_matrix)
    ant_colony = colony.Colony(num_of_ants, args, G, num_of_iter)
    ant_colony.start_search()
    print(f"Total cost {ant_colony.best_global_path_cost}")
    print(print(f"the song playlist smooth order: {[song_names[i] for i in ant_colony.best_global_path]}"))
    plot(ant_colony.iter_costs)


def songs_distance(song1_features , songs2_features):

    song_dist = np.linalg.norm(features_importancy*(song1_features - songs2_features))
    return song_dist


def songlist_to_songfeatures(song_names, df):

    my_playlist_df = df.head(0)
    for song in song_names:
        fil = df["song_name"] == song
        # filtering data to the wanted features
        my_playlist_df = my_playlist_df.append(df[fil])

    my_playlist_df = my_playlist_df.drop_duplicates(subset=['song_name']) # remove duplicate names
    songs_features = my_playlist_df[the_features]
    songs_features = (songs_features - songs_features.mean()) / songs_features.std() #mean normelizition DF
    songs_features = (songs_features - songs_features.min()) / (songs_features.max() - songs_features.min()) # min-max normalizition DF
    return songs_features*100


def songs_features_to_dist_matrix(song_features): # converting all the songs to distances matrix between songs

    song_features_np = song_features.to_numpy()
    num_of_songs = song_features_np.shape[0]
    dist_matrix = np.zeros(shape=(num_of_songs,num_of_songs))

    for i in range(song_features_np.shape[0]):
        for j in range(song_features_np.shape[0]):

            dist_matrix[i, j] = songs_distance(song_features_np[i],song_features_np[j])

    return dist_matrix


def plot(cost_list):  # plotting the cost of the tour as a function of iteration

    plt.plot([i+1 for i in range(len(cost_list))], cost_list)
    plt.show()


if __name__ == '__main__':
    main()



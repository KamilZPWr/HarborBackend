import pandas as pd

from model import UseEmbedding

DB_PATH = './assets/db.csv'

ID = 'id'
NAME = 'name'
VALUE = 'value'
FEATURES = 'features'
LONGITUDE = 'longitude'
LATITUDE = 'latitude'
FOTO_URL = 'foto_url'
ROOMS_N = 'rooms_n'
SIZE = 'size'
DESC = 'desc'
PRICE = 'price'
REAL_ESTATES = 'real_estates'

tmp_data = pd.read_csv('./assets/features_list.csv')
mapper = {row[1]: row[2] for row in tmp_data.itertuples()}


def read_db():
    real_estates = pd.read_csv(DB_PATH, sep=';')
    return real_estates


def create_response(core_results, additional_features, additional_features_names):
    results = {REAL_ESTATES: []}

    for row in core_results.iterrows():
        parsed_additional_features = []

        for n in range(len(additional_features_names)):
            parsed_additional_features.append({
                VALUE: 0.5,  # additional_features.loc[row[0]][additional_features_names[n]],
                NAME: mapper[additional_features_names[n]]
            })

        row = row[1]
        results[REAL_ESTATES].append({
            ID: row[0],
            PRICE: float(row[1]),
            DESC: row[2],
            SIZE: float(row[3]),
            ROOMS_N: row[4],
            FOTO_URL: row[5],
            LATITUDE: row[6],
            LONGITUDE: row[7],
            FEATURES: parsed_additional_features
        })

    return results


def process(
        text: str, price_max: float, price_min: float,
        size_max: float, size_min: float,
        rooms_n_max: int, rooms_n_min: int
):

    db = read_db()
    ue = UseEmbedding()
    additional_features_names = ue.get_most_important_features(text)

    results = db[
        (
            db[PRICE] <= price_max
        ) & (
            db[PRICE] >= price_min
        ) & (
            db[SIZE] <= size_max
        ) & (
            db[SIZE] >= size_min
        ) & (
            db[ROOMS_N] <= rooms_n_max
        ) & (
            db[ROOMS_N] >= rooms_n_min
        )
    ]

    core_results = results[[ID, PRICE, DESC, SIZE, ROOMS_N, FOTO_URL, LATITUDE, LONGITUDE]]
    additional_features = results[additional_features_names]

    return create_response(core_results, additional_features, additional_features_names)

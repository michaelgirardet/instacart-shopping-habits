"""Construction du jeu de données pour la modélisation.

Principe : pour chaque client, la dernière commande observée sert de cible
et toutes les commandes précédentes servent d'historique. On ne calcule
jamais une feature avec des informations postérieures au point de
prédiction, pour éviter toute fuite de données.
"""

import pandas as pd

# Seuil opérationnel identifié dans l'analyse (Bloc C) : au-delà de 15 jours
# sans commande, le retour devient inhabituel. Il est aussi inférieur au
# plafond de 30 jours du dataset, ce qui évite le problème de censure.
SEUIL_RETOUR_RAPIDE = 15


def build_ml_dataset(df_commandes: pd.DataFrame, seuil: int = SEUIL_RETOUR_RAPIDE) -> pd.DataFrame:
    """Construit une table avec une ligne par client.

    - Les features décrivent l'historique du client (toutes ses commandes
      sauf la dernière) : volume, panier, rythme, réachat.
    - Le label `retour_rapide` vaut 1 si le délai avant sa dernière
      commande est inférieur ou égal au seuil, 0 sinon.
    """
    df = df_commandes.sort_values(["user_id", "order_number"])

    derniere = df.groupby("user_id")["order_number"].transform("max")
    hist = df[df["order_number"] < derniere].copy()
    cible = df[df["order_number"] == derniere]

    # Part des délais >= seuil dans l'historique (les NaN de la première
    # commande sont exclus du calcul).
    delais = hist["days_since_prior_order"]
    hist["delai_long"] = (delais >= seuil).astype(float).mask(delais.isna())

    features = hist.groupby("user_id").agg(
        nb_commandes=("order_number", "max"),
        panier_moyen=("basket_size", "mean"),
        panier_dernier=("basket_size", "last"),
        part_reachat=("reorder_share", "mean"),
        delai_moyen=("days_since_prior_order", "mean"),
        delai_median=("days_since_prior_order", "median"),
        delai_std=("days_since_prior_order", "std"),
        delai_dernier=("days_since_prior_order", "last"),
        part_delais_longs=("delai_long", "mean"),
        heure_moyenne=("order_hour_of_day", "mean"),
    )

    labels = (
        cible.set_index("user_id")["days_since_prior_order"]
        .le(seuil)
        .astype(int)
        .rename("retour_rapide")
    )

    return features.join(labels, how="inner").dropna().reset_index()

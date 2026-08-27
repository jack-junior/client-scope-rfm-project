from pathlib import Path
import argparse

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


VALID_SCALED_COLUMNS = [
	"recence_jours_scaled",
	"frequence_scaled",
	"montant_total_scaled",
]
GLOBAL_SCALED_COLUMNS = [
	"recence_globale_jours_scaled",
	"frequence_globale_scaled",
	"montant_global_scaled",
]


def evaluate_k_values(data, feature_columns, k_values, random_state=42):
	"""Measure inertia and silhouette for several values of k."""
	features = data[feature_columns]
	results = []

	for k in k_values:
		model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
		labels = model.fit_predict(features)
		results.append({
			"k": k,
			"inertie": model.inertia_,
			"silhouette": silhouette_score(features, labels),
		})

	return pd.DataFrame(results)


def fit_segmentation(data, feature_columns, k, random_state=42):
	"""Fit K-means and return a copy of the data with a segment column."""
	model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
	segmented_data = data.copy()
	segmented_data["segment"] = model.fit_predict(data[feature_columns])
	return model, segmented_data


def _top_value(values):
	"""Return the most frequent non-missing value."""
	values = values.dropna()
	return values.mode().iat[0] if not values.empty else "Inconnu"


def _top_values(values, limit=3):
	"""Return the most frequent values as a readable string."""
	values = values.dropna().astype(str)
	return ", ".join(values.value_counts().head(limit).index) or "Inconnu"


def summarize_segments(data, approach):
	"""Create an interpretable summary of each segment."""
	if approach == "valid":
		amount_column = "montant_total"
		recency_column = "recence_jours"
		frequency_column = "frequence"
	elif approach == "global":
		amount_column = "montant_global"
		recency_column = "recence_globale_jours"
		frequency_column = "frequence_globale"
	else:
		raise ValueError("approach doit être 'valid' ou 'global'")

	total_amount = data[amount_column].sum()
	summary = data.groupby("segment").agg(
		effectif=("CustomerID", "size"),
		chiffre_affaires_moyen=(amount_column, "mean"),
		recence_moyenne=(recency_column, "mean"),
		frequence_moyenne=(frequency_column, "mean"),
		montant_moyen=(amount_column, "mean"),
		top_pays=("pays_residence", _top_value),
		top_produit_code=("produit_top_code", _top_value),
		top_produit_description=("produit_top_description", _top_value),
		top_produits=("produit_top_description", _top_values),
	).reset_index()
	summary["part_chiffre_affaires_pct"] = (
		summary["chiffre_affaires_moyen"] * summary["effectif"]
		/ total_amount * 100
	)
	summary = summary.rename(columns={"chiffre_affaires_moyen": "chiffre_affaires_segment"})
	return summary.sort_values("segment").reset_index(drop=True)


def run_segmentation(input_path, output_dir, k_valid, k_global, random_state=42):
	"""Train both approaches and save segmented data and summaries."""
	input_path = Path(input_path)
	output_dir = Path(output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	data = pd.read_csv(input_path)

	approaches = {
		"valid": (VALID_SCALED_COLUMNS, k_valid),
		"global": (GLOBAL_SCALED_COLUMNS, k_global),
	}
	outputs = {}

	for approach, (feature_columns, k) in approaches.items():
		_, segmented_data = fit_segmentation(
			data, feature_columns, k, random_state=random_state
		)
		summary = summarize_segments(segmented_data, approach)
		segmented_data.to_csv(output_dir / f"clients_segmentes_{approach}.csv", index=False)
		summary.to_csv(output_dir / f"resume_segments_{approach}.csv", index=False)
		outputs[approach] = summary

	return outputs


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Segmenter les clients avec K-means.")
	parser.add_argument("--input", default="data/processed/features_rfm_datacsv")
	parser.add_argument("--output-dir", default="outputs")
	parser.add_argument("--k-valid", type=int, default=4)
	parser.add_argument("--k-global", type=int, default=4)
	args = parser.parse_args()

	run_segmentation(
		input_path=args.input,
		output_dir=args.output_dir,
		k_valid=args.k_valid,
		k_global=args.k_global,
	)
	print(f"Résultats sauvegardés dans {args.output_dir}")

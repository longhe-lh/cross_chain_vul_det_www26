import pandas as pd

df = pd.read_csv("prediction_results.csv")

filtered_df = df[df["true_label"] == "Yes"]

filtered_df.to_csv("prediction_results_true_yes.csv", index=False)

print("筛选完成，结果保存在 prediction_results_true_yes.csv")

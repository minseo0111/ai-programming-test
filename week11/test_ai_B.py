import csv

import pytest

from ai_B import read_csv


def test_reads_names_and_numeric_scores_from_csv(tmp_path):
	csv_path = tmp_path / "scores.csv"
	with csv_path.open("w", encoding="utf-8", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["김민수", 85])
		writer.writerow(["Jane Doe", 92])

	result = read_csv(str(csv_path))

	assert result == [("김민수", 85), ("Jane Doe", 92)]
	assert all(isinstance(row, tuple) and len(row) == 2 for row in result)
	assert all(isinstance(score, (int, float)) for _, score in result)


def test_reads_empty_csv_as_empty_list(tmp_path):
	csv_path = tmp_path / "empty.csv"
	csv_path.write_text("", encoding="utf-8")

	assert read_csv(str(csv_path)) == []


def test_missing_csv_raises_file_not_found_error(tmp_path):
	csv_path = tmp_path / "missing.csv"

	with pytest.raises(FileNotFoundError):
		read_csv(str(csv_path))

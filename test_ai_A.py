import pytest

from ai_A import load_scores


def test_load_scores_keeps_valid_rows_and_ignores_header_and_blank_lines(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"name,score\nAlice,90\n\n Bob , 75 \n",
		encoding="utf-8",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Alice", 90), ("Bob", 75)]
	assert skipped == []


@pytest.mark.parametrize("score", [0, 100])
def test_load_scores_accepts_score_boundaries(tmp_path, score):
	path = tmp_path / "scores.csv"
	path.write_text(f"name,score\nBoundary,{score}\n", encoding="utf-8")

	kept, skipped = load_scores(path)

	assert kept == [("Boundary", score)]
	assert skipped == []


def test_load_scores_records_invalid_rows_with_line_numbers_and_reasons(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"name,score\n"
		"OnlyOne\n"          # 2: wrong number of columns
		",80\n"              # 3: empty name
		"NoScore,\n"          # 4: empty score
		"NotAnInt,abc\n"      # 5: non-integer score
		"TooLow,-1\n"         # 6: below range
		"TooHigh,101\n"       # 7: above range
		"Valid,50\n",
		encoding="utf-8",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Valid", 50)]
	assert skipped == [
		(2, "OnlyOne", "열 개수가 2가 아님"),
		(3, ",80", "이름이 비어 있음"),
		(4, "NoScore,", "점수가 비어 있음"),
		(5, "NotAnInt,abc", "점수가 정수가 아님"),
		(6, "TooLow,-1", "점수가 0~100 밖"),
		(7, "TooHigh,101", "점수가 0~100 밖"),
	]


def test_load_scores_reads_utf8_bom(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text("name,score\nKim,88\n", encoding="utf-8-sig")

	assert load_scores(path) == ([("Kim", 88)], [])


def test_load_scores_raises_file_not_found_error(tmp_path):
	missing_path = tmp_path / "missing.csv"

	with pytest.raises(FileNotFoundError):
		load_scores(missing_path)

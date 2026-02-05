"""
Beginner-friendly text summarizer.

Features:
- Reads text from user input or a text file
- Uses simple "AI-style" logic to summarize and structure the text
- Outputs a short summary and bullet points
- Prints the results and saves them to output.txt
"""

import re
from collections import Counter


def read_text_from_user() -> str:
	"""Ask the user to paste or type text directly."""
	print("Enter/paste your text. When finished, press Enter on an empty line:")
	lines = []
	while True:
		line = input()
		if line.strip() == "":
			break
		lines.append(line)
	return "\n".join(lines).strip()


def read_text_from_file(file_path: str) -> str:
	"""Read text from a file path provided by the user."""
	with open(file_path, "r", encoding="utf-8") as file:
		return file.read().strip()


def split_sentences(text: str) -> list:
	"""Split text into sentences using a simple pattern."""
	# This is a simple approach and works well for beginner use cases.
	sentences = re.split(r"(?<=[.!?])\s+", text.strip())
	return [s for s in sentences if s]


def summarize_text(text: str) -> tuple[str, list]:
	"""Create a short summary and bullet points from the text."""
	sentences = split_sentences(text)

	# Short summary: first 1-2 sentences (simple, beginner-friendly logic)
	summary = " ".join(sentences[:2]) if sentences else ""

	# Bullet points: pick key sentences based on keyword frequency
	words = re.findall(r"[A-Za-z']+", text.lower())
	common_words = {
		"the", "and", "is", "in", "to", "of", "a", "for", "on", "with",
		"as", "by", "at", "it", "this", "that", "from", "be", "are", "an"
	}
	keywords = [w for w in words if w not in common_words and len(w) > 2]
	keyword_counts = Counter(keywords)

	# Score each sentence by how many common keywords it contains
	sentence_scores = []
	for sentence in sentences:
		sentence_words = re.findall(r"[A-Za-z']+", sentence.lower())
		score = sum(keyword_counts.get(w, 0) for w in sentence_words)
		sentence_scores.append((score, sentence))

	# Take top 3 sentences as bullet points (keep original order)
	top_sentences = sorted(sentence_scores, key=lambda x: x[0], reverse=True)[:3]
	top_set = {s for _, s in top_sentences}
	bullet_points = [s for s in sentences if s in top_set]

	return summary, bullet_points


def format_output(summary: str, bullet_points: list) -> str:
	"""Create a clean output string for printing and saving."""
	lines = []
	lines.append("SUMMARY:")
	lines.append(summary if summary else "(No summary available)")
	lines.append("")
	lines.append("BULLET POINTS:")
	if bullet_points:
		for point in bullet_points:
			lines.append(f"- {point}")
	else:
		lines.append("- (No bullet points available)")
	return "\n".join(lines)


def main() -> None:
	"""Main program flow."""
	print("Text Summarizer")
	print("1) Type/paste text")
	print("2) Read from a file")
	choice = input("Choose an option (1 or 2): ").strip()

	if choice == "2":
		file_path = input("Enter the file path: ").strip()
		try:
			text = read_text_from_file(file_path)
		except FileNotFoundError:
			print("File not found. Please check the path and try again.")
			return
	else:
		text = read_text_from_user()

	if not text:
		print("No text provided. Exiting.")
		return

	summary, bullet_points = summarize_text(text)
	output = format_output(summary, bullet_points)

	# Print results clearly
	print("\n" + output)

	# Save results to output.txt
	with open("output.txt", "w", encoding="utf-8") as file:
		file.write(output)

	print("\nSaved to output.txt")


if __name__ == "__main__":
	main()

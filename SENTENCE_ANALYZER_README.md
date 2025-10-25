# Sentence Analyzer for Turkish Text-to-Speech

## Overview
This tool analyzes `givenText.txt` to identify the longest sentences that may need additional punctuation marks for better text-to-speech conversion. Long sentences without proper punctuation can cause issues with natural speech flow and breathing patterns in TTS systems.

## Usage

### Basic Usage
```bash
python3 analyze_sentences.py
```

This will:
1. Analyze all sentences in `givenText.txt`
2. Display the longest sentences sorted by word count (descending)
3. Show sentences without internal punctuation (commas, semicolons, colons)
4. Generate statistics about your text
5. Save results to `sentence_analysis.txt`

### Output Files
- **sentence_analysis.txt**: Contains a complete list of all sentences sorted by word count, with the format:
  ```
  [word_count] words | [sentence text]
  ```

## What It Analyzes

### Analysis 1: Longest Sentences with Low Punctuation Density
- Shows the top 30 longest sentences
- Displays word count, internal punctuation count, and punctuation density
- Helps identify sentences that might benefit from additional commas or other punctuation

### Analysis 2: Long Sentences WITHOUT Any Internal Punctuation
- Focuses on sentences with 15+ words that have NO commas, semicolons, or colons
- These sentences are prime candidates for adding punctuation to improve TTS flow

## Understanding the Output

Each sentence entry shows:
- **Word count**: Number of words in the sentence
- **Internal punctuation marks**: Count of commas, semicolons, and colons
- **Punctuation density**: Ratio of punctuation marks to words (lower = fewer punctuation marks)

### Example Output
```
62 words, 5 punctuation marks, density: 0.081
Bu doğrultuda hareket etmek üzere dört temel kural belirledi: (1) doğruluğu...
```

This sentence has 62 words but only 5 internal punctuation marks (density 0.081), which might make it challenging for TTS to process naturally.

## Customization

You can modify the script to change:

### Minimum Word Count for Analysis
Edit the function call in `main()`:
```python
no_punct = find_sentences_without_punctuation(min_words=20)  # Change from 15 to 20
```

### Number of Sentences Displayed
```python
print_analysis(sentence_data, top_n=50, show_density=True)  # Change from 30 to 50
```

### Input File
Change the file being analyzed:
```python
sentence_data = analyze_sentences('different_file.txt')
```

## Integration with TTS Workflow

1. **Run the analyzer** before processing text for TTS
2. **Review** `sentence_analysis.txt` for long sentences
3. **Add punctuation** (commas, semicolons) to break up long sentences
4. **Update** `givenText.txt` with improved punctuation
5. **Re-run** the analyzer to verify improvements
6. **Process** the improved text with your TTS functions

## Tips for Adding Punctuation

For Turkish text, consider adding commas at:
- After introductory phrases (ancak, dolayısıyla, bunun için)
- Between clauses connected by "ve", "veya", "ama"
- After subordinate clauses (ki, için, gibi, ile)
- To separate items in lists
- Around parenthetical expressions

## Statistics Provided

The tool provides:
- Total number of sentences analyzed
- Count of long sentences without punctuation
- Average sentence length (words)
- Average internal punctuation per sentence

Use these metrics to track improvements in your text over time.

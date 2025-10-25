#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentence Length Analyzer for Turkish Text
Analyzes givenText.txt to find longest sentences without proper punctuation
"""

import re
import functions


def analyze_sentences(file_path='givenText.txt', apply_preprocessing=True):
    """
    Reads the given text file and analyzes sentences to find the longest ones
    without proper punctuation marks for natural speech.
    
    Args:
        file_path: Path to the text file to analyze
        apply_preprocessing: If True, applies the TTS preprocessing functions before analysis
        
    Returns:
        List of tuples (word_count, sentence) sorted by word count in descending order
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Apply preprocessing pipeline if requested
    if apply_preprocessing:
        print("Applying TTS preprocessing functions...")
        try:
            pfirstCheck = functions.firstCheck(text)
            prepParen = functions.repParen(pfirstCheck.lower())
            prepWords = functions.repWords(prepParen)
            pLastcheck = functions.lastCheck(prepWords)
            # Apply only the simplified_rules with rules3 (skip wrapSoftloud)
            text = functions.apply_simplified_rules(pLastcheck, functions.rules3)
            print("Preprocessing complete (with rules3 applied)!\n")
        except Exception as e:
            print(f"Warning: Error during preprocessing: {e}")
            print("Continuing with original text...\n")
    
    # Split text by sentence-ending punctuation
    # Consider ., !, ?, as sentence endings - but capture them too
    sentences = re.split(r'([.!?]+)', text)
    
    sentence_data = []
    
    # Process pairs of sentence and its ending punctuation
    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i].strip()
        ending_punct = sentences[i+1] if i+1 < len(sentences) else ''
        
        # Skip empty sentences
        if not sentence:
            continue
        
        # Combine sentence with its ending punctuation
        full_sentence = sentence + ending_punct
        
        # Count words (split by whitespace)
        words = sentence.split()
        word_count = len(words)
        
        # Only consider sentences with at least 5 words
        if word_count >= 5:
            # Check if sentence has internal punctuation (commas, semicolons, colons, ¿)
            comma_count = sentence.count(',') + sentence.count('¿')
            semicolon_count = sentence.count(';')
            colon_count = sentence.count(':')
            internal_punct_count = comma_count + semicolon_count + colon_count
            
            # Calculate punctuation density (internal punctuation per word)
            punct_density = internal_punct_count / word_count if word_count > 0 else 0
            
            # Calculate the longest segment without punctuation
            # Split by any internal punctuation (including ¿)
            segments = re.split(r'[,;:¿]', sentence)
            max_segment_length = max(len(seg.split()) for seg in segments) if segments else word_count
            
            # Store sentence with metadata
            sentence_data.append({
                'word_count': word_count,
                'sentence': full_sentence,  # Use full_sentence with ending punctuation
                'comma_count': comma_count,
                'internal_punct': internal_punct_count,
                'punct_density': punct_density,
                'max_segment_length': max_segment_length,
                'needs_attention': max_segment_length > 15 or (word_count > 20 and comma_count == 0)
            })
    
    # Sort by max_segment_length (descending) - this shows sentences with longest unpunctuated segments
    sentence_data.sort(key=lambda x: (-x['max_segment_length'], -x['word_count']))
    
    return sentence_data


def print_analysis(sentence_data, top_n=20, show_density=False):
    """
    Prints the analysis results in a formatted way.
    
    Args:
        sentence_data: List of sentence dictionaries from analyze_sentences()
        top_n: Number of top sentences to display
        show_density: Whether to show punctuation density in output
    """
    if not sentence_data:
        print("No sentences to analyze.")
        return
    
    print("=" * 100)
    print(f"SENTENCES WITH LONGEST UNPUNCTUATED SEGMENTS (Top {top_n})")
    print("=" * 100)
    print()
    
    for i, data in enumerate(sentence_data[:top_n], 1):
        word_count = data['word_count']
        sentence = data['sentence']
        comma_count = data['comma_count']
        internal_punct = data['internal_punct']
        max_segment = data['max_segment_length']
        
        # Format the output
        header = f"{i}. {word_count} words | Longest unpunctuated segment: {max_segment} words | Commas: {comma_count}"
        
        print(header)
        print("-" * 100)
        
        # Highlight the segments by showing them split by punctuation (including ¿)
        segments = re.split(r'([,;:¿])', sentence)
        formatted = ""
        for seg in segments:
            if seg in [',', ';', ':', '¿']:
                formatted += seg + " "
            else:
                seg_words = len(seg.split())
                if seg_words > 15:
                    formatted += f"[{seg_words}w: {seg.strip()}]"
                else:
                    formatted += seg.strip()
        
        print(formatted)
        print()
        print("=" * 100)
        print()


def find_sentences_without_punctuation(file_path='givenText.txt', min_words=15, apply_preprocessing=True):
    """
    Finds sentences that are longer than min_words and have no internal punctuation.
    
    Args:
        file_path: Path to the text file to analyze
        min_words: Minimum word count to consider
        apply_preprocessing: If True, applies the TTS preprocessing functions before analysis
        
    Returns:
        List of tuples (word_count, sentence) for sentences without punctuation
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return []
    
    # Apply preprocessing pipeline if requested
    if apply_preprocessing:
        try:
            pfirstCheck = functions.firstCheck(text)
            prepParen = functions.repParen(pfirstCheck.lower())
            prepWords = functions.repWords(prepParen)
            pLastcheck = functions.lastCheck(prepWords)
            # Apply only the simplified_rules with rules3 (skip wrapSoftloud)
            text = functions.apply_simplified_rules(pLastcheck, functions.rules3)
        except Exception as e:
            print(f"Warning: Error during preprocessing: {e}")
    
    # Split by sentence-ending punctuation - capture them too
    sentences = re.split(r'([.!?]+)', text)
    
    no_punct_sentences = []
    
    # Process pairs of sentence and its ending punctuation
    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i].strip()
        ending_punct = sentences[i+1] if i+1 < len(sentences) else ''
        
        if not sentence:
            continue
        
        # Combine sentence with its ending punctuation
        full_sentence = sentence + ending_punct
        
        words = sentence.split()
        word_count = len(words)
        
        # Check if sentence is long enough and has no internal punctuation (including ¿)
        has_no_internal_punct = (
            ',' not in sentence and 
            ';' not in sentence and 
            ':' not in sentence and
            '¿' not in sentence
        )
        
        if word_count >= min_words and has_no_internal_punct:
            no_punct_sentences.append((word_count, full_sentence))
    
    # Sort by word count descending
    no_punct_sentences.sort(key=lambda x: -x[0])
    
    return no_punct_sentences


def print_no_punctuation_analysis(sentences, top_n=20):
    """
    Prints sentences without any internal punctuation.
    
    Args:
        sentences: List of (word_count, sentence) tuples
        top_n: Number of sentences to display
    """
    if not sentences:
        print("No long sentences without punctuation found.")
        return
    
    print("=" * 100)
    print(f"SENTENCES WITHOUT ANY INTERNAL PUNCTUATION (Top {top_n})")
    print("=" * 100)
    print()
    
    for i, (word_count, sentence) in enumerate(sentences[:top_n], 1):
        print(f"{i}. {word_count} words")
        print("-" * 100)
        print(sentence)
        print()
        print("=" * 100)
        print()


def save_to_file(sentence_data, output_file='sentence_analysis.txt'):
    """
    Saves the analysis results to a file for easy review.
    
    Args:
        sentence_data: List of sentence dictionaries from analyze_sentences()
        output_file: Path to output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("TURKISH TEXT SENTENCE ANALYSIS - SENTENCES NEEDING PUNCTUATION\n")
        f.write("=" * 100 + "\n\n")
        f.write("Format: [word_count] words | [max_unpunctuated_segment] words unpunctuated | [commas] | [sentence]\n\n")
        
        for i, data in enumerate(sentence_data, 1):
            word_count = data['word_count']
            sentence = data['sentence']
            max_segment = data['max_segment_length']
            comma_count = data['comma_count']
            
            f.write(f"{word_count} words | {max_segment} words unpunctuated | {comma_count} commas | {sentence}\n\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write("END OF ANALYSIS\n")
        f.write("=" * 100 + "\n")
    
    print(f"\nAnalysis saved to: {output_file}")


def main():
    """Main function to run the analysis."""
    print("=" * 100)
    print("TURKISH TEXT-TO-SPEECH SENTENCE ANALYZER")
    print("=" * 100)
    print("\nAnalyzing text AFTER applying TTS preprocessing functions...")
    print("(firstCheck -> repParen -> repWords -> lastCheck -> apply_simplified_rules(rules3))")
    print("Note: Skipping wrapSoftloud to avoid <prosody> tags in analysis\n")
    
    # Analyze all sentences with preprocessing
    sentence_data = analyze_sentences(apply_preprocessing=True)
    
    print("\nANALYSIS: Sentences with longest unpunctuated segments")
    print("(This shows sentences where there are long stretches without commas/punctuation)")
    print()
    print_analysis(sentence_data, top_n=30, show_density=True)
    
    print("\n\n")
    
    # Find sentences without any internal punctuation
    print("VERIFICATION: Long sentences with NO internal punctuation at all")
    print()
    no_punct = find_sentences_without_punctuation(min_words=15)
    print_no_punctuation_analysis(no_punct, top_n=20)
    
    # Print summary statistics
    print("\n" + "=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)
    print(f"Total sentences analyzed: {len(sentence_data)}")
    print(f"Sentences without ANY internal punctuation (15+ words): {len(no_punct)}")
    if sentence_data:
        avg_words = sum(s['word_count'] for s in sentence_data) / len(sentence_data)
        avg_comma = sum(s['comma_count'] for s in sentence_data) / len(sentence_data)
        avg_max_segment = sum(s['max_segment_length'] for s in sentence_data) / len(sentence_data)
        sentences_needing_attention = sum(1 for s in sentence_data if s['needs_attention'])
        
        print(f"Average sentence length: {avg_words:.1f} words")
        print(f"Average commas per sentence: {avg_comma:.2f}")
        print(f"Average longest unpunctuated segment: {avg_max_segment:.1f} words")
        print(f"Sentences needing attention (>15 word segments or >20 words with no commas): {sentences_needing_attention}")
    
    # Save results to file
    if sentence_data:
        save_to_file(sentence_data, 'sentence_analysis.txt')


if __name__ == "__main__":
    main()

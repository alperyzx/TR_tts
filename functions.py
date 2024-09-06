# Description: This file contains the functions used in the main script.
import re
import time
import string
from google.cloud import texttospeech

# Define the output directory as a global variable (outside the function)
output_dir = "d:/books/ders/output"

def text2speech(text, language_code="tr-TR", voice_name="tr-TR-Standard-E"):
    # print (f'ssml input: {text}')
    # Create a TextToSpeech client (assuming it's not already created elsewhere)
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Generate a unique filename incorporating a timestamp
    current_time = int(time.time())
    filename = f"{output_dir}/{current_time}.mp3"

    with open(filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{filename}"')

def replace_roman_numerals(text):
    # first replace upper turkish i to lower i
    text = ascii_text = text.replace("İ", "i")
    # Define the Roman numerals and their corresponding Arabic numerals
    roman_to_int_mapping = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    # Define a function to convert a Roman numeral to an Arabic numeral
    def roman_to_int(s):
        total = 0
        prev_value = 0
        for char in reversed(s):
            current_value = roman_to_int_mapping[char]
            if prev_value > current_value:
                total -= current_value
            else:
                total += current_value
            prev_value = current_value
        return total

    # Define a regular expression pattern to find Roman numerals
    pattern = r'\b[MDCLXVI]+\b'

    # Use the re.sub function to replace each Roman numeral with its corresponding Arabic numeral
    text = re.sub(pattern, lambda m: str(roman_to_int(m.group(0))), text)
    return text

def addSsml(mdText):
    mdText = re.sub(r'¿',r',', mdText)
    mdText = re.sub(r'\.(?=\n[^$])', '. ', mdText)  # Split text into paragraphs
    paragraphs = mdText.split("\n\n")

    for i, paragraph in enumerate(paragraphs):
        # Skip if paragraph is an empty string
        if not paragraph.strip():
            continue

        # Split paragraph into sentences
        sentences = paragraph.split(". ")
        ssml_output = "<speak><p>\n <break time=\"1s\"/>\n"
        current_length = len(ssml_output)

        for j, sentence in enumerate(sentences):
            # Add dot at the end of each sentence if it's not the last one
            if j != len(sentences) - 1:
                sentence += "."
            # Add <s> tags to each sentence if it's not an empty string
            if sentence.strip():
                sentence_ssml = f" <s>{sentence.strip()}</s>\n"
                sentence_length = len(sentence_ssml)
                if current_length + sentence_length > 3000:
                    # Close the current SSML output and send it to text2speech
                    ssml_output += "</p></speak>"
                    ssml_output = fix_yy(ssml_output)
                    ssml_output = replace_numbers(ssml_output)
                    print(f'\nSSML output OK: {len(ssml_output)} passing it to text2speech')
                    print(f'addSsml: \n{ssml_output}')
                    #text2speech(ssml_output)

                    # Start a new SSML output
                    ssml_output = "<speak><p>\n <break time=\"1s\"/>\n"
                    current_length = len(ssml_output)

                ssml_output += sentence_ssml
                current_length += sentence_length

                if j % 2 == 1 and j != len(sentences) - 1:
                    ssml_output += " <break time=\"1.0s\"/>\n"
                    current_length += len(" <break time=\"1.0s\"/>\n")

        # Close the SSML output and send it to text2speech
        ssml_output += "</p></speak>"
        ssml_output = fix_yy(ssml_output)
        ssml_output = replace_numbers(ssml_output)
        print(f'\nSSML output OK: {len(ssml_output)} passing it to text2speech')
        print(f'addSsml: \n{ssml_output}')
        #text2speech(ssml_output)

    return ssml_output

def fix_yy(ptext):
    ptext= re.sub(r'_yy', '. yüzyıl', ptext)
    return ptext

def replace_numbers(text):
    # return re.sub(r'(?<=\S) (\d+!)', lambda m: ' ' + m.group(1)[:-1] + '.', text)
    text = re.sub(r'(\d+_)', lambda m: m.group(0)[:-1] + ('.' if m.group(0)[-2].isdigit() else '_'), text)
    text = apply_sub_outside_parentheses(text)
    return text

def apply_sub_outside_parentheses(mtext):
    segments = re.split(r'(\(.*?\))', mtext)
    for i in range(len(segments)):
        # If the segment is not inside parentheses
        if not (segments[i].startswith('(') and segments[i].endswith(')')):
            segments[i] = re.sub(r'(\d+)- ', r'\1!, ', segments[i])
    return ''.join(segments)


def replace_headers(givenText):
    def replacer(match):
        return '}'.join(match.group(1).split('.')) + '}'

    return re.sub(r'^(\d+(\.\d+)*)\.', replacer, givenText, flags=re.MULTILINE)

def split_yle(text):
    # Split the text into lines
    lines = text.split('\n')

    # Iterate over each line
    for i in range(len(lines)):
        # Split the line into words
        words = lines[i].split()

        # Iterate over each word in the line
        for j in range(len(words)):
            # Strip trailing punctuation from the word
            stripped_word = words[j].rstrip(string.punctuation)

            # If the stripped word ends with "yle" or "yla", its length is more than 6, and it does not already contain an apostrophe before "yle" or "yla"
            if stripped_word.endswith(("yle", "yla")) and len(stripped_word) > 6 and not stripped_word[-4] == "’":
                # Replace "yle" or "yla" with "'yle" or "'yla", preserving any trailing punctuation
                words[j] = stripped_word[:-3] + "’" + stripped_word[-3:] + words[j][len(stripped_word):]

        # Join the words back into a line
        lines[i] = ' '.join(words)

    # Join the lines back into a text
    text = '\n'.join(lines)

    return text

def apply_simplified_rules(text, rules):
    punctuation = (';', ':', '.', ',', '¿')
    sentence_ending_punctuation = ('.', '!', '?')
    modified_paragraphs = []
    #print("Starting apply_simplified_rules ...")

    paragraphs = text.split('\n')

    for paragraph in paragraphs:
        sentences = paragraph.split('.')
        modified_lines = []

        for sentence in sentences:
            #print(f"Processing sentence: {sentence.strip()}")
            words = sentence.split()
            for j, word in enumerate(words):
                applied = False
                stripped_word = word.strip('¿')

                if stripped_word in rules and (word.endswith('¿') or word.startswith('¿')):
                    rule = rules[stripped_word]
                    if j == 0 or j == 1 or j == 2 or j == len(words) - 3 or j == len(words) - 2:
                        words[j] = stripped_word if rule['stripMark'] else word
                        applied = True

                if not applied and stripped_word in rules:
                    rule = rules[stripped_word]
                    left_range, right_range = rule['range']
                    left_indices = range(max(0, j - left_range), j)
                    right_indices = range(j + 1, min(len(words), j + right_range + 1))

                    if any(words[k].endswith(punctuation) or words[k].startswith(punctuation) for k in left_indices) or \
                            any(words[k].endswith(punctuation) or words[k].startswith(punctuation) for k in right_indices):
                        words[j] = stripped_word if rule['stripMark'] else word

            modified_lines.append(' '.join(words))

        modified_paragraphs.append('. '.join(modified_lines).strip())

    processed_text = '\n'.join(modified_paragraphs)
    print("Finished apply_simplified_rules ")
    return processed_text


rules1 = {
    "da": {"stripMark": True, "range": (2, 3)},
    "de": {"stripMark": True, "range": (2, 3)},
    "dolayı": {"stripMark": True, "range": (1, 2)},
}

rules2 = {
    "ve": {"stripMark": True, "range": (3, 3)},
}

rules3 = {
    "için": {"stripMark": True, "range": (3, 1)},
    "ile": {"stripMark": True, "range": (2, 2)},
    "hem": {"stripMark": True, "range": (1, 1)},
    "gibi": {"stripMark": True, "range": (3, 3)},
    "bile": {"stripMark": True, "range": (1, 1)},
    "daha": {"stripMark": True, "range": (2, 2)},
    "göre": {"stripMark": True, "range": (1, 2)},
    "değil": {"stripMark": True, "range": (1, 1)},
    "hangi": {"stripMark": True, "range": (1, 2)},
    "yani": {"stripMark": True, "range": (1, 1)},
    "kadar": {"stripMark": True, "range": (1, 1)},
    "bilakis": {"stripMark": True, "range": (1, 1)},
    "üzere": {"stripMark": True, "range": (1, 1)},
    "yoksa": {"stripMark": True, "range": (1, 1)},
    "özellikle": {"stripMark": True, "range": (1, 1)},
    "bir taraftan": {"stripMark": True, "range": (1, 1)},
}


def firstCheck(ftext):
    # replace dots next to first names of people. to make sentence detection simpler.
    ftext = re.sub(r'([A-Z])\.', r'\1-', ftext)
    ftext = re.sub(r'(\d+)\.\s*yy', r'\1_yy', ftext)
    ftext = re.sub(r'(\d+)\. ?yüzyıl', r'\1_yy', ftext)
    ftext= re.sub(r'\(([^()]*?):([^()]*?)\)', r'(\1;\2)', ftext)
    ftext = re.sub(r'\?', '? . ', ftext)
    ftext = re.sub(r's\. ?(\d+)', r'sayfa \1', ftext)
    ftext=re.sub(r'\(\.\.\.\)', '¤', ftext)

    ftext = ascii_text = ftext.replace("İ", "i")
    ftext = re.sub(r'(?<=\s)da \b', 'da¿ ', ftext)
    ftext = re.sub(r'(?<=\s)de \b', 'de¿ ', ftext)
    ftext = re.sub(r'\b ve\b', ' ¿ve', ftext)
    ftext = re.sub(r'\b veya\b', ' ¿veya', ftext)
    ftext = re.sub(r'\bdolayı \b', 'dolayı¿ ', ftext)

    # ftext = re.sub(r'\bya\b', ',ya', ftext)
    ftext = re.sub(r'(?<![’\w])ya\b', '¿ya', ftext)

    ftext = re.sub(r'n’un', 'nun', ftext)
    ftext = re.sub(r'n’a', 'na', ftext)
    ftext = re.sub(r's’', 's', ftext)
    ftext = re.sub(r't’', 't', ftext)
    ftext = re.sub(r"'", "’", ftext)  #replace ' with ’ -- tts engine reads ’ better.
    print(f'firstCheck: {ftext}')
    return ftext

def repParen(rtext):
    rtext = replace_headers(rtext)
    # rtext = re.sub(r'^(\d+)[).-] ', r'\1}, ', rtext, flags=re.MULTILINE)
    rtext = re.sub(r'\.\s*”', '”.', rtext)
    rtext = re.sub(r'(?=\S)([^\.])\s*$', r'\1!!', rtext, flags=re.MULTILINE)
    rtext = rtext.replace(":", "!:.")
    rtext = re.sub(r'\bmö\b\.?', 'milattan önce ', rtext)
    rtext = re.sub(r'\bayr\b\.?', 'ayrıca ', rtext)
    rtext = re.sub(r'\böl\b\.?', 'ölümü ', rtext)
    rtext = re.sub(r'\bö\b\.?', 'ölümü ', rtext)
    rtext = re.sub(r'\bmö\s\.?', 'milattan önce', rtext)
    rtext = re.sub(r'\bm\.ö\.', 'milattan önce', rtext)
    rtext = re.sub(r'\bms\b\.?', 'milattan sonra', rtext)
    rtext = re.sub(r'\bms\s\.?', 'milattan sonra', rtext)
    rtext = re.sub(r'\bm\.s\.', 'milattan sonra', rtext)
    rtext = re.sub(r'\bakt\b\.?', 'aktaran ', rtext)
    #rtext = re.sub(r'\byön\b\.?', 'yönetmen ', rtext)
    # rtext = re.sub(r'\bder\b\.?', 'derleyen ', rtext)
    rtext = re.sub(r'\bçev\b\.?', 'çeviren ', rtext)
    rtext = re.sub(r'\bed\b\.?', 'editor ', rtext)
    rtext = re.sub(r'\byay\b\.?', 'yayınları ', rtext)
    rtext = re.sub(r'\btüik\b\.?', 'türkiye istatistik kurumu', rtext)
    # Find all occurrences of ")."
    periods = [match.start() for match in re.finditer(r'\)\.', rtext)]

    # Reverse the list to replace from the end of the text to the beginning
    periods.reverse()

    # Replace one "(" before each ")." and remove any space before it
    for period in periods:
        open_paren_index = rtext.rfind('(', 0, period)
        if open_paren_index != -1:
            # Check if there is a space before the "(" and remove it
            if rtext[open_paren_index - 1] == ' ':
                rtext = rtext[:open_paren_index - 1] + '. (' + rtext[open_paren_index + 1:]
            else:
                rtext = rtext[:open_paren_index] + '. (' + rtext[open_paren_index + 1:]
    print(f'repParen: {rtext}')
    return rtext

def repWords(mtext):
    mtext = split_yle(mtext)
    mtext = apply_simplified_rules(mtext, rules1)
    mtext = re.sub(r'\bydh\b\.?', 'yeni dini hareket', mtext)
    mtext = re.sub(r'\balim(\w*)\b', r'aalim\1', mtext)
    mtext = re.sub(r'\bschacht(\w*)\b', r'schaht\1', mtext)
    mtext = re.sub(r'\bvacip(\w*)\b', r'vaacip\1', mtext)
    mtext = re.sub(r'\bnous(\w*)\b', r'nohus\1', mtext)
    mtext = re.sub(r'\bhyle(\w*)\b', r'heyle\1', mtext)
    mtext = re.sub(r'\balem(\w*)\b', r'âlem\1', mtext)
    mtext = re.sub(r'\bkafir(\w*)\b', r'kâfir\1', mtext)
    mtext = re.sub(r'\bkainat(\w*)\b', r'kâinat\1', mtext)
    mtext = re.sub(r'\bkeramet(\w*)\b', r'kerâmet\1', mtext)
    mtext = re.sub(r'\bkafiye(\w*)\b', r'kâfiye\1', mtext)
    mtext = re.sub(r'\bliteralizm(\w*)\b', r'literâlizm\1', mtext)
    mtext = re.sub(r'\bspekülatif(\w*)\b', r'spekü’latif\1', mtext)
    mtext = re.sub(r'\bmerasim(\w*)\b', r'merâsim\1', mtext)
    mtext = re.sub(r'\bthales(\w*)\b', r'tales\1', mtext)
    mtext = re.sub(r'\bdeterminizm(\w*)\b', r'determinizim\1', mtext)

    mtext = re.sub(r'nizam-ı(\w*)', r"nizam’ı\1", mtext)
    mtext = re.sub(r'kitab-ı(\w*)', r"kitabı\1", mtext)
    mtext = re.sub(r'asr-ı(\w*)', r"asr’ı\1", mtext)
    mtext = re.sub(r'insan-ı(\w*)', r"insan’ı\1", mtext)

    # mtext = re.sub(r'\bnesney(\w*)\b', r'nesne’y\1', mtext)
    mtext = re.sub(r'\bkurcala(\w*)\b', r'kurca’la\1', mtext)
    mtext = re.sub(r'\btelakki(\w*)\b', r'telak’ki\1', mtext)
    # mtext = re.sub(r'\bfelsefey(\w*)\b', r'felsefe’y\1', mtext)
    # mtext = re.sub(r'\bçerçevey(\w*)\b', r'çerçeve’y\1', mtext)

    mtext = re.sub(r'\bseyyah(\w*)\b', r'seyyah’\1', mtext)
    mtext = re.sub(r'\bmeta(\w*)\b', r'meta’\1', mtext)
    mtext = re.sub(r'\bkapitalizm(\w*)\b', r'kapitalizm’\1', mtext)
    mtext = re.sub(r'\bsosyalizm(\w*)\b', r'sosyalizm’\1', mtext)
    mtext = re.sub(r'\bkur’an(\w*)\b', r'kuran\1', mtext)
    mtext = re.sub(r'\bkur’ân(\w*)\b', r'kuran\1', mtext)
    mtext = re.sub(r'\bkur’ân-ı(\w*)\b', r'kuranı\1', mtext)
    mtext = re.sub(r'\bnumenal(\w*)\b', r'numena’l\1', mtext)
    mtext = re.sub(r'\btransendental(\w*)\b', r'transendenta’l\1', mtext)
    mtext = re.sub(r'\btransandantal(\w*)\b', r'transandanta’l\1', mtext)
    mtext = re.sub(r'\bfenomenal(\w*)\b', r'fenomena’l\1', mtext)
    mtext = re.sub(r'\bkurgan(\w*)\b', r'kurga’n\1', mtext)
    mtext = re.sub(r'\bödeve(\w*)\b', r'ödev’e\1', mtext)
    mtext = re.sub(r'\bspekülatif(\w*)\b', r'spekülati’f\1', mtext)
    mtext = re.sub(r'\bmuteber(\w*)\b', r'muteb’er\1', mtext)
    mtext = re.sub(r'\bmümin(\w*)\b', r'mü’min\1', mtext)
    mtext = re.sub(r'\bseman(\w*)\b', r'sema’n\1', mtext)
    mtext = re.sub(r'\borhon(\w*)\b', r'orho’n\1', mtext)
    mtext = re.sub(r'\bzüht(\w*)\b', r'züh’t\1', mtext)
    mtext = re.sub(r'\bzühd(\w*)\b', r'züh’d\1', mtext)
    mtext = re.sub(r'\bspekülatif(\w*)\b', r'spekülati’f\1', mtext)
    mtext = re.sub(r'\bkura’n(\w*)\b', r'kuran\1', mtext)
    mtext = re.sub(r'\bvahiy(\w*)\b', r'vahiy’\1', mtext)
    mtext = re.sub(r'\bliteral(\w*)\b', r'literâl\1', mtext)
    mtext = re.sub(r'\bhadisi(\w*)\b', r'hadisi’\1', mtext)
    mtext = re.sub(r'\bşafi(\w*)\b', r'şaafi\1', mtext)
    mtext = re.sub(r'\bhakim(\w*)\b', r'haakim\1', mtext)
    mtext = re.sub(r'\bgaza(\w*)\b', r'gazaa\1', mtext)
    mtext = re.sub(r'\bhale(\w*)\b', r'haale\1', mtext)
    mtext = re.sub(r'\bhalife(\w*)\b', r'halife’\1', mtext)
    mtext = re.sub(r'\bpadişah(\w*)\b', r'padişah’\1', mtext)
    mtext = re.sub(r'\breaya(\w*)\b', r'reaya’\1', mtext)
    mtext = re.sub(r'\bfiskalizm(\w*)\b', r'fiskalizm’\1', mtext)
    mtext = re.sub(r'\bfilozof(\w*)\b', r'filozof’\1', mtext)
    # mtext = re.sub(r'\bçevre(\w*)\b', r'çevre’\1', mtext)
    mtext = re.sub(r'\bahlâk(\w*)\b', r'ahlak\1', mtext)
    mtext = re.sub(r'\bkindî(\w*)\b', r'kindi\1', mtext)
    mtext = re.sub(r'\bhayatî(\w*)\b', r'hayati\1', mtext)
    mtext = re.sub(r'\bilâh(\w*)\b', r'ilah\1', mtext)
    mtext = re.sub(r'\bi̇slam(\w*)\b', r'islam\1', mtext)
    mtext = re.sub(r'\bi̇slâm(\w*)\b', r'islam\1', mtext)
    mtext = re.sub(r'\bislâm(\w*)\b', r'islam\1', mtext)
    mtext = re.sub(r'\bislamî(\w*)\b', r'islami\1', mtext)
    mtext = re.sub(r'\bkelâm(\w*)\b', r'kelam\1', mtext)
    mtext = re.sub(r'\bi̇nsan(\w*)\b', r'i̇nsan\1', mtext)
    mtext = re.sub(r'\bmutezile(\w*)\b', r'mu’tezile\1', mtext)
    mtext = re.sub(r'\bbatini(\w*)\b', r'baatini\1', mtext)
    mtext = re.sub(r'\bitikadi(\w*)\b', r'iitikadi\1', mtext)
    mtext = re.sub(r'\bchomsky(\w*)\b', r'çomski\1', mtext)
    mtext = re.sub(r'\btatianus(\w*)\b', r'tatyanus\1', mtext)
    mtext = re.sub(r'\btatien(\w*)\b', r'tatyen\1', mtext)
    mtext = re.sub(r'\bpantene(\w*)\b', r'panten\1', mtext)

    mtext = re.sub(r'i̇bn\s', 'ibni ', mtext)
    mtext = re.sub(r'batıl\s', 'baatıl', mtext)
    mtext = re.sub(r'\bibn\s', 'ibni ', mtext)
    mtext = re.sub(r'\bsiyasî(\w*)\b', r'siyasi\1', mtext)
    mtext = re.sub(r'\bmekâni(\w*)\b', r'mekani\1', mtext)
    mtext = re.sub(r'\bplaton(\w*)\b', r"plato'n\1", mtext)
    mtext = re.sub(r'\bklement(\w*)\b', r"klem'ent\1", mtext)
    mtext = re.sub(r'\borigenes(\w*)\b', r"ori-gene's\1", mtext)
    mtext = re.sub(r'\bpahl(\w*)\b', r"pah'l\1", mtext)

    mtext = re.sub(r'\bfakat \b', 'fakat¿ ', mtext)
    mtext = re.sub(r'\bdahi \b', 'dahi¿ ', mtext)
    mtext = re.sub(r'\b daha\b', ' ¿daha', mtext)
    mtext = re.sub(r'\bilaveten \b', 'ilaveten¿ ', mtext)
    # mtext = re.sub(r'\bolarak \b', 'olarak¿ ', mtext)
    mtext = re.sub(r'\bsebebiyle \b', 'sebebiyle¿ ', mtext)
    mtext = re.sub(r'\byahut\b', '¿yahut', mtext)
    mtext = re.sub(r'\bhangi\b', '¿hangi', mtext)
    mtext = re.sub(r'\bgöre \b', 'göre¿ ', mtext)
    mtext = re.sub(r'\bdeğil \b', 'değil¿ ', mtext)
    mtext = re.sub(r'\bziyade \b', 'ziyade¿ ', mtext)
    mtext = re.sub(r'\biken \b', 'iken¿ ', mtext)
    mtext = re.sub(r'\byani\b', '¿yani', mtext)
    mtext = re.sub(r'\bbilakis\b', '¿bilakis', mtext)
    mtext = re.sub(r'\byoksa\b', '¿yoksa', mtext)
    mtext = re.sub(r'\bözellikle\b', '¿özellikle', mtext)
    mtext = re.sub(r'\bkadar\b', 'kadar¿', mtext)
    mtext = re.sub(r'\büzere\b', 'üzere¿', mtext)
    mtext = re.sub(r'\bgibi \b', 'gibi¿ ', mtext)
    mtext = re.sub(r'\bhem\b', '¿hem', mtext)
    mtext = re.sub(r'\brağmen \b', 'rağmen¿ ', mtext)
    mtext = re.sub(r'\bbile \b', 'bile¿ ', mtext)
    mtext = re.sub(r'\bile \b', 'ile¿ ', mtext)
    mtext = re.sub(r'\biçin \b', 'için¿ ', mtext)
    mtext = re.sub(r'\bancak\b', '¿ancak', mtext)
    mtext = re.sub(r'\bhatta\b', '¿hatta', mtext)
    mtext = re.sub(r'\bbir taraftan\b', '¿bir taraftan', mtext)
    mtext = re.sub(r'\bise \b', 'ise¿ ', mtext)

    mtext = re.sub(r'(?<=\s)ki \b', 'ki¿ ', mtext)

    mtext = re.sub(r'¿ya da,', '¿ya da', mtext)
    mtext = re.sub(r'o zaman ', '¿o zaman ', mtext)
    mtext = re.sub(r'\bama\b', '¿ama', mtext)

    mtext = re.sub(r'\bvs\.', 'vesaire,', mtext)
    mtext = re.sub(r'\bvb\.', 'vebenzeri', mtext)
    mtext = re.sub(r'\bvd\.', 'vediğer', mtext)
    mtext = re.sub(r'\bvd\b', 'vediğer', mtext)
    mtext = re.sub(r'\bv\.b\.', 'vebenzeri', mtext)
    mtext = re.sub(r'\bhz\.', 'hazreti', mtext)
    mtext = re.sub(r'\bhaz\.', 'hazırlayan ', mtext)
    mtext = re.sub(r'\biq', 'ay q', mtext)

    # Replace numbered lines with "1), ", "2), ", "3), ", etc.
    # mtext = re.sub(r'^(\d+)[).-] ', r'\1!, ', mtext, flags=re.MULTILINE)
    # Replace "1- ", "2- ", "3- ", etc. with "1), ", "2), ", "3), ", etc.
    # mtext = apply_sub_outside_parentheses(mtext)
    # mtext = re.sub(r'(\d+)[.)],', r'\1,', mtext)
    mtext = re.sub(r'(\d+)[.]', r'\1_', mtext)

    # Add a space after every dot at the end of the line
    mtext = re.sub(r'\)(?=\s*$)', ').', mtext, flags=re.MULTILINE)
    mtext = re.sub(r'\.(?=\n)', '. ', mtext)
    print(f'repWords: {mtext}')
    return mtext

def lastCheck(text):
    text= re.sub(r'\. \.', '.', text)
    text = re.sub(r"’(?=\s|$)", " ", text)
    text = re.sub(r"(\w+)’,", r"\1,", text)
    text = text.replace("¿hem de¿", "¿hem de")
    text = apply_simplified_rules(text, rules2)

    print(f'lastCheck: {text}')
    return text

def fixPunct(ptext):
    ptext = wrapSoftloud(ptext)
    ptext = apply_simplified_rules(ptext, rules3)
    print(f'fixPunctuation: {ptext}')
    return ptext

def wrapSoftloud(wtext):
    # Wrap texts in parentheses with <prosody volume="soft"></prosody> tags
    wtext = re.sub(r'^(.*!!)$', r'<prosody volume="loud">\1</prosody> . ', wtext, flags=re.MULTILINE)
    wtext = re.sub(r'\((.*?)\)', r'<prosody volume="soft">(\1)</prosody>', wtext, flags=re.IGNORECASE)
    print(f'loudSoft: {wtext}')
    return wtext


# Tokenizer v1 for TinyGPT
# 're' is a regular expression library used to evaluate text patterns.
import re
import json

class Tokenizer:
    # On the formation of the tokenizer object, the default constructor will be called.
    def __init__(self):
        # Setting the maximum sequence length for our context window.
        self.maxlength = 512
        # Making the dictionaries for the model's vocabulary.
        self.word_to_id = {}
        self.id_to_word = {}

    # Property to easily check the size of the vocabulary.
    @property
    def vocab_size(self):
        return len(self.word_to_id)

    # Internal function to safely handle the case when the vocabulary is not built yet.
    def _check_vocabulary(self):
        if not self.word_to_id or not self.id_to_word:
            raise ValueError("Vocabulary is not built yet. Please call build_vocabulary() or load() first.")

    # Internal function to split the sentence into distinct tokens.
    def _split(self, sentence):
        # Identifying the pattern using regex.
        # \w+ : Matches one or more word characters.
        # [^\w\s]: Matches any symbol (like ! or .) excluding words and whitespace.
        return re.findall(r"\w+|[^\w\s]", sentence)

    # Function to build vocabulary from the training dataset and feed it to the dictionaries.
    def build_vocabulary(self, corpus):
        # 'tokens' is a set of unique words.
        tokens = set()
        for sentence in corpus:
            tokens.update(self._split(sentence))
        
        # We are creating a deterministic vocabulary from the sorted tokens.
        vocab = ["<PAD>", "<UNK>", "<SOS>", "<EOS>"] + sorted(tokens)
        
        # Now we map the vocabulary into our dictionaries.
        self.word_to_id = {w: i for i, w in enumerate(vocab)}
        self.id_to_word = {i: w for w, i in self.word_to_id.items()}

    # Encode function to translate a raw sentence into a tensor-ready list of IDs.
    def encode(self, sentence):
        self._check_vocabulary()
        tokens = self._split(sentence)
        
        # Retrieves the ID of the token 't'. If not found, defaults to the ID of "<UNK>".
        encoded = [self.word_to_id.get(t, self.word_to_id["<UNK>"]) for t in tokens]
        # Truncate if the sequence exceeds our maximum context window.
        if self.maxlength is not None and len(encoded) > (self.maxlength-2):
                    encoded = encoded[:self.maxlength-2]
        # Wrap the sequence in <SOS> (Start of Sequence) and <EOS> (End of Sequence) tokens.
        sequence = [self.word_to_id["<SOS>"]] + encoded + [self.word_to_id["<EOS>"]] 
        return sequence

    # Padding function to ensure uniform tensor shapes for batch processing.
    def padding(self, sequence, target_length):
        self._check_vocabulary()
        pad_id = self.word_to_id["<PAD>"]
        padding_needed = target_length - len(sequence)
        
        if padding_needed > 0:
            return sequence + [pad_id] * padding_needed
            
        return sequence[:target_length]

    # Decode function to translate a list of IDs back into a clean, human-readable sentence.
    def decode(self, ids, skip_special_tokens=True):
        self._check_vocabulary()
        words = []
        
        for i in ids:
            word = self.id_to_word.get(i, "<UNK>")
            # If the flag is True, we strip out structural tokens for a clean UI output.
            if skip_special_tokens and word in ["<PAD>", "<SOS>", "<EOS>"]:
                continue
            words.append(word)
            
        # Join words with spaces.
        text = " ".join(words)
        
        # Detokenization: Remove the space before punctuation marks using regex.
        # This converts "Hello , how are you ?" into "Hello, how are you?"
        text = re.sub(r'\s+([?.!,;\'])', r'\1', text)
        
        return text.strip()

    # Save function to serialize the vocabulary to a JSON file.
    def save(self, filepath):
        with open(filepath, "w") as f:
            # We save version and metadata to future-proof the architecture.
            metadata = {
                "version": 1,
                "vocab_size": self.vocab_size,
                "word_to_id": self.word_to_id,
                "id_to_word": self.id_to_word
            }
            json.dump(metadata, f, indent=4)

    # Load function to restore the vocabulary from a JSON file.
    def load(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            self.word_to_id = data["word_to_id"]
            # json.load converts integer keys to strings, so we cast them back to int.
            self.id_to_word = {int(k): v for k, v in data["id_to_word"].items()}
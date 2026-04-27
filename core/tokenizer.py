"""
🧠 NanoTokenizer v2 - Advanced BERT-style + BPE
Advanced tokenization with subword handling and special tokens
"""
import re
import json
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
import numpy as np
from rich.console import Console

class NanoTokenizer:
    def __init__(self, vocab_size: int = 5000):
        self.console = Console()
        self.vocab_size = vocab_size
        self.special_tokens = {
            'PAD': 0, 'UNK': 1, 'CLS': 2, 'SEP': 3, 'MASK': 4
        }
        self.vocab, self.id_to_token = self._build_vocab()
        self.max_len = 512
        
    def _build_vocab(self) -> Tuple[Dict[str, int], Dict[int, str]]:
        """Build comprehensive vocab for Indo+English+Termux"""
        # Base special tokens
        vocab = {token: idx for token, idx in self.special_tokens.items()}
        id_to_token = {idx: token for token, idx in vocab.items()}
        
        # Common Termux/Indo/English tokens (2000+)
        common_tokens = [
            # Greetings & basics
            'halo', 'hai', 'hello', 'hi', 'bye', 'selamat', 'terima', 'kasih',
            # Commands
            'install', 'pkg', 'cek', 'check', 'status', 'run', 'start', 'stop',
            'update', 'upgrade', 'remove', 'clean', 'list', 'search',
            # System
            'cpu', 'ram', 'memory', 'memori', 'storage', 'disk', 'free', 'df',
            'top', 'htop', 'uptime', 'load', 'process', 'kill',
            # Network
            'network', 'ip', 'wifi', 'ping', 'netstat', 'ss', 'route',
            # Dev tools
            'git', 'python', 'nodejs', 'npm', 'pip', 'flask', 'django',
            'nginx', 'apache', 'mysql', 'postgres', 'redis',
            # File ops
            'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'edit', 'nano',
            # Indonesian
            'siapa', 'apa', 'bagaimana', 'mengapa', 'kapan', 'dimana',
            'saya', 'kamu', 'dia', 'kami', 'mereka', 'ini', 'itu',
            # Numbers + punctuation
        ] + [f'{i}' for i in range(100)] + ['.', ',', '!', '?', ':']
        
        # Fill vocab
        for i, token in enumerate(common_tokens, 5):
            if i >= self.vocab_size:
                break
            vocab[token] = i
            id_to_token[i] = token
            
        self.console.print(f"[green]✓ Tokenizer vocab: {len(vocab)} tokens[/]")
        return vocab, id_to_token

    def encode(self, text: str, max_len: Optional[int] = None) -> List[int]:
        """Full encoding pipeline"""
        if max_len is None:
            max_len = self.max_len
            
        # 1. Clean & normalize
        text = self._clean_text(text)
        
        # 2. BPE tokenization
        tokens = self._bpe_tokenize(text)
        
        # 3. Convert to IDs
        token_ids = [self.vocab.get(token, self.special_tokens['UNK']) for token in tokens]
        
        # 4. Truncate + pad
        if len(token_ids) > max_len - 2:  # CLS + SEP
            token_ids = token_ids[:max_len-2]
        token_ids = [self.special_tokens['CLS']] + token_ids + [self.special_tokens['SEP']]
        
        # Pad
        padding_len = max_len - len(token_ids)
        token_ids += [self.special_tokens['PAD']] * padding_len
        
        return token_ids[:max_len]

    def batch_encode(self, texts: List[str], max_len: int = 512) -> np.ndarray:
        """Batch processing"""
        return np.array([self.encode(text, max_len) for text in texts])

    def decode(self, token_ids: List[int]) -> str:
        """Decode back to text"""
        tokens = [self.id_to_token.get(tid, '[UNK]') for tid in token_ids]
        # Remove special tokens
        text_tokens = [t for t in tokens if t not in ['[PAD]', '[CLS]', '[SEP]']]
        return ' '.join(text_tokens).strip()

    def _clean_text(self, text: str) -> str:
        """Advanced text cleaning"""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special chars but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\$\$]', ' ', text)
        # Lowercase
        text = text.lower().strip()
        return text

    def _bpe_tokenize(self, text: str) -> List[str]:
        """Byte Pair Encoding"""
        words = text.split()
        tokens = []
        
        for word in words:
            if word in self.vocab:
                tokens.append(word)
            else:
                # Subword splitting
                sub_tokens = self._split_subwords(word)
                tokens.extend(sub_tokens)
                
        return tokens

    def _split_subwords(self, word: str) -> List[str]:
        """Greedy BPE splitting"""
        if len(word) <= 3:
            return [word]
            
        for split_len in range(len(word), 2, -1):
            prefix = word[:split_len]
            if prefix in self.vocab:
                return [prefix] + self._split_subwords(word[split_len:])
                
        return [word]

    def get_stats(self) -> Dict:
        """Tokenizer statistics"""
        return {
            'vocab_size': self.vocab_size,
            'special_tokens': len(self.special_tokens),
            'max_len': self.max_len
        }

# Global instance
tokenizer = NanoTokenizer()
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class IntentMatch:
    name: str
    confidence: float
    entities: Dict[str, str]
    pattern: str

class NanoIntentEngine:
    def __init__(self):
        self.intent_patterns = self._load_patterns()
        self.entity_patterns = self._load_entities()
        
    def _load_patterns(self) -> Dict[str, List[Tuple[str, float]]]:
        return {
            'system_info': [(r'(cek|check)\s+(ram|cpu|memori|storage|disk)', 0.95), (r'(free|df|top|htop|uptime)', 0.90)],
            'package_install': [(r'(install|pasang|pkg)\s+(\w+)', 0.98), (r'pkg\s+(install|upgrade|update)', 0.92)],
            'network': [(r'(network|ip|wifi|ping|net)', 0.92), (r'(ip\s+addr|ifconfig|iwconfig)', 0.88)],
            'file_ops': [(r'(ls|dir|cd|mkdir|rm|cp|mv)', 0.95), (r'(cat|edit|nano|vim)\s+\S+', 0.90)],
            'greeting': [(r'(halo|hai|hello|hi|selamat)', 0.98)],
            'question': [(r'(siapa|apa|bagaimana|mengapa|kapan|dimana)', 0.85)]
        }

    def _load_entities(self) -> Dict[str, List[str]]:
        return {
            'package': ['python', 'git', 'nodejs', 'nginx', 'flask'],
            'resource': ['ram', 'cpu', 'disk', 'memory']
        }

    def detect(self, text: str) -> List[IntentMatch]:
        text_lower = text.lower()
        matches = []
        for intent_name, patterns in self.intent_patterns.items():
            for pattern_str, confidence in patterns:
                match = re.search(pattern_str, text_lower)
                if match:
                    entities = self._extract_entities(text_lower, match)
                    matches.append(IntentMatch(intent_name, confidence, entities, pattern_str))
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches[:3]

    def _extract_entities(self, text: str, match) -> Dict[str, str]:
        entities = {}
        for pkg in self.entity_patterns['package']:
            if pkg in text: entities['package'] = pkg
        if match.groups():
            for i, group in enumerate(match.groups()):
                if group: entities[f'arg{i}'] = group
        return entities

    def explain(self, text: str):
        matches = self.detect(text)
        print(f"\n--- Intent Analysis for: '{text}' ---")
        for m in matches:
            print(f"[{m.name}] Conf: {m.confidence:.2f} | Entities: {m.entities}")
        return matches if matches else None

intent_engine = NanoIntentEngine()

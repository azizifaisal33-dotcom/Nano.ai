"""
🎯 NanoIntentEngine v2 - Advanced NLU + Multi-label
Multi-intent detection with confidence scoring
"""
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import numpy as np
from dataclasses import dataclass
from rich.table import Table
from rich.console import Console

@dataclass
class IntentMatch:
    name: str
    confidence: float
    entities: Dict[str, str]
    pattern: str

class NanoIntentEngine:
    def __init__(self):
        self.console = Console()
        self.intent_patterns = self._load_patterns()
        self.entity_patterns = self._load_entities()
        
    def _load_patterns(self) -> Dict[str, List[Tuple[str, float]]]:
        """Intent pattern database"""
        patterns = {
            # System intents (high priority)
            'system_info': [
                (r'(cek|check)\s+(ram|cpu|memori|storage|disk)', 0.95),
                (r'(free|df|top|htop|uptime)', 0.90),
                (r'status?\s+(system|sistem)', 0.85)
            ],
            # Package management
            'package_install': [
                (r'(install|pasang|pkg)\s+(\w+)', 0.98),
                (r'pkg\s+(install|upgrade|update)', 0.92),
                (r'(apt|yum|dnf)\s+(install)', 0.88)
            ],
            # Network
            'network': [
                (r'(network|ip|wifi|ping|net)', 0.92),
                (r'(ip\s+addr|ifconfig|iwconfig)', 0.88),
                (r'(ping|traceroute|ss|netstat)', 0.85)
            ],
            # Development workflows
            'dev_workflow': [
                (r'(setup|buat|create)\s+(web|server|dev|project)', 0.90),
                (r'(flask|django|nginx|nodejs|react)', 0.85),
                (r'(git\s+(clone|init|push))', 0.82)
            ],
            # File operations
            'file_ops': [
                (r'(ls|dir|cd|mkdir|rm|cp|mv)', 0.95),
                (r'(cat|edit|nano|vim)\s+\S+', 0.90),
                (r'(find|grep|sed|awk)', 0.85)
            ],
            # General conversation
            'greeting': [
                (r'(halo|hai|hello|hi|selamat)', 0.98),
                (r'(apa\s+kabar|how\s+are\s+you)', 0.90)
            ],
            'question': [
                (r'(siapa|apa|bagaimana|mengapa|kapan|dimana|why|what|how|when|where)', 0.85),
                (r'\?$', 0.70)
            ]
        }
        return patterns

    def _load_entities(self) -> Dict[str, List[str]]:
        """Named Entity Recognition patterns"""
        return {
            'package': ['python', 'git', 'nodejs', 'nginx', 'flask', 'mysql', 'redis'],
            'command': ['ls', 'cd', 'rm', 'cp', 'mv', 'cat', 'grep', 'find'],
            'resource': ['ram', 'cpu', 'disk', 'memory', 'storage']
        }

    def detect(self, text: str) -> List[IntentMatch]:
        """Multi-intent detection with confidence"""
        text_lower = text.lower()
        matches = []
        
        for intent_name, patterns in self.intent_patterns.items():
            for pattern_str, confidence in patterns:
                match = re.search(pattern_str, text_lower)
                if match:
                    entities = self._extract_entities(text_lower, match)
                    matches.append(IntentMatch(
                        name=intent_name,
                        confidence=confidence,
                        entities=entities,
                        pattern=pattern_str
                    ))
        
        # Sort by confidence
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches[:3]  # Top 3 intents

    def _extract_entities(self, text: str, match) -> Dict[str, str]:
        """Extract entities from match"""
        entities = {}
        
        # Package names
        for pkg in self.entity_patterns['package']:
            if pkg in text:
                entities['package'] = pkg
                
        # Extract from regex groups
        if match.groups():
            for i, group in enumerate(match.groups()):
                if group:
                    entities[f'arg{i}'] = group
                    
        return entities

    def explain(self, text: str):
        """Explain intent detection"""
        matches = self.detect(text)
        table = Table(title="Intent Analysis")
        table.add_column("Intent", style="cyan")
        table.add_column("Confidence", justify="right")
        table.add_column("Entities")
        
        for match in matches:
            entities_str = ', '.join([f"{k}:{v}" for k,v in match.entities.items()])
            table.add_row(match.name, f"{match.confidence:.2f}", entities_str)
            
        self.console.print(table)
        return matches[0] if matches else None

# Global instance
intent_engine = NanoIntentEngine()
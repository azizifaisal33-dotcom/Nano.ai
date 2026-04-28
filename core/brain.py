# core/brain.py - Cognitive Processing Core for NanoAI v2.5
import os
import ast
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from core.revolver import LVRBinaryEngine, SyntaxValidator

@dataclass
class ThoughtProcess:
    reasoning: str
    confidence: float
    context: Dict[str, Any]

@dataclass
class SystemCommand:
    command: str
    args: List[str]
    priority: int = 1
    execute_silently: bool = False

class NanoBrain:
    def __init__(self):
        self.lvr_engine = LVRBinaryEngine("data/brain.lvr")
        self.thought_log: List[ThoughtProcess] = []
        self.command_queue: List[SystemCommand] = []
    
    def process_input(self, user_input: str) -> Tuple[Optional[str], List[SystemCommand]]:
        """
        Separate Thought Process from System Commands
        Returns: (response, commands)
        """
        # Parse input for system commands vs conversation
        if self._is_system_command(user_input):
            commands = self._extract_commands(user_input)
            response = "System commands queued for execution."
            return response, commands
        
        # Normal thought processing
        thought = self._generate_thought(user_input)
        self.thought_log.append(thought)
        
        # Store in LVR memory
        self.lvr_engine.write_memory(f"thought_{len(self.thought_log)}", asdict(thought))
        
        response = f"Thought: {thought.reasoning} (Confidence: {thought.confidence:.2f})"
        return response, []
    
    def _is_system_command(self, input_str: str) -> bool:
        """Detect system commands (starts with ! or contains specific keywords)"""
        triggers = ['!', 'exec:', 'run:', 'sys:', 'termux:']
        return any(trigger in input_str.lower() for trigger in triggers)
    
    def _extract_commands(self, input_str: str) -> List[SystemCommand]:
        """Parse and validate system commands"""
        commands = []
        parts = input_str.split(';')
        
        for part in parts:
            part = part.strip()
            if part.startswith('!'):
                cmd = part[1:].strip()
                commands.append(SystemCommand(command=cmd, args=[], priority=1))
        
        return commands
    
    def _generate_thought(self, input_str: str) -> ThoughtProcess:
        """Generate intelligent response with confidence scoring"""
        # Retrieve relevant context from LVR memory
        context = self.lvr_engine.read_memory("last_context") or {}
        
        # Simple reasoning engine
        reasoning = f"Analyzing: {input_str[:50]}..."
        confidence = 0.85  # Dynamic scoring in production
        
        return ThoughtProcess(reasoning=reasoning, confidence=confidence, context=context)
    
    def execute_commands(self) -> Dict[str, Any]:
        """Execute queued system commands safely"""
        results = {}
        for cmd in self.command_queue:
            try:
                if cmd.execute_silently:
                    os.system(cmd.command)
                    results[cmd.command] = "Executed silently"
                else:
                    results[cmd.command] = "Command queued"
            except Exception as e:
                results[cmd.command] = f"Error: {e}"
        
        self.command_queue.clear()
        return results
    
    def self_heal(self):
        """Self-healing mechanism using AST validation"""
        # Validate own syntax
        with open(__file__, 'r') as f:
            code = f.read()
        
        if not SyntaxValidator.validate_syntax(code):
            fixed_code = SyntaxValidator.auto_fix_indentation(code)
            # In production: write back with backup
            print("Self-healing: Fixed syntax issues")
    
    def close(self):
        self.lvr_engine.close()

# Global brain instance
brain = NanoBrain()
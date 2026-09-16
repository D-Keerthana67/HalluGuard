from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.app import analyze
samples=[
 ('Paris is the capital of France.','SUPPORTED'),
 ('Paris is the capital of Germany.','CONTRADICTED'),
 ('The Pacific Ocean is the largest ocean on Earth.','SUPPORTED'),
 ('Python was created by James Gosling.','CONTRADICTED')]
correct=0
for text,expected in samples:
    got=analyze(text)['claims'][0]['verdict']; correct+=got==expected; print(f'{got:20} expected={expected:20} {text}')
print(f'Accuracy: {correct/len(samples)*100:.1f}%')

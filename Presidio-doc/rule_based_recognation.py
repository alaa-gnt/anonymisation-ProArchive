from typing import List 
from presidio_analyzer import EntityRecognizer , RecognizerResult 
from presidio_analyzer.nlp_engine import NlpArtifacts

class MyRecognizer(EntityRecognizer):
    def load(self) -> None:
        pass
    
    def analyze(
            self , text: str , entities: List[str] , nlp_artifacts: NlpArtifacts 
    ) -> List[RecognizerResult]:
        pass
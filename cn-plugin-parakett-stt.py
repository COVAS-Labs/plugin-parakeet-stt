"""
Sherpa ONNX Parakeet STT Plugin for COVAS:NEXT
Provides offline Speech-to-Text capabilities using the Sherpa ONNX library and Parakeet model.
"""

from typing import override, Any
import os
import numpy as np
import speech_recognition as sr
import sherpa_onnx

from lib.PluginHelper import PluginHelper, STTModel
from lib.PluginSettingDefinitions import (
    PluginSettings,
    ModelProviderDefinition,
    SettingsGrid,
)
from lib.PluginBase import PluginBase, PluginManifest
from lib.Logger import log

class SherpaParakeetSTTModel(STTModel):
    """Sherpa ONNX Parakeet Speech-to-Text model implementation."""
    
    def __init__(self, model_dir: str):
        super().__init__("parakeet-stt")
        self.model_dir = model_dir
        self._recognizer = None
    
    def _get_recognizer(self) -> Any:
        """Lazily initialize the Sherpa recognizer."""
        if self._recognizer is None:
            if not os.path.exists(self.model_dir):
                raise ValueError(f"Model directory not found: {self.model_dir}")

            # Find model files in the directory
            files = os.listdir(self.model_dir)
            try:
                encoder = next(f for f in files if "encoder" in f and f.endswith(".onnx"))
                decoder = next(f for f in files if "decoder" in f and f.endswith(".onnx"))
                joiner = next(f for f in files if "joiner" in f and f.endswith(".onnx"))
                tokens = next(f for f in files if "tokens" in f and f.endswith(".txt"))
            except StopIteration:
                raise ValueError(f"Required model files (encoder, decoder, joiner, tokens) not found in {self.model_dir}")
            
            log('info', f"Loading Sherpa Parakeet model from {self.model_dir}")
            
            try:
                self._recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
                    encoder=os.path.join(self.model_dir, encoder),
                    decoder=os.path.join(self.model_dir, decoder),
                    joiner=os.path.join(self.model_dir, joiner),
                    tokens=os.path.join(self.model_dir, tokens),
                    num_threads=1,
                    model_type="nemo_transducer",
                    debug=False
                )
            except Exception as e:
                log('error', f"Failed to initialize Sherpa recognizer: {e}")
                raise

        return self._recognizer
    
    def transcribe(self, audio: sr.AudioData) -> str:
        """Transcribe audio using Sherpa ONNX."""
        try:
            recognizer = self._get_recognizer()
            
            # Convert audio to 16kHz 16-bit mono PCM
            # get_raw_data returns bytes
            raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            
            # Convert to float32 array normalized to [-1, 1]
            samples = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            stream = recognizer.create_stream()
            stream.accept_waveform(16000, samples)
            recognizer.decode_stream(stream)
            
            text = stream.result.text
            return text.strip()
            
        except Exception as e:
            log('error', f"Sherpa STT transcription failed: {e}")
            raise

class SherpaParakeetPlugin(PluginBase):
    """
    Plugin providing Sherpa ONNX Parakeet Speech-to-Text services.
    """
    
    def __init__(self, plugin_manifest: PluginManifest):
        super().__init__(plugin_manifest)
        
        self.settings = {
            PluginSettings(
                key="Parakeet STT",
                label="Parakeet STT",
                icon="mic",
                grids=[
                    SettingsGrid(
                        key="general",
                        label="General",
                        fields=[
                            ParagraphSetting(
                                key="info_text",
                                label=None,
                                type="paragraph",
                                readonly=False,
                                placeholder=None,
                                
                                content="To use Parakeet STT, select it as your *STT provider* in *Advanced → STT Settings*."
                            ),
                        ]
                    ),
                ]
            )
        }
        
        self.model_providers = [
            ModelProviderDefinition(
                kind='stt',
                id='parakeet-stt',
                label='Parakeet STT (Offline)',
                settings_config=[] # No settings needed as model path is hardcoded
            )
        ]
    
    @override
    def create_model(self, provider_id: str, settings: dict[str, Any]) -> STTModel:
        """Create a model instance for the given provider."""
        
        if provider_id == 'parakeet-stt':
            # Model is expected to be in a 'model' subdirectory relative to this file
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(plugin_dir, "model")
            
            return SherpaParakeetSTTModel(model_dir=model_dir)
        
        raise ValueError(f'Unknown Sherpa provider: {provider_id}')

if __name__ == "__main__":
    # For testing purposes
    plugin_manifest = PluginManifest(
        name="Sherpa Parakeet STT Plugin",
        version="1.0.0",
        author="OpenAI",
        description="Sherpa ONNX Parakeet STT Plugin for COVAS:NEXT"
    )
    plugin = SherpaParakeetPlugin(plugin_manifest)
    model = plugin.create_model('parakeet-stt', {})
    log('info', "Parakeet STT Plugin initialized successfully.")
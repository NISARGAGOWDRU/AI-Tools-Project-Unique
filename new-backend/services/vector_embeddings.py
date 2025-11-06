import numpy as np
import re
import json
import asyncio
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VectorEmbeddingService:
    """Service for generating semantic chunks and vector embeddings"""
    
    def __init__(self):
        self.model = None
        self._model_loaded = False
    
    async def _load_model(self):
        """Load sentence transformer model"""
        if self._model_loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self._model_loaded = True
            logger.info("✅ Sentence transformer model loaded")
        except ImportError:
            logger.error("❌ sentence-transformers not installed")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
    
    def _semantic_chunk(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """Split text into semantic chunks"""
        if not text.strip():
            return []
        
        # Split by sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_chunk_size and current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks
    
    async def create_embeddings(self, page_data: Dict[str, Any], page_number: int) -> Dict[str, Any]:
        """Create embeddings for page content"""
        await self._load_model()
        
        # Extract text content
        content = page_data.get("text", "").strip()
        if not content:
            html_content = page_data.get("html", "").strip()
            if html_content:
                content = re.sub(r'<[^>]+>', ' ', html_content)
                content = re.sub(r'\s+', ' ', content).strip()
        
        if not content:
            logger.warning(f"No content found for page {page_number}")
            return {
                "embeddings": np.array([], dtype=np.float32).reshape(0, 384),
                "metadata": {
                    "page_number": page_number,
                    "chunks": [],
                    "chunk_count": 0
                }
            }
        
        # Create semantic chunks
        chunks = self._semantic_chunk(content)
        logger.info(f"Created {len(chunks)} chunks for page {page_number}")
        
        if not chunks:
            return {
                "embeddings": np.array([], dtype=np.float32).reshape(0, 384),
                "metadata": {
                    "page_number": page_number,
                    "chunks": [],
                    "chunk_count": 0
                }
            }
        
        # Generate embeddings
        embeddings = await asyncio.to_thread(self.model.encode, chunks)
        embeddings = embeddings.astype(np.float32)
        
        metadata = {
            "page_number": page_number,
            "chunks": chunks,
            "chunk_count": len(chunks)
        }
        
        logger.info(f"Generated embeddings shape: {embeddings.shape} for page {page_number}")
        return {
            "embeddings": embeddings,
            "metadata": metadata
        }

# Global service instance
_embedding_service = None

async def get_embedding_service() -> VectorEmbeddingService:
    """Get or create embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = VectorEmbeddingService()
    return _embedding_service

async def create_page_embeddings(page_data: Dict[str, Any], page_number: int, embeddings_dir: Path) -> None:
    """Create and save page embeddings"""
    try:
        service = await get_embedding_service()
        result = await service.create_embeddings(page_data, page_number)
        
        # Save embeddings as .npy file
        embeddings_file = embeddings_dir / f"page_{page_number}_embeddings.npy"
        await asyncio.to_thread(np.save, embeddings_file, result["embeddings"])
        
        # Save metadata as JSON
        metadata_file = embeddings_dir / f"page_{page_number}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(result["metadata"], f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved embeddings for page {page_number}: {result['embeddings'].shape}")
        
    except Exception as e:
        logger.error(f"❌ Failed to create embeddings for page {page_number}: {e}")
        raise
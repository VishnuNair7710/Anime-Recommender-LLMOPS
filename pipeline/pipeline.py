from src.vector_store import VectorStore
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommenderPipeline:
    def __init__(self, csv_path: str, persist_dir: str = "chroma_db"):
        try:
            logger.info("Initializing Anime Recommender Pipeline...")
            vector_store = VectorStore(csv_path=csv_path, persist_dir=persist_dir)
            # Build and save the vector store first
            vector_store.build_and_save_vectorstore()
            # Then get the retriever
            db = vector_store.get_vectorstore()
            # Create retriever from the vectorstore
            retriever = db.as_retriever()
            self.recommender = AnimeRecommender(retriever, GROQ_API_KEY, MODEL_NAME)
            logger.info("Anime Recommender Pipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Anime Recommender Pipeline: {e}")
            raise CustomException("Failed to initialize Anime Recommender Pipeline", e)
        

    def recommend(self, query: str):
        try:
            logger.info(f"Getting recommendation for query: {query}")
            recommendation = self.recommender.get_recommndation(query)
            logger.info("Recommendation generated successfully.")
            return recommendation
        except Exception as e:
            logger.error(f"Error getting recommendation: {e}")
            raise CustomException("Failed to get recommendation", e) from e
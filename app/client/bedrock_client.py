import boto3
import json
from typing import Dict, Any, Optional, List
from botocore.exceptions import ClientError, NoCredentialsError
import logging

from pydantic import BaseModel, Field

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


## Valid Request Model
class ChatRequest(BaseModel):
    user_prompt: str = Field(min_length=3)
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9


class BedrockClient:
    """
    Client générique pour Amazon Bedrock permettant d'interagir avec différents modèles
    """
    
    def __init__(
        self,
        region_name: Optional[str] = "eu-west-1",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None
    ):
        """
        Initialise le client Bedrock
        
        Args:
            region_name: Région AWS (par défaut eu-west-1)
            aws_access_key_id: Clé d'accès AWS (optionnel si configuré via ~/.aws/credentials)
            aws_secret_access_key: Clé secrète AWS (optionnel si configuré via ~/.aws/credentials)
            aws_session_token: Token de session AWS (optionnel)
        """
        self.region_name = region_name
        
        try:
            # Configuration des credentials
            session_kwargs = {"region_name": region_name}
            
            if aws_access_key_id and aws_secret_access_key:
                session_kwargs.update({
                    "aws_access_key_id": aws_access_key_id,
                    "aws_secret_access_key": aws_secret_access_key
                })
                
                if aws_session_token:
                    session_kwargs["aws_session_token"] = aws_session_token
            
            # Création de la session boto3
            self.session = boto3.Session(**session_kwargs)
            
            # Clients Bedrock
            self.bedrock_runtime = self.session.client("bedrock-runtime")
            self.bedrock = self.session.client("bedrock")
            
            logger.info(f"Client Bedrock initialisé pour la région {region_name}")
            
        except NoCredentialsError:
            logger.error("Credentials AWS non trouvés. Configurez vos credentials.")
            raise
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client Bedrock: {str(e)}")
            raise
    
    def list_foundation_models(self) -> List[Dict[str, Any]]:
        """
        Liste tous les modèles fondamentaux disponibles
        
        Returns:
            Liste des modèles disponibles
        """
        try:
            response = self.bedrock.list_foundation_models()
            return response.get("modelSummaries", [])
        except ClientError as e:
            logger.error(f"Erreur lors de la récupération des modèles: {str(e)}")
            raise
    
    def invoke_model(
        self,
        model_id: str,
        request: ChatRequest,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Invoque un modèle Bedrock avec des paramètres génériques
        
        Args:
            model_id: ID du modèle (ex: "anthropic.claude-3-sonnet-20240229-v1:0")
            prompt: Prompt à envoyer au modèle
            max_tokens: Nombre maximum de tokens à générer
            temperature: Température pour le sampling (0.0 à 1.0)
            top_p: Top-p pour le sampling
            **kwargs: Paramètres additionnels spécifiques au modèle
        
        Returns:
            Réponse du modèle
        """
        try:
            # Invocation du modèle
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": request.max_tokens,
                    "temperature": request.temperature,
                    "top_p": request.top_p,
                    "messages": [
                        {
                            "role": "user",
                            "content": request.user_prompt
                        }
                    ],
                    **kwargs
                }),
                contentType="application/json",
                accept="application/json"
            )
            
            # Parsing de la réponse
            response_body = json.loads(response["body"].read())
            
            logger.info(f"Modèle {model_id} invoqué avec succès")
            return response_body
            
        except ClientError as e:
            logger.error(f"Erreur lors de l'invocation du modèle {model_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}")
            raise
    
    def invoke_model_with_streaming(
        self,
        model_id: str,
        request: ChatRequest,
        **kwargs
    ):
        """
        Invoque un modèle en streaming
        
        Args:
            model_id: ID du modèle
            prompt: Prompt à envoyer
            max_tokens: Nombre maximum de tokens
            temperature: Température
            top_p: Top-p
            **kwargs: Paramètres additionnels
        
        Yields:
            Chunks de réponse en streaming
        """
        try:
            response = self.bedrock_runtime.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": request.max_tokens,
                    "temperature": request.temperature,
                    "top_p": request.top_p,
                    "messages": [
                        {
                            "role": "user",
                            "content": request.user_prompt
                        }
                    ],
                    **kwargs
                }),
                contentType="application/json",
                accept="application/json"
            )
            
            for event in response["body"]:
                if "chunk" in event:
                    chunk_data = json.loads(event["chunk"]["bytes"])
                    yield chunk_data
                    
        except ClientError as e:
            logger.error(f"Erreur lors du streaming du modèle {model_id}: {str(e)}")
            raise
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Récupère les informations d'un modèle spécifique
        
        Args:
            model_id: ID du modèle
        
        Returns:
            Informations du modèle
        """
        try:
            response = self.bedrock.get_foundation_model(modelIdentifier=model_id)
            return response.get("modelDetails", {})
        except ClientError as e:
            logger.error(f"Erreur lors de la récupération des infos du modèle {model_id}: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Teste la connexion au service Bedrock
        
        Returns:
            True si la connexion fonctionne, False sinon
        """
        try:
            self.list_foundation_models()
            logger.info("Connexion à Bedrock réussie")
            return True
        except Exception as e:
            logger.error(f"Échec de la connexion à Bedrock: {str(e)}")
            return False
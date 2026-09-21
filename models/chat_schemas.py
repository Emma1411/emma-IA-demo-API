from typing import Any, Dict, List, Literal
from pydantic import BaseModel, Field, field_validator


MAX_ITEMS_LISTE = 50
MAX_MESSAGES = 40


class MessageHistorique(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    donnees_dossier: Dict[str, Any] = Field(default_factory=dict)

    metriques_officielles_calculees: Dict[str, Any] = Field(
        default_factory=dict
    )

    champs_obligatoires_pour_ce_produit: List[str] = Field(
        default_factory=list,
        max_length=MAX_ITEMS_LISTE,
    )

    hypotheses_existantes: List[Dict[str, Any]] = Field(
        default_factory=list,
        max_length=MAX_ITEMS_LISTE,
    )

    messages: List[MessageHistorique] = Field(
        ...,
        min_length=1,
        max_length=MAX_MESSAGES,
    )

    @field_validator("messages")
    @classmethod
    def valider_dernier_message(
        cls,
        v: List[MessageHistorique],
    ) -> List[MessageHistorique]:
        # Le dernier message doit toujours venir de l'utilisateur
        if v[-1].role != "user":
            raise ValueError(
                "Le dernier message de 'messages' doit être 'user'"
            )

        return v


class ChatResponse(BaseModel):
    mode: Literal["chat", "analyse_complete"]
    reponse: Dict[str, Any]

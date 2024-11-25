from datetime import datetime
from typing import Optional, List


class Thread:
    def __init__(
        self,
        code: int,
        type: str,
        status: str,
        subject: str,
        snippet: str,
        summary: str,
        notes: Optional[str] = None,
        contact: Optional[dict] = None,
        main_contact: Optional[dict] = None,
        thread_id: Optional[str] = None,
        estimated_cost: Optional[float] = None,
        created_by: Optional[dict] = None,
        updated_by: Optional[dict] = None,
        user: Optional[dict] = None,
    ):
        # Campos obrigatórios
        self.code = code
        self.type = type  # "Chat", "Email", "WhatsApp"
        self.status = status  # "Em Andamento", "Concluído", "Aguardando"
        self.subject = subject
        self.snippet = snippet
        self.summary = summary

        # Campos opcionais
        self.notes = notes
        self.contact = contact  # {"name": str, "email": str, "phone": str}
        self.main_contact = main_contact  # {"name.full": str, "email": str, "phone": str}
        self.thread_id = thread_id
        self.estimated_cost = estimated_cost

        # Metadados de criação e atualização
        self._created_at = datetime.now()
        self._created_by = created_by  # {"name": str, "group.name": str}
        self._updated_at = datetime.now()
        self._updated_by = updated_by
        self._user = user  # {"name": str, "email": str}

    def update_status(self, new_status: str):
        """
        Atualiza o status do atendimento.
        :param new_status: Novo status ("Em Andamento", "Concluído", "Aguardando").
        """
        valid_statuses = ["Em Andamento", "Concluído", "Aguardando"]
        if new_status not in valid_statuses:
            raise ValueError(f"Status inválido: {new_status}. Escolha entre {valid_statuses}.")
        self.status = new_status
        self._updated_at = datetime.now()

    def add_notes(self, additional_notes: str):
        """
        Adiciona notas ao atendimento.
        :param additional_notes: Notas adicionais para o atendimento.
        """
        if self.notes:
            self.notes += f"\n{additional_notes}"
        else:
            self.notes = additional_notes
        self._updated_at = datetime.now()

    def assign_user(self, user: dict):
        """
        Designa um usuário para o atendimento.
        :param user: Dicionário contendo informações do usuário {"name": str, "email": str}.
        """
        self._user = user
        self._updated_at = datetime.now()

    def to_dict(self):
        """
        Converte o objeto Thread em um dicionário para facilitar a visualização ou armazenamento.
        :return: Dicionário representando o atendimento.
        """
        return {
            "code": self.code,
            "type": self.type,
            "status": self.status,
            "subject": self.subject,
            "snippet": self.snippet,
            "summary": self.summary,
            "notes": self.notes,
            "contact": self.contact,
            "main_contact": self.main_contact,
            "thread_id": self.thread_id,
            "estimated_cost": self.estimated_cost,
            "_created_at": self._created_at.isoformat(),
            "_created_by": self._created_by,
            "_updated_at": self._updated_at.isoformat(),
            "_updated_by": self._updated_by,
            "_user": self._user,
        }


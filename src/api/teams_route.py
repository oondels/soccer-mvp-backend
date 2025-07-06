from datetime import datetime
from flask import Blueprint, request, jsonify
from src.models.teams import Team
from src.models.team_players import TeamPlayer
from src.database.db import db

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")
teamModel = db.select(Team)

@teams_bp.route("/", methods=["POST"])
def create_team():
    """
    Cria uma nova equipe
    ---
    tags:
      - Teams
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: Nome da equipe (obrigatório)
              description:
                type: string
                description: Descrição da equipe (opcional)
              team_profile_image:
                type: string
                description: URL da imagem de perfil da equipe (opcional)
              team_banner_image:
                type: string
                description: URL da imagem de banner da equipe (opcional)
              captain_id:
                type: integer
                description: ID do capitão da equipe (opcional)
              notes:
                type: string
                description: Observações adicionais (opcional)
            required:
              - name
    responses:
      201:
        description: Equipe criada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: object
                  properties:
                    team_id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    captain_id:
                      type: integer
                    is_active:
                      type: boolean
                    ranking_points:
                      type: integer
                    members_count:
                      type: integer
                    create_date:
                      type: string
      400:
        description: Validation error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
      500:
        description: Database error
    """
    team_data = request.get_json()

    if not team_data:
        return jsonify({
            "error": "Invalid request",
            "message": "Informações Ausentes. JSON data é obrigatório."
        }), 400
    
    if "name" not in team_data or not team_data.get("name"):
        return jsonify({
            "error": "Validation error",
            "message": "O campo 'name' é obrigatório e não pode estar vazio"
        }), 400
    
    team_name = team_data.get("name").strip()
    if len(team_name) < 2:
        return jsonify({
            "error": "Validation error",
            "message": "O nome da equipe deve ter pelo menos 2 caracteres"
        }), 400
    
    if len(team_name) > 255:
        return jsonify({
            "error": "Validation error",
            "message": "O nome da equipe não pode exceder 255 caracteres"
        }), 400
    
    description = team_data.get("description")
    if description and len(description) > 350:
        return jsonify({
            "error": "Validation error",
            "message": "A descrição não pode exceder 350 caracteres"
        }), 400
        
    captain_id = team_data.get("captain_id")
    if captain_id and not isinstance(captain_id, int):
        return jsonify({
            "error": "Validation error",
            "message": "O ID do capitão deve ser um número inteiro válido"
        }), 400
    
    notes = team_data.get("notes")
    if notes and len(notes) > 350:
        return jsonify({
            "error": "Validation error",
            "message": "As notas não podem exceder 350 caracteres"
        }), 400

    try:
        new_team = Team(name=team_name)
        
        if description:
            new_team.description = description.strip()
        if team_data.get("team_profile_image"):
            new_team.team_profile_image = team_data.get("team_profile_image")
        if team_data.get("team_banner_image"):
            new_team.team_banner_image = team_data.get("team_banner_image")
        if captain_id:
            new_team.captain_id = captain_id
        if notes:
            new_team.notes = notes.strip()

        db.session.add(new_team)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Equipe criada com sucesso",
            "data": {
                "team_id": new_team.id,
                "name": new_team.name,
                "description": new_team.description,
                "captain_id": new_team.captain_id,
                "is_active": new_team.is_active,
                "ranking_points": new_team.ranking_points,
                "members_count": new_team.members_count,
                "create_date": new_team.create_date.isoformat() if new_team.create_date else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Falha ao criar equipe. Por favor, tente novamente."
        }), 500


@teams_bp.route("/<int:team_id>", methods=["PUT"])
def edit_team(team_id):
    """
    Atualiza uma equipe existente
    ---
    tags:
      - Teams
    parameters:
      - in: path
        name: team_id
        required: true
        schema:
          type: integer
        description: O ID da equipe a ser atualizada
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: Nome da equipe (opcional)
              description:
                type: string
                description: Descrição da equipe (opcional)
              team_profile_image:
                type: string
                description: URL da imagem de perfil da equipe (opcional)
              team_banner_image:
                type: string
                description: URL da imagem de banner da equipe (opcional)
              captain_id:
                type: integer
                description: ID do capitão da equipe (opcional)
              notes:
                type: string
                description: Notas adicionais (opcional)
    responses:
      200:
        description: Equipe atualizada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: object
                  properties:
                    team_id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    team_profile_image:
                      type: string
                    team_banner_image:
                      type: string
                    captain_id:
                      type: integer
                    notes:
                      type: string
                    is_active:
                      type: boolean
                    ranking_points:
                      type: integer
                    members_count:
                      type: integer
                    create_date:
                      type: string
                    update_date:
                      type: string
      400:
        description: Erro de validação
      404:
        description: Equipe não encontrada
      500:
        description: Erro no banco de dados
    """
    team_data = request.get_json()
    print(team_data)
    if not team_data:
        return jsonify({
            "error": "Invalid request",
            "message": "JSON data is required"
        }), 400
    
    try:
        team = db.session.get(Team, team_id)
        if not team:
            return jsonify({
                "error": "Not found",
                "message": f"Team with ID {team_id} not found"
            }), 404
        
        if "name" in team_data:
            team_name = team_data.get("name")
            if not team_name or not team_name.strip():
                return jsonify({
                    "error": "Validation error",
                    "message": "Field 'name' cannot be empty"
                }), 400
            
            team_name = team_name.strip()
            if len(team_name) < 2:
                return jsonify({
                    "error": "Validation error",
                    "message": "Team name must be at least 2 characters long"
                }), 400
            
            if len(team_name) > 255:
                return jsonify({
                    "error": "Erro de validação",
                    "message": "O nome da equipe não pode exceder 255 caracteres"
                }), 400
            
            team.name = team_name

        if "description" in team_data:
            description = team_data.get("description")
            if description and len(description) > 350:
                return jsonify({
                    "error": "Erro de validação",
                    "message": "A descrição não pode exceder 350 caracteres"
                }), 400
            team.description = description.strip() if description else None
        
        if "team_profile_image" in team_data:
            team.team_profile_image = team_data.get("team_profile_image")
        
        if "team_banner_image" in team_data:
            team.team_banner_image = team_data.get("team_banner_image")
        
        if "captain_id" in team_data:
            captain_id = team_data.get("captain_id")
            if captain_id is not None and not isinstance(captain_id, int):
                return jsonify({
                    "error": "Erro de validação",
                    "message": "O ID do capitão deve ser um número inteiro válido"
                }), 400
            team.captain_id = captain_id
        
        if "notes" in team_data:
            notes = team_data.get("notes")
            if notes and len(notes) > 350:
                return jsonify({
                    "error": "Erro de validação",
                    "message": "As notas não podem exceder 350 caracteres"
                }), 400
            team.notes = notes.strip() if notes else None
        
        team.update_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Equipe atualizada com sucesso",
            "data": {
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "team_profile_image": team.team_profile_image,
                "team_banner_image": team.team_banner_image,
                "captain_id": team.captain_id,
                "notes": team.notes,
                "is_active": team.is_active,
                "ranking_points": team.ranking_points,
                "members_count": team.members_count,
                "create_date": team.create_date.isoformat() if team.create_date else None,
                "update_date": team.update_date.isoformat() if team.update_date else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erro no banco de dados",
            "message": "Falha ao atualizar equipe. Por favor, tente novamente."
        }), 500


@teams_bp.route("/", methods=["GET"])
def get_teams():
    """
    Obter todas as equipes
    ---
    tags:
      - Teams
    responses:
      200:
        description: Lista de equipes recuperada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      team_id:
                        type: integer
                      name:
                        type: string
                      description:
                        type: string
                      team_profile_image:
                        type: string
                      team_banner_image:
                        type: string
                      captain_id:
                        type: integer
                      is_active:
                        type: boolean
                      ranking_points:
                        type: integer
                      members_count:
                        type: integer
                      create_date:
                        type: string
                      update_date:
                        type: string
    """
    try:
        teams = db.session.execute(teamModel.order_by(Team.id)).scalars().all()
        
        team_list = [
            {
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "team_profile_image": team.team_profile_image,
                "team_banner_image": team.team_banner_image,
                "captain_id": team.captain_id,
                "is_active": team.is_active,
                "ranking_points": team.ranking_points,
                "members_count": team.members_count,
                "create_date": team.create_date.isoformat() if team.create_date else None,
                "update_date": team.update_date.isoformat() if team.update_date else None
            }
            for team in teams
        ]
        
        return jsonify({
            "success": True,
            "message": "Equipes encontradas com sucesso",
            "data": team_list
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Erro no banco de dados",
            "message": "Falha ao encontrar equipes. Por favor, tente novamente."
        }), 500


@teams_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    """
    Obter uma equipe por ID
    ---
    tags:
      - Teams
    parameters:
      - in: path
        name: team_id
        required: true
        schema:
          type: integer
        description: O ID da equipe a ser recuperada
    responses:
      200:
        description: Equipe encontrada
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: object
                  properties:
                    team_id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    team_profile_image:
                      type: string
                    team_banner_image:
                      type: string
                    captain_id:
                      type: integer
                    notes:
                      type: string
                    is_active:
                      type: boolean
                    ranking_points:
                      type: integer
                    members_count:
                      type: integer
                    create_date:
                      type: string
                    update_date:
                      type: string
      404:
        description: Equipe não encontrada
      500:
        description: Erro no banco de dados
    """
    try:
        team = db.session.get(Team, team_id)
        if not team:
            return jsonify({
                "error": "Não encontrado",
                "message": f"Equipe não encontrada"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Equipe encontrada com sucesso",
            "data": {
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "team_profile_image": team.team_profile_image,
                "team_banner_image": team.team_banner_image,
                "captain_id": team.captain_id,
                "notes": team.notes,
                "is_active": team.is_active,
                "ranking_points": team.ranking_points,
                "members_count": team.members_count,
                "create_date": team.create_date.isoformat() if team.create_date else None,
                "update_date": team.update_date.isoformat() if team.update_date else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Erro no banco de dados",
            "message": "Falha ao encontrar equipe. Por favor, tente novamente."
        }), 500


@teams_bp.route("/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    """
    Deletar uma equipe por ID
    ---
    tags:
      - Teams
    parameters:
      - in: path
        name: team_id
        required: true
        schema:
          type: integer
        description: O ID da equipe a ser deletada
    responses:
      200:
        description: Equipe deletada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
      404:
        description: Equipe não encontrada
      500:
        description: Erro no banco de dados
    """
    try:
        team = db.session.get(Team, team_id)
        if not team:
            return jsonify({
                "error": "Não encontrado",
                "message": f"Equipe não encontrada. Tente novamente."
            }), 404
        
        db.session.delete(team)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Equipe deletada com sucesso"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Erro no banco de dados",
            "message": "Falha ao deletar equipe. Por favor, tente novamente."
        }), 500


@teams_bp.route("/<int:team_id>/players", methods=["POST"])
def add_team_player(team_id):
    """
    Adicionar um jogador a uma equipe
    ---
    tags:
      - Teams
    parameters:
      - in: path
        name: team_id
        required: true
        schema:
          type: integer
        description: O ID da equipe
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id:
                type: integer
                description: ID do usuário a ser adicionado à equipe (obrigatório)
            required:
              - user_id
    responses:
      201:
        description: Jogador adicionado à equipe com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                    user_id:
                      type: integer
                    team_id:
                      type: integer
                    create_date:
                      type: string
      400:
        description: Erro de validação
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                message:
                  type: string
      404:
        description: Equipe não encontrada
      409:
        description: Jogador já está na equipe
      500:
        description: Erro no banco de dados
    """
    player_data = request.get_json()
    
    if not player_data:
        return jsonify({
            "error": "Invalid request",
            "message": "JSON data é obrigatório."
        }), 400
    
    if "user_id" not in player_data or not player_data.get("user_id"):
        return jsonify({
            "error": "Validation error",
            "message": "É obrigatório fornecer um usuário válido."
        }), 400
    
    user_id = player_data.get("user_id")
    if not isinstance(user_id, int):
        return jsonify({
            "error": "Validation error",
            "message": "O ID do usuário deve ser um número inteiro válido"
        }), 400
    
    try:
        team = db.session.get(Team, team_id)
        if not team:
            return jsonify({
                "error": "Not found",
                "message": "Equipe não encontrada"
            }), 404
        
        existing_player = db.session.query(TeamPlayer).filter_by(
            user_id=user_id, team_id=team_id
        ).first()
        
        if existing_player:
            return jsonify({
                "error": "Conflict",
                "message": "Jogador já está nesta equipe"
            }), 409
        
        new_team_player = TeamPlayer(user_id=user_id, team_id=team_id)
        
        db.session.add(new_team_player)
        
        team.members_count += 1
        team.update_date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Jogador adicionado à equipe com sucesso",
            "data": {
                "id": new_team_player.id,
                "user_id": new_team_player.user_id,
                "team_id": new_team_player.team_id,
                "create_date": new_team_player.create_date.isoformat() if new_team_player.create_date else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Falha ao adicionar jogador à equipe. Por favor, tente novamente."
        }), 500

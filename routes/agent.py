# ===============================================================================
# Agent routes blueprints
# ===============================================================================

from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.agent import Agent
from schemas.agent import AgentSchema

agent_bp = Blueprint('agents', __name__)


# Get all agents with pagination
# ===============================================================================
@agent_bp.route('/api/agents/', methods=['GET'])
def get_agents():
    """Get all agents with pagination."""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=6, type=int)

    agents_paginated = Agent.query.paginate(page=page, per_page=limit, error_out=False)

    agents_schema = AgentSchema(many=True)
    result = agents_schema.dump(agents_paginated.items)

    response = {
        'agents': result,
        'total_agents': agents_paginated.total,
        'total_pages': agents_paginated.pages,
        'current_page': agents_paginated.page,
        'has_next': agents_paginated.has_next,
        'has_prev': agents_paginated.has_prev
    }

    return make_response(jsonify(response), 200)


# Get agent by ID
# ===============================================================================
@agent_bp.route('/api/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent by ID."""
    agent = Agent.query.get_or_404(agent_id)

    # Serialize policies
    policies = []
    for p in agent.policies:
        policies.append({
            "policy_id": p.policy_id,
            "status": getattr(p, "status", None),
            "start_date": p.start_date.isoformat() if getattr(p, "start_date", None) else None,
            "end_date": p.end_date.isoformat() if getattr(p, "end_date", None) else None
        })

    response = {
        "agent_id": agent.agent_id,
        "name": agent.name,
        "email": agent.email,
        "phone": agent.phone,
        "policies": policies
    }

    return jsonify(response), 200


# Create agent
# ===============================================================================
@agent_bp.route('/api/agents', methods=['POST'])
def create_agent():
    """Create a new agent."""
    data = request.get_json()
    agent_schema = AgentSchema()
    new_agent = agent_schema.load(data)
    db.session.add(new_agent)
    db.session.commit()
    result = agent_schema.dump(new_agent)
    return make_response(jsonify({'message': 'Agent created successfully', 'agent': result}), 201)


# Update agent
# ===============================================================================
@agent_bp.route('/api/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an existing agent."""
    agent = Agent.query.get_or_404(agent_id)
    data = request.get_json()

    agent_schema = AgentSchema()
    updated_agent = agent_schema.load(data, instance=agent, partial=True)

    db.session.commit()
    result = agent_schema.dump(updated_agent)

    return make_response(jsonify({'message': 'Agent updated successfully', 'agent': result}), 200)


# Delete agent
# ===============================================================================
@agent_bp.route('/api/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent."""
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return make_response(jsonify({'message': 'Agent deleted successfully'}), 200)

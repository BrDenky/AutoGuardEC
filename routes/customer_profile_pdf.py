from flask import Blueprint, render_template, Response
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
from extensions import db
from models.customer import Customer
from models.vehicle import Vehicle
from models.policy import Policy
from models.agent import Agent
from models.claim import Claim
from models.premium_payment import PremiumPayment
from models.claim_payment import ClaimPayment
from sqlalchemy import func

customer_profile_pdf_bp = Blueprint('customer_profile_pdf', __name__)

@customer_profile_pdf_bp.route('/api/customers/<int:customer_id>/profile/pdf')
def generate_customer_profile_pdf(customer_id):
    """
    Generate a comprehensive PDF profile for a specific customer
    showing all related data: vehicles, policies, claims, payments, agent info
    """
    
    # Get customer or return 404
    customer = Customer.query.get_or_404(customer_id)
    
    # Build customer full name
    customer_name = f"{customer.first_name} {customer.last_name}"
    
    # ========================================================================
    # VEHICLES - Get all vehicles owned by this customer
    # ========================================================================
    vehicles = Vehicle.query.filter_by(customer_id=customer_id).all()
    vehicles_data = []
    for v in vehicles:
        vehicles_data.append({
            'vehicle_id': v.vehicle_id,
            'brand': v.brand,
            'model': v.model,
            'year': v.year,
            'license_plate': v.license_plate
        })
    
    # ========================================================================
    # POLICIES - Get all policies for this customer with related data
    # ========================================================================
    policies = Policy.query.filter_by(customer_id=customer_id).all()
    policies_data = []
    agent_info = None
    
    for p in policies:
        # Get agent info (assuming all policies have same agent, take first)
        if not agent_info and p.agent:
            agent_info = {
                'agent_id': p.agent.agent_id,
                'name': p.agent.name,
                'phone': p.agent.phone,
                'email': p.agent.email
            }
        
        # Get vehicle info for this policy
        vehicle_info = None
        if p.vehicle:
            vehicle_info = f"{p.vehicle.brand} {p.vehicle.model} ({p.vehicle.license_plate})"
        
        # Get premium payments for this policy
        premium_payments = PremiumPayment.query.filter_by(policy_id=p.policy_id).all()
        total_premiums_paid = sum([float(pp.amount) for pp in premium_payments])
        
        # Get claims for this policy
        claims = Claim.query.filter_by(policy_id=p.policy_id).all()
        claims_count = len(claims)
        
        policies_data.append({
            'policy_id': p.policy_id,
            'vehicle': vehicle_info,
            'start_date': p.start_date.strftime('%Y-%m-%d') if p.start_date else 'N/A',
            'end_date': p.end_date.strftime('%Y-%m-%d') if p.end_date else 'N/A',
            'status': p.status,
            'total_premiums': total_premiums_paid,
            'claims_count': claims_count,
            'premium_payments': premium_payments
        })
    
    # ========================================================================
    # CLAIMS - Get all claims for customer's policies
    # ========================================================================
    # Get all policy IDs for this customer
    policy_ids = [p.policy_id for p in policies]
    
    claims_data = []
    total_claim_amount = 0
    
    if policy_ids:
        claims = Claim.query.filter(Claim.policy_id.in_(policy_ids)).all()
        
        for c in claims:
            # Get claim payments
            claim_payments = ClaimPayment.query.filter_by(claim_id=c.claim_id).all()
            claim_total = sum([float(cp.amount) for cp in claim_payments])
            total_claim_amount += claim_total
            
            # Get policy info
            policy_info = f"Policy #{c.policy_id}"
            if c.policy and c.policy.vehicle:
                policy_info = f"Policy #{c.policy_id} - {c.policy.vehicle.brand} {c.policy.vehicle.model}"
            
            claims_data.append({
                'claim_id': c.claim_id,
                'policy': policy_info,
                'claim_date': c.claim_date.strftime('%Y-%m-%d') if c.claim_date else 'N/A',
                'description': c.description,
                'status': c.status,
                'amount_paid': claim_total,
                'payments': claim_payments
            })
    
    # ========================================================================
    # PREMIUM PAYMENTS - Get all premium payments across all policies
    # ========================================================================
    premium_payments_data = []
    total_premiums_paid = 0
    
    if policy_ids:
        premium_payments = PremiumPayment.query.filter(
            PremiumPayment.policy_id.in_(policy_ids)
        ).order_by(PremiumPayment.payment_date.desc()).all()
        
        for pp in premium_payments:
            total_premiums_paid += float(pp.amount)
            
            # Get policy info
            policy_info = f"Policy #{pp.policy_id}"
            if pp.policy and pp.policy.vehicle:
                policy_info = f"Policy #{pp.policy_id} - {pp.policy.vehicle.brand} {pp.policy.vehicle.model}"
            
            premium_payments_data.append({
                'payment_id': pp.payment_id,
                'policy': policy_info,
                'payment_date': pp.payment_date,
                'amount': float(pp.amount)
            })
    
    # ========================================================================
    # STATISTICS & SUMMARY
    # ========================================================================
    stats = {
        'total_vehicles': len(vehicles_data),
        'total_policies': len(policies_data),
        'active_policies': len([p for p in policies if p.status == 'active']),
        'total_claims': len(claims_data),
        'open_claims': len([c for c in claims_data if c['status'] == 'open']),
        'total_premiums_paid': total_premiums_paid,
        'total_claims_paid': total_claim_amount,
        'net_value': total_premiums_paid - total_claim_amount
    }
    
    # ========================================================================
    # PREPARE DATA FOR TEMPLATE
    # ========================================================================
    data = {
        'customer': {
            'customer_id': customer.customer_id,
            'name': customer_name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address
        },
        'agent': agent_info,
        'vehicles': vehicles_data,
        'policies': policies_data,
        'claims': claims_data,
        'premium_payments': premium_payments_data,
        'stats': stats,
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'company_name': 'AutoGuard EC'
    }
    
    # ========================================================================
    # RENDER HTML TEMPLATE
    # ========================================================================
    html = render_template('profile1/customer_profile_pdf.html', data=data)
    
    # ========================================================================
    # CONVERT HTML TO PDF
    # ========================================================================
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
    
    if pisa_status.err:
        return Response('Error generating PDF', status=500)
    
    pdf_buffer.seek(0)
    
    # Return PDF as inline display
    return Response(
        pdf_buffer.getvalue(),
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'inline; filename=customer_{customer_id}_profile.pdf'
        }
    )
